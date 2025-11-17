"""Starlette app for serving static Storytime sites."""

from pathlib import Path

from starlette.applications import Starlette
from starlette.routing import Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles

from storytime.websocket import websocket_endpoint


def create_app(path: Path) -> Starlette:
    """Create a Starlette application to serve a built Storytime site.

    Args:
        path: Path to the built site root directory (e.g., var/)
              This directory should contain index.html, section/*, static/*

    Returns:
        Configured Starlette application instance ready to serve

    The application serves all content via a single StaticFiles mount at the
    root path with html=True for automatic index.html resolution. It also
    provides a WebSocket endpoint at /ws/reload for hot reload functionality.
    """
    return Starlette(
        debug=True,
        routes=[
            WebSocketRoute("/ws/reload", websocket_endpoint),
            Mount("/", app=StaticFiles(directory=path, html=True), name="site"),
        ],
    )
