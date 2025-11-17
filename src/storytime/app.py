"""Starlette app for serving static Storytime sites."""

import asyncio
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from starlette.applications import Starlette
from starlette.routing import Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles

from storytime.build import build_site
from storytime.nodes import get_package_path
from storytime.watchers import watch_and_rebuild
from storytime.websocket import broadcast_reload, websocket_endpoint

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(
    app: Starlette,
    input_path: str | None = None,
    package_location: str | None = None,
    output_dir: Path | None = None,
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

    Yields:
        None (no app state needed)
    """
    tasks: list[asyncio.Task] = []

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

        # Create unified watcher task that watches, rebuilds, and broadcasts
        watcher_task = asyncio.create_task(
            watch_and_rebuild(
                content_path=content_path,
                storytime_path=storytime_path,
                rebuild_callback=build_site,
                broadcast_callback=broadcast_reload,
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


def create_app(
    path: Path,
    input_path: str | None = None,
    package_location: str | None = None,
    output_dir: Path | None = None,
) -> Starlette:
    """Create a Starlette application to serve a built Storytime site.

    Args:
        path: Path to the built site root directory (e.g., var/)
              This directory should contain index.html, section/*, static/*
        input_path: Optional path to content directory for hot reload watching
        package_location: Optional package location for hot reload rebuilds
        output_dir: Optional output directory for hot reload rebuilds

    Returns:
        Configured Starlette application instance ready to serve

    The application serves all content via a single StaticFiles mount at the
    root path with html=True for automatic index.html resolution. It also
    provides a WebSocket endpoint at /ws/reload for hot reload functionality.

    If input_path, package_location, and output_dir are provided, the app
    will start a unified file watcher during its lifespan to enable hot reload.
    The watcher monitors source files, triggers rebuilds on changes, and
    broadcasts reload messages to the browser after successful builds.
    """
    # Create lifespan context manager with bound parameters
    @asynccontextmanager
    async def app_lifespan(app: Starlette) -> AsyncIterator[None]:
        async with lifespan(app, input_path, package_location, output_dir):
            yield

    return Starlette(
        debug=True,
        routes=[
            WebSocketRoute("/ws/reload", websocket_endpoint),
            Mount("/", app=StaticFiles(directory=path, html=True), name="site"),
        ],
        lifespan=app_lifespan,
    )
