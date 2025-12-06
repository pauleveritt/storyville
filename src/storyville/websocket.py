"""WebSocket endpoint for hot reload functionality."""

import asyncio
import json
import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import PurePath

from starlette.websockets import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)


class PageType(Enum):
    """Type of page being viewed by the client."""

    STORY = "story"
    STORY_CONTAINER = "story_container"
    NON_STORY = "non_story"


@dataclass
class PageMetadata:
    """Metadata about the page a WebSocket connection is viewing.

    Attributes:
        page_url: Full URL path of the page (e.g., "/components/heading/story-0/index.html")
        page_type: Type of page (story, story_container, non_story)
        story_id: Story identifier if viewing a story (e.g., "components/heading/story-0")
    """

    page_url: str
    page_type: PageType
    story_id: str | None = None


# Module-level set to track active WebSocket connections
_active_connections: set[WebSocket] = set()

# Module-level dict to track page metadata per connection
_connection_metadata: dict[WebSocket, PageMetadata] = {}

# Store reference to the event loop managing websocket connections
_websocket_loop: asyncio.AbstractEventLoop | None = None


def _extract_story_id_from_url(page_url: str) -> str | None:
    """Extract story identifier from URL path.

    Extracts the story path from URLs like:
    - /components/heading/story-0/index.html -> components/heading/story-0
    - /components/heading/story-0/ -> components/heading/story-0

    Args:
        page_url: Full URL path of the page

    Returns:
        Story identifier or None if not a story page
    """
    path = PurePath(page_url)

    # Remove index.html if present
    if path.name == "index.html":
        path = path.parent

    # Check if this looks like a story path (contains "story-" segment)
    parts = path.parts
    for i, part in enumerate(parts):
        if part.startswith("story-"):
            # Join parts up to and including the story-N segment, skip leading slash
            story_parts = [p for p in parts[1 : i + 1]]
            return "/".join(story_parts) if story_parts else None

    return None


def _classify_page_type(page_url: str) -> PageType:
    """Classify the page type based on URL.

    Args:
        page_url: Full URL path of the page

    Returns:
        PageType enum value
    """
    # Check if it's a story page (has story-N in path)
    if "story-" in page_url and page_url.endswith("/index.html"):
        return PageType.STORY

    # Check if it's a story container (themed_story.html)
    if "themed_story.html" in page_url:
        return PageType.STORY_CONTAINER

    # Everything else is non-story (docs, indexes, etc.)
    return PageType.NON_STORY


async def websocket_endpoint(websocket: WebSocket) -> None:
    """WebSocket endpoint handler for /ws/reload.

    Accepts WebSocket connections from browsers and maintains them in the
    active connections set. Receives initial page metadata from client and
    stores it for targeted broadcasting.

    Args:
        websocket: Starlette WebSocket instance for the connection
    """
    global _websocket_loop

    await websocket.accept()
    _active_connections.add(websocket)

    # Store reference to the event loop managing this connection
    if _websocket_loop is None:
        _websocket_loop = asyncio.get_running_loop()

    logger.info("WebSocket client connected (total: %d)", len(_active_connections))

    try:
        # Wait for initial page metadata message from client
        while True:
            message_text = await websocket.receive_text()
            try:
                message = json.loads(message_text)

                # Handle page_info message to track connection metadata
                if message.get("type") == "page_info":
                    page_url = message.get("page_url", "")
                    page_type_str = message.get("page_type", "")
                    story_id = message.get("story_id")

                    # Parse page type from string or classify from URL
                    if page_type_str:
                        try:
                            page_type = PageType(page_type_str)
                        except ValueError:
                            page_type = _classify_page_type(page_url)
                    else:
                        page_type = _classify_page_type(page_url)

                    # Extract story_id from URL if not provided
                    if story_id is None and page_type == PageType.STORY:
                        story_id = _extract_story_id_from_url(page_url)

                    # Store metadata
                    metadata = PageMetadata(
                        page_url=page_url, page_type=page_type, story_id=story_id
                    )
                    _connection_metadata[websocket] = metadata

                    logger.info(
                        "Page metadata received: url=%s, type=%s, story_id=%s",
                        page_url,
                        page_type.value,
                        story_id,
                    )

            except json.JSONDecodeError:
                logger.warning(
                    "Failed to parse WebSocket message as JSON: %s", message_text
                )
            except Exception as e:
                logger.warning("Error processing WebSocket message: %s", e)

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    finally:
        # Clean up connection and metadata
        _active_connections.discard(websocket)
        _connection_metadata.pop(websocket, None)

        # Clear loop reference if no connections remain
        if not _active_connections:
            _websocket_loop = None

        logger.info(
            "WebSocket client removed (remaining: %d)", len(_active_connections)
        )


async def broadcast_reload_async() -> None:
    """Async version of broadcast_reload.

    Broadcast reload message to all connected WebSocket clients.
    Sends JSON message {"type": "reload"} to all active connections.
    Handles disconnections gracefully by removing failed connections.
    """
    if not _active_connections:
        logger.debug("No WebSocket clients to broadcast to")
        return

    message = json.dumps({"type": "reload"})
    disconnected: list[WebSocket] = []

    for connection in _active_connections:
        try:
            await connection.send_text(message)
        except Exception as e:
            logger.warning("Failed to send to WebSocket client: %s", e)
            disconnected.append(connection)

    # Clean up disconnected clients
    for connection in disconnected:
        _active_connections.discard(connection)
        _connection_metadata.pop(connection, None)

    logger.info("Broadcast reload to %d clients", len(_active_connections))


def _clear_websocket_loop() -> None:
    """Clear the stored websocket loop reference."""
    globals()["_websocket_loop"] = None


def _is_loop_closed_error(e: RuntimeError) -> bool:
    """Check if RuntimeError indicates a closed event loop."""
    error_msg = str(e).lower()
    return "closed" in error_msg or "runner is closed" in error_msg


def broadcast_reload() -> None:
    """Synchronous wrapper for broadcast_reload_async.

    Broadcasts reload message to all connected WebSocket clients.
    This is a synchronous convenience function that handles event loop management.

    In TestClient context, this is called from the main thread while the ASGI app
    runs in a background thread with its own event loop. We use run_coroutine_threadsafe
    to safely schedule the broadcast across threads.
    """
    import concurrent.futures

    # Early return if no clients connected
    if not _active_connections:
        logger.debug("No WebSocket clients to broadcast to")
        return

    # Early return if no websocket loop available
    if _websocket_loop is None:
        logger.debug("No websocket loop available; skipping broadcast")
        return

    # Check if the stored loop is closed
    if _websocket_loop.is_closed():
        logger.warning("Stored websocket loop is closed, clearing reference")
        _clear_websocket_loop()
        return

    # Schedule the broadcast in the websocket event loop
    logger.debug("Scheduling broadcast in websocket event loop")
    try:
        future = asyncio.run_coroutine_threadsafe(
            broadcast_reload_async(), _websocket_loop
        )
        future.result(timeout=5.0)
    except concurrent.futures.TimeoutError as e:
        msg = "Broadcast timed out after 5 seconds"
        raise TimeoutError(msg) from e
    except RuntimeError as e:
        # Loop might have been closed during the call
        if _is_loop_closed_error(e):
            logger.warning("Loop closed during broadcast: %s", e)
            _clear_websocket_loop()
        else:
            raise
