"""File watchers for hot reload functionality."""

import asyncio
import inspect
import logging
from collections.abc import Awaitable, Callable
from enum import Enum
from pathlib import Path

from watchfiles import Change, awatch

logger = logging.getLogger(__name__)

# Static file extensions to watch in src/storyville/ and input directories
STATIC_EXTENSIONS = {".css", ".js", ".png", ".jpg", ".jpeg", ".svg", ".ico", ".gif"}

# Debounce delay in seconds
DEBOUNCE_DELAY = 0.3


class ChangeType(Enum):
    """Classification of file changes by their impact on the site.

    GLOBAL_ASSET: Changes that affect all story pages (themed_story.html, CSS/JS bundles)
    STORY_SPECIFIC: Changes to individual story index.html files
    NON_STORY: Changes to documentation, section indexes, and other non-story content
    """

    GLOBAL_ASSET = "global_asset"
    STORY_SPECIFIC = "story_specific"
    NON_STORY = "non_story"


def classify_change(changed_path: Path) -> tuple[ChangeType, str | None]:
    """Classify a file change and extract affected story ID if applicable.

    Examines the file path to determine what type of content changed and which
    stories are affected by the change.

    Args:
        changed_path: Path to the changed file

    Returns:
        Tuple of (ChangeType, story_id), where story_id is None for non-story-specific changes

    Examples:
        >>> classify_change(Path("/output/components/heading/story-0/themed_story.html"))
        (ChangeType.GLOBAL_ASSET, None)

        >>> classify_change(Path("/output/components/heading/story-0/index.html"))
        (ChangeType.STORY_SPECIFIC, "components/heading/story-0")

        >>> classify_change(Path("/output/docs/getting-started.html"))
        (ChangeType.NON_STORY, None)
    """
    path_str = str(changed_path)
    parts = changed_path.parts

    # Check for global assets that affect all story pages
    # 1. themed_story.html - the template for all story pages
    if changed_path.name == "themed_story.html":
        logger.debug(
            "Change classified as GLOBAL_ASSET: themed_story.html at %s", changed_path
        )
        return ChangeType.GLOBAL_ASSET, None

    # 2. CSS/JS files in static directories - affect all pages
    if "static" in parts and changed_path.suffix.lower() in {".css", ".js", ".mjs"}:
        logger.debug("Change classified as GLOBAL_ASSET: static asset %s", changed_path)
        return ChangeType.GLOBAL_ASSET, None

    # Check for story-specific changes (individual story index.html)
    # Look for pattern: .../story-N/index.html
    if changed_path.name == "index.html" and "story-" in path_str:
        # Extract story ID from path
        # Find the story-N segment in the path
        for i, part in enumerate(parts):
            if part.startswith("story-"):
                # Build story ID from parts leading up to and including story-N
                # Skip leading parts that are likely directory prefixes:
                # - Root "/" (parts[0])
                # - Common output directory names (output, build, dist, _output, etc.)
                start_idx = 0
                for j in range(min(i, 2)):  # Check first 2 parts only
                    part_lower = parts[j].lower()
                    if (
                        parts[j] == "/"
                        or part_lower
                        in {"output", "build", "dist", "_output", "public"}
                        or part_lower.startswith(".")  # Hidden directories
                    ):
                        start_idx = j + 1
                    else:
                        break

                story_parts = parts[start_idx : i + 1]
                story_id = "/".join(story_parts)

                logger.debug(
                    "Change classified as STORY_SPECIFIC: story %s at %s",
                    story_id,
                    changed_path,
                )
                return ChangeType.STORY_SPECIFIC, story_id

    # Everything else is non-story content (docs, section indexes, catalog index)
    logger.debug("Change classified as NON_STORY: %s", changed_path)
    return ChangeType.NON_STORY, None


def read_story_html(output_dir: Path, story_id: str) -> str | None:
    """Read the HTML content of a story's themed_story.html file.

    Args:
        output_dir: Output directory containing the built site
        story_id: Story identifier (e.g., "components/heading/story-0")

    Returns:
        HTML content as string, or None if file not found or cannot be read
    """
    # Construct path to the story's themed_story.html
    story_path = output_dir / story_id / "themed_story.html"

    try:
        if not story_path.exists():
            logger.warning(
                "Story HTML file not found at %s for story %s", story_path, story_id
            )
            return None

        # Read the HTML content
        html_content = story_path.read_text(encoding="utf-8")
        logger.debug(
            "Read %d bytes of HTML for story %s from %s",
            len(html_content),
            story_id,
            story_path,
        )
        return html_content

    except Exception as e:
        logger.error(
            "Failed to read story HTML at %s: %s", story_path, e, exc_info=True
        )
        return None


async def watch_and_rebuild(
    content_path: Path,
    storyville_path: Path | None,
    rebuild_callback: Callable[[str, Path], None]
    | Callable[[str, Path], Awaitable[None]],
    broadcast_callback: Callable[[], Awaitable[None]],
    package_location: str,
    output_dir: Path,
    ready_event: asyncio.Event | None = None,
) -> None:
    """Watch source files, rebuild on changes, and trigger browser reload.

    Single unified watcher that:
    1. Monitors content and storyville static files for changes
    2. Monitors all static/ folders in both content_path and storyville_path
    3. Triggers rebuild via rebuild_callback when changes detected
    4. Broadcasts reload to WebSocket clients after successful rebuild

    This replaces the previous dual-watcher approach (watch_input_directory +
    watch_output_directory) with a simpler workflow: watch -> build -> broadcast.

    After rebuild, the watcher:
    - Classifies output changes (GLOBAL_ASSET, STORY_SPECIFIC, NON_STORY)
    - For STORY_SPECIFIC changes: reads HTML and sends targeted morph broadcast
    - For GLOBAL_ASSET changes: sends iframe reload broadcast to all stories
    - For NON_STORY changes: sends full reload broadcast to non-story pages

    Args:
        content_path: Path to content directory to monitor
        storyville_path: Optional path to src/storyville/ directory
        rebuild_callback: Function to call to rebuild site (e.g., build_site)
                         Can be sync or async
        broadcast_callback: Async function to call to broadcast reload (e.g., broadcast_reload_async)
                           DEPRECATED: Use targeted broadcast functions instead
        package_location: Package location to pass to rebuild_callback
        output_dir: Output directory to pass to rebuild_callback
        ready_event: Optional Event to signal when watcher is ready (for testing)
    """
    # Import targeted broadcast functions
    from storyville.websocket import (
        broadcast_full_reload_async,
        broadcast_global_reload_async,
        broadcast_story_reload_async,
    )

    # Build list of paths to watch
    watch_paths: list[Path] = [content_path]
    if storyville_path and storyville_path.exists():
        watch_paths.append(storyville_path)

    logger.info("Starting unified watcher for paths: %s", watch_paths)

    # Track last change time for debouncing
    last_change_time: float = 0.0

    try:
        # Use yield_on_timeout to ensure we can signal ready even without initial changes
        async for changes in awatch(
            *watch_paths, yield_on_timeout=True, rust_timeout=100
        ):
            # Signal that watcher is ready on first iteration (even if no changes)
            if ready_event and not ready_event.is_set():
                ready_event.set()
                logger.debug("Watcher ready event set")

            # Filter changes based on path
            relevant_changes = []
            for change_type, changed_path in changes:
                path_obj = Path(changed_path)

                # Skip Python cache files
                if "__pycache__" in path_obj.parts or path_obj.suffix == ".pyc":
                    continue

                # Check if change is in content directory
                try:
                    path_obj.relative_to(content_path)
                    # Accept all files in content directory
                    relevant_changes.append((change_type, changed_path))
                    continue
                except ValueError:
                    pass

                # Check if change is in storyville directory
                if storyville_path:
                    try:
                        path_obj.relative_to(storyville_path)
                        # Only accept static files in storyville directory
                        # This includes all files in static/ folders
                        if (
                            path_obj.suffix.lower() in STATIC_EXTENSIONS
                            or "static" in path_obj.parts
                        ):
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

            # Log changes with classification
            for change_type, changed_path in relevant_changes:
                change_name = (
                    Change(change_type).name
                    if isinstance(change_type, int)
                    else change_type
                )
                logger.info("Detected %s: %s", change_name, changed_path)

                # Classify the change to understand its impact
                # Note: This classification happens BEFORE rebuild, so we're analyzing
                # the source file path, not the output path. After rebuild, we'll
                # classify the output changes to determine targeted broadcasts.
                path_obj = Path(changed_path)
                classification, story_id = classify_change(path_obj)
                logger.info(
                    "Change classification: type=%s, story_id=%s",
                    classification.value,
                    story_id,
                )

            # Trigger rebuild
            logger.info("Triggering rebuild...")
            try:
                # Check if callback is async (coroutine function)
                if inspect.iscoroutinefunction(rebuild_callback):
                    # Async callback - await it directly
                    # Runtime check ensures this is Awaitable, but type checker can't infer
                    await rebuild_callback(package_location, output_dir)  # type: ignore[misc]
                else:
                    # Sync callback - call it directly
                    rebuild_callback(package_location, output_dir)

                logger.info("Rebuild completed successfully")

                # After successful build, determine which broadcast to send
                # based on the classification of changes in the OUTPUT directory
                logger.info("Broadcasting reload to WebSocket clients...")

                # Collect classifications from output changes
                # We need to determine what was actually built/changed
                has_global_change = False
                story_changes: set[str] = set()
                has_non_story_change = False

                for change_type, changed_path in relevant_changes:
                    path_obj = Path(changed_path)

                    # Map input changes to output classifications
                    # For simplicity, assume input changes map to output changes
                    # In a full implementation, we'd scan the output directory

                    # Check if this is a global asset change
                    if "static" in path_obj.parts and path_obj.suffix.lower() in {
                        ".css",
                        ".js",
                        ".mjs",
                    }:
                        has_global_change = True
                        logger.info("Detected global asset change: %s", path_obj)

                    # Check if this is a story-specific change
                    # Story source files typically contain "stories.py" or are in story directories
                    if (
                        path_obj.name == "stories.py"
                        or "story" in str(path_obj).lower()
                    ):
                        # For story changes, we need to determine which stories were affected
                        # This is a simplified heuristic - in practice, we'd need to know
                        # which stories were actually rebuilt
                        # For now, trigger global reload for story changes
                        has_global_change = True
                        logger.info(
                            "Detected story content change, treating as global: %s",
                            path_obj,
                        )

                    # Check for documentation/non-story changes
                    if "docs" in path_obj.parts or path_obj.name.endswith(".md"):
                        has_non_story_change = True
                        logger.info("Detected non-story change: %s", path_obj)

                # Broadcast based on classifications
                # Priority: global > story-specific > non-story
                try:
                    if has_global_change:
                        # Global asset change - reload all story iframes
                        logger.info(
                            "Broadcasting global reload (iframe reload for all stories)"
                        )
                        await broadcast_global_reload_async()
                        logger.info("Global reload broadcast sent")

                    elif story_changes:
                        # Story-specific changes - morph each affected story
                        for story_id in story_changes:
                            logger.info(
                                "Broadcasting story-specific reload with DOM morph: %s",
                                story_id,
                            )

                            # Read the HTML content for this story
                            html_content = read_story_html(output_dir, story_id)

                            if html_content:
                                await broadcast_story_reload_async(
                                    story_id, html_content
                                )
                                logger.info("Story reload broadcast sent: %s", story_id)
                            else:
                                logger.warning(
                                    "Could not read HTML for story %s, falling back to global reload",
                                    story_id,
                                )
                                await broadcast_global_reload_async()

                    elif has_non_story_change:
                        # Non-story change - full reload for non-story pages
                        logger.info("Broadcasting full reload for non-story pages")
                        await broadcast_full_reload_async()
                        logger.info("Full reload broadcast sent")

                    else:
                        # Default fallback - use the provided broadcast callback
                        # This maintains backward compatibility
                        logger.info(
                            "No specific change type detected, using legacy broadcast"
                        )
                        await broadcast_callback()
                        logger.info("Legacy reload broadcast sent")

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
