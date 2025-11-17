"""WebSocket endpoint for hot reload functionality."""

import json
import logging

from starlette.websockets import WebSocket, WebSocketDisconnect

# Module-level set to track active WebSocket connections
_active_connections: set[WebSocket] = set()

logger = logging.getLogger(__name__)


async def websocket_endpoint(websocket: WebSocket) -> None:
    """WebSocket endpoint handler for /ws/reload.

    Accepts WebSocket connections from browsers and maintains them in the
    active connections set. Listens for disconnections and cleans up.

    Args:
        websocket: Starlette WebSocket instance for the connection
    """
    await websocket.accept()
    _active_connections.add(websocket)
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
        logger.info(
            "WebSocket client removed (remaining: %d)", len(_active_connections)
        )


def broadcast_reload() -> None:
    """Broadcast reload message to all connected WebSocket clients.

    Sends JSON message {"type": "reload"} to all active connections.
    Handles disconnections gracefully by removing failed connections.
    This function is synchronous but schedules async broadcast operations.
    """
    if not _active_connections:
        logger.debug("No WebSocket clients to broadcast to")
        return

    message = json.dumps({"type": "reload"})
    disconnected: list[WebSocket] = []

    # Note: This is a synchronous wrapper for use in async contexts
    # In practice, this will be called from async watcher code
    import asyncio

    async def _broadcast() -> None:
        """Internal async broadcast implementation."""
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

    # Try to get running event loop, or create a new one
    try:
        loop = asyncio.get_running_loop()
        # If we have a running loop, create a task
        loop.create_task(_broadcast())
    except RuntimeError:
        # No running loop - run in new event loop
        asyncio.run(_broadcast())
