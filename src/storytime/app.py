"""Starlette app for serving static Storytime sites."""

import asyncio
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from functools import partial
from pathlib import Path

from starlette.applications import Starlette
from starlette.routing import Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles

from storytime.build import build_site
from storytime.nodes import get_package_path
from storytime.watchers import watch_and_rebuild
from storytime.websocket import broadcast_reload_async, websocket_endpoint

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(
    app: Starlette,
    input_path: str | None = None,
    package_location: str | None = None,
    output_dir: Path | None = None,
    use_subinterpreters: bool = False,
    with_assertions: bool = True,
) -> AsyncIterator[None]:
    """Starlette lifespan context manager for hot reload watcher.

    Starts a unified watcher task on app startup and cancels it on shutdown.
    The watcher monitors source file changes, triggers rebuilds, and broadcasts
    reload messages to the browser.

    This uses a single watcher that combines the previous dual-watcher approach
    (input + output) into a unified watch -> build -> broadcast workflow.

    Args:
        app: Starlette application instance
        input_path: Path to content directory to monitor (optional)
        package_location: Package location for rebuilds (optional)
        output_dir: Output directory to rebuild to (optional)
        use_subinterpreters: Whether to use subinterpreters for builds (default: False)
        with_assertions: Whether to enable assertions during builds (default: True)

    Yields:
        None (no app state needed)
    """
    tasks: list[asyncio.Task] = []

    # Create subinterpreter pool if enabled
    if use_subinterpreters and input_path and package_location and output_dir:
        from storytime.subinterpreter_pool import create_pool, shutdown_pool

        logger.info("Creating subinterpreter pool for hot reload...")
        pool = create_pool()
        app.state.pool = pool
        logger.info("Subinterpreter pool created")

    # Only start watcher if all required paths are provided
    if input_path and package_location and output_dir:
        logger.info("Starting hot reload watcher...")

        # Determine paths to watch
        # Convert package name (e.g., "examples.minimal") to filesystem path
        content_path = get_package_path(input_path)

        # Check if src/storytime/ exists for static asset watching
        # This would be in the project root where the package is
        storytime_src = Path("src/storytime")
        storytime_path = storytime_src if storytime_src.exists() else None

        # Determine which rebuild callback to use based on mode
        if use_subinterpreters:
            from storytime.subinterpreter_pool import rebuild_callback_subinterpreter

            # Create async callback that uses subinterpreter
            # Bind pool and with_assertions using partial
            rebuild_callback = partial(
                rebuild_callback_subinterpreter,
                pool=app.state.pool,
                with_assertions=with_assertions,
            )
        else:
            # Use direct build_site callback
            # Bind with_assertions using partial
            rebuild_callback = partial(build_site, with_assertions=with_assertions)

        # Create unified watcher task that watches, rebuilds, and broadcasts
        watcher_task = asyncio.create_task(
            watch_and_rebuild(
                content_path=content_path,
                storytime_path=storytime_path,
                rebuild_callback=rebuild_callback,
                broadcast_callback=broadcast_reload_async,
                package_location=package_location,
                output_dir=output_dir,
            ),
            name="unified-watcher",
        )
        tasks.append(watcher_task)

        logger.info("Hot reload watcher started")

    # Yield control to the application
    try:
        yield
    finally:
        # Shutdown: cancel all watcher tasks
        if tasks:
            logger.info("Stopping hot reload watcher...")
            for task in tasks:
                task.cancel()

            # Wait for tasks to complete with timeout
            try:
                await asyncio.wait_for(
                    asyncio.gather(*tasks, return_exceptions=True),
                    timeout=5.0,
                )
            except asyncio.TimeoutError:
                logger.warning("Watcher task did not complete within timeout")
            except asyncio.CancelledError:
                # Expected - task was cancelled
                pass

            logger.info("Hot reload watcher stopped")

        # Shutdown subinterpreter pool if it was created
        if use_subinterpreters and hasattr(app.state, "pool"):
            from storytime.subinterpreter_pool import shutdown_pool

            logger.info("Shutting down subinterpreter pool...")
            shutdown_pool(app.state.pool)
            logger.info("Subinterpreter pool shutdown complete")


def create_app(
    path: Path,
    input_path: str | None = None,
    package_location: str | None = None,
    output_dir: Path | None = None,
    use_subinterpreters: bool = False,
    with_assertions: bool = True,
) -> Starlette:
    """Create a Starlette application to serve a built Storytime site.

    Args:
        path: Path to the built site root directory (e.g., var/)
              This directory should contain index.html, section/*, static/*
        input_path: Optional path to content directory for hot reload watching
        package_location: Optional package location for hot reload rebuilds
        output_dir: Optional output directory for hot reload rebuilds
        use_subinterpreters: Whether to use subinterpreters for hot reload builds (default: False)
                            When True, builds run in isolated subinterpreters for fresh module imports.
                            When False, builds run directly in the main interpreter.
        with_assertions: Whether to enable assertion execution during rendering (default: True)
                        When True, assertions defined on stories will execute and display badges.
                        When False, assertion execution is skipped entirely.

    Returns:
        Configured Starlette application instance ready to serve

    The application serves all content via a single StaticFiles mount at the
    root path with html=True for automatic index.html resolution. It also
    provides a WebSocket endpoint at /ws/reload for hot reload functionality.

    If input_path, package_location, and output_dir are provided, the app
    will start a unified file watcher during its lifespan to enable hot reload.
    The watcher monitors source files, triggers rebuilds on changes, and
    broadcasts reload messages to the browser after successful builds.

    Subinterpreter Mode:
    When use_subinterpreters=True, each rebuild runs in a fresh subinterpreter,
    allowing module changes (e.g., to stories.py) to take effect immediately.
    This is useful for development but adds slight overhead. The default (False)
    maintains backward compatibility with direct builds.
    """
    # Create lifespan context manager with bound parameters
    @asynccontextmanager
    async def app_lifespan(app: Starlette) -> AsyncIterator[None]:
        async with lifespan(
            app,
            input_path,
            package_location,
            output_dir,
            use_subinterpreters,
            with_assertions,
        ):
            yield

    # Create the app
    starlette_app = Starlette(
        debug=True,
        routes=[
            WebSocketRoute("/ws/reload", websocket_endpoint),
            Mount("/", app=StaticFiles(directory=path, html=True), name="site"),
        ],
        lifespan=app_lifespan,
    )

    # Store with_assertions flag in app state for view access
    starlette_app.state.with_assertions = with_assertions

    return starlette_app
