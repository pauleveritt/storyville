"""File watchers for hot reload functionality."""

import asyncio
import logging
from collections.abc import Callable
from pathlib import Path

from watchfiles import Change, awatch

logger = logging.getLogger(__name__)

# Static file extensions to watch in src/storytime/
STATIC_EXTENSIONS = {".css", ".js", ".png", ".jpg", ".jpeg", ".svg", ".ico", ".gif"}

# Debounce delay in seconds
DEBOUNCE_DELAY = 0.3


async def watch_input_directory(
    content_path: Path,
    storytime_path: Path | None,
    rebuild_callback: Callable[[str, Path], None],
    package_location: str,
    output_dir: Path,
) -> None:
    """Watch input directories for changes and trigger rebuilds.

    Monitors two directories:
    1. Content directory (content_path) - watch all file types
    2. Storytime static assets (storytime_path) - watch only static files

    Args:
        content_path: Path to content directory to monitor
        storytime_path: Optional path to src/storytime/ directory
        rebuild_callback: Function to call when changes detected
        package_location: Package location to pass to rebuild_callback
        output_dir: Output directory to pass to rebuild_callback
    """
    # Build list of paths to watch
    watch_paths: list[Path] = [content_path]
    if storytime_path and storytime_path.exists():
        watch_paths.append(storytime_path)

    logger.info("Starting INPUT watcher for paths: %s", watch_paths)

    # Track last change time for debouncing
    last_change_time: float = 0.0

    try:
        async for changes in awatch(*watch_paths):
            # Filter changes based on path
            relevant_changes = []
            for change_type, changed_path in changes:
                path_obj = Path(changed_path)

                # Skip Python cache files
                if "__pycache__" in path_obj.parts or path_obj.suffix == ".pyc":
                    continue

                # Check if change is in content directory (accept all files)
                try:
                    path_obj.relative_to(content_path)
                    relevant_changes.append((change_type, changed_path))
                    continue
                except ValueError:
                    pass

                # Check if change is in storytime directory (only static files)
                if storytime_path:
                    try:
                        path_obj.relative_to(storytime_path)
                        if path_obj.suffix.lower() in STATIC_EXTENSIONS:
                            relevant_changes.append((change_type, changed_path))
                    except ValueError:
                        pass

            if not relevant_changes:
                continue

            # Implement simple debouncing (use monotonic clock, independent of event loop)
            from time import monotonic as _monotonic
            current_time = _monotonic()
            if current_time - last_change_time < DEBOUNCE_DELAY:
                logger.debug("Debouncing file changes (too soon after last change)")
                continue

            last_change_time = current_time

            # Log changes
            for change_type, changed_path in relevant_changes:
                change_name = Change(change_type).name if isinstance(change_type, int) else change_type
                logger.info("Detected %s: %s", change_name, changed_path)

            # Trigger rebuild
            logger.info("Triggering rebuild...")
            try:
                rebuild_callback(package_location, output_dir)
                logger.info("Rebuild completed successfully")
            except Exception as e:
                logger.error("Rebuild failed: %s", e, exc_info=True)
                # Continue watching even if build fails

    except asyncio.CancelledError:
        logger.info("INPUT watcher stopped")
        raise
    except RuntimeError as e:
        # Handle shutdown races with anyio/asyncio runners gracefully
        msg = str(e).lower()
        if (
            "runner is closed" in msg
            or "event loop is closed" in msg
            or "another loop is running" in msg
        ):
            logger.info("INPUT watcher stopped due to loop shutdown: %s", e)
            return
        logger.error("INPUT watcher runtime error: %s", e, exc_info=True)
        return


async def watch_and_rebuild(
    content_path: Path,
    storytime_path: Path | None,
    rebuild_callback: Callable[[str, Path], None],
    broadcast_callback: Callable[[], None],
    package_location: str,
    output_dir: Path,
) -> None:
    """Watch source files, rebuild on changes, and trigger browser reload.

    Single unified watcher that:
    1. Monitors content and storytime static files for changes
    2. Triggers rebuild via rebuild_callback when changes detected
    3. Broadcasts reload to WebSocket clients after successful rebuild

    This replaces the previous dual-watcher approach (watch_input_directory +
    watch_output_directory) with a simpler workflow: watch -> build -> broadcast.

    Args:
        content_path: Path to content directory to monitor
        storytime_path: Optional path to src/storytime/ directory
        rebuild_callback: Function to call to rebuild site (e.g., build_site)
        broadcast_callback: Function to call to broadcast reload (e.g., broadcast_reload)
        package_location: Package location to pass to rebuild_callback
        output_dir: Output directory to pass to rebuild_callback
    """
    # Build list of paths to watch
    watch_paths: list[Path] = [content_path]
    if storytime_path and storytime_path.exists():
        watch_paths.append(storytime_path)

    logger.info("Starting unified watcher for paths: %s", watch_paths)

    # Track last change time for debouncing
    last_change_time: float = 0.0

    try:
        async for changes in awatch(*watch_paths):
            # Filter changes based on path
            relevant_changes = []
            for change_type, changed_path in changes:
                path_obj = Path(changed_path)

                # Skip Python cache files
                if "__pycache__" in path_obj.parts or path_obj.suffix == ".pyc":
                    continue

                # Check if change is in content directory (accept all files)
                try:
                    path_obj.relative_to(content_path)
                    relevant_changes.append((change_type, changed_path))
                    continue
                except ValueError:
                    pass

                # Check if change is in storytime directory (only static files)
                if storytime_path:
                    try:
                        path_obj.relative_to(storytime_path)
                        if path_obj.suffix.lower() in STATIC_EXTENSIONS:
                            relevant_changes.append((change_type, changed_path))
                    except ValueError:
                        pass

            if not relevant_changes:
                continue

            # Implement simple debouncing (use monotonic clock, independent of event loop)
            from time import monotonic as _monotonic
            current_time = _monotonic()
            if current_time - last_change_time < DEBOUNCE_DELAY:
                logger.debug("Debouncing file changes (too soon after last change)")
                continue

            last_change_time = current_time

            # Log changes
            for change_type, changed_path in relevant_changes:
                change_name = Change(change_type).name if isinstance(change_type, int) else change_type
                logger.info("Detected %s: %s", change_name, changed_path)

            # Trigger rebuild
            logger.info("Triggering rebuild...")
            try:
                rebuild_callback(package_location, output_dir)
                logger.info("Rebuild completed successfully")

                # After successful build, broadcast reload to WebSocket clients
                logger.info("Broadcasting reload to WebSocket clients...")
                try:
                    broadcast_callback()
                    logger.info("Reload broadcast sent")
                except Exception as e:
                    logger.error("Broadcast failed: %s", e, exc_info=True)
                    # Continue watching even if broadcast fails

            except Exception as e:
                logger.error("Rebuild failed: %s", e, exc_info=True)
                # Continue watching even if build fails (don't broadcast on failure)

    except asyncio.CancelledError:
        logger.info("Unified watcher stopped")
        raise
    except RuntimeError as e:
        # Handle shutdown races with anyio/asyncio runners gracefully
        msg = str(e).lower()
        if (
            "runner is closed" in msg
            or "event loop is closed" in msg
            or "another loop is running" in msg
        ):
            logger.info("Unified watcher stopped due to loop shutdown: %s", e)
            return
        logger.error("Unified watcher runtime error: %s", e, exc_info=True)
        return


# Legacy function - kept for backward compatibility but deprecated
async def watch_output_directory(
    output_dir: Path,
    broadcast_callback: Callable[[], None],
) -> None:
    """Watch output directory for changes and trigger WebSocket broadcast.

    DEPRECATED: This function is kept for backward compatibility but is no longer
    used. The new watch_and_rebuild() function provides a unified watch-build-broadcast
    workflow that eliminates the need for separate output watching.

    Monitors the output directory where build_site() writes HTML.
    When changes are detected, broadcasts reload message to WebSocket clients.

    Args:
        output_dir: Path to output directory to monitor
        broadcast_callback: Function to call to broadcast reload message
    """
    logger.info("Starting OUTPUT watcher for path: %s", output_dir)

    # Track last change time for debouncing
    last_change_time: float = 0.0

    try:
        async for changes in awatch(output_dir):
            # Filter out any changes we want to ignore
            relevant_changes = []
            for change_type, changed_path in changes:
                path_obj = Path(changed_path)

                # Skip Python cache files (shouldn't be in output, but just in case)
                if "__pycache__" in path_obj.parts or path_obj.suffix == ".pyc":
                    continue

                relevant_changes.append((change_type, changed_path))

            if not relevant_changes:
                continue

            # Implement simple debouncing (use monotonic clock, independent of event loop)
            from time import monotonic as _monotonic
            current_time = _monotonic()
            if current_time - last_change_time < DEBOUNCE_DELAY:
                logger.debug("Debouncing output changes (too soon after last change)")
                continue

            last_change_time = current_time

            # Don't log individual output file changes (too noisy)
            # Just trigger the broadcast

            # Trigger broadcast
            logger.info("Broadcasting reload to WebSocket clients...")
            try:
                broadcast_callback()
                logger.info("Reload broadcast sent")
            except Exception as e:
                logger.error("Broadcast failed: %s", e, exc_info=True)
                # Continue watching even if broadcast fails

    except asyncio.CancelledError:
        logger.info("OUTPUT watcher stopped")
        raise
    except RuntimeError as e:
        # Handle shutdown races with anyio/asyncio runners gracefully
        msg = str(e).lower()
        if (
            "runner is closed" in msg
            or "event loop is closed" in msg
            or "another loop is running" in msg
        ):
            logger.info("OUTPUT watcher stopped due to loop shutdown: %s", e)
            return
        logger.error("OUTPUT watcher runtime error: %s", e, exc_info=True)
        return
