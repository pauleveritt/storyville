"""WebSocket endpoint for hot reload functionality."""

import asyncio
import json
import logging

from starlette.websockets import WebSocket, WebSocketDisconnect

# Module-level set to track active WebSocket connections
_active_connections: set[WebSocket] = set()

# Store reference to the event loop managing websocket connections
_websocket_loop: asyncio.AbstractEventLoop | None = None

logger = logging.getLogger(__name__)


async def websocket_endpoint(websocket: WebSocket) -> None:
    """WebSocket endpoint handler for /ws/reload.

    Accepts WebSocket connections from browsers and maintains them in the
    active connections set. Listens for disconnections and cleans up.

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
        # Keep connection alive and wait for disconnection
        while True:
            # Receive any data to detect disconnection
            # We don't expect clients to send data, but this keeps the connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    finally:
        # Clean up connection
        _active_connections.discard(websocket)

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

    logger.info("Broadcast reload to %d clients", len(_active_connections))


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

    # Check if the stored loop is closed and clear if necessary
    if _websocket_loop.is_closed():
        logger.warning("Stored websocket loop is closed, clearing reference")
        globals()["_websocket_loop"] = None
        logger.debug("No websocket loop available; skipping broadcast")
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
        if "closed" in str(e).lower() or "runner is closed" in str(e).lower():
            logger.warning("Loop closed during broadcast: %s", e)
            globals()["_websocket_loop"] = None
        else:
            raise
