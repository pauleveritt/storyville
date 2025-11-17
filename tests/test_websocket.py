"""Tests for WebSocket reload endpoint."""

from pathlib import Path

from starlette.testclient import TestClient

from storytime.app import create_app
from storytime.build import build_site
from storytime.websocket import broadcast_reload


def test_websocket_accepts_connection(tmp_path: Path) -> None:
    """Test WebSocket connection acceptance at /ws/reload."""
    build_site(package_location="examples.minimal", output_dir=tmp_path)
    app = create_app(tmp_path)

    with TestClient(app) as client:
        with client.websocket_connect("/ws/reload") as websocket:
            # Connection successful if we reach here
            assert websocket is not None


def test_websocket_receives_reload_message(tmp_path: Path) -> None:
    """Test receiving reload message from WebSocket."""
    build_site(package_location="examples.minimal", output_dir=tmp_path)
    app = create_app(tmp_path)

    with TestClient(app) as client:
        with client.websocket_connect("/ws/reload") as websocket:
            # Trigger broadcast
            broadcast_reload()

            # Receive message
            data = websocket.receive_json()
            assert data == {"type": "reload"}


def test_websocket_multiple_connections(tmp_path: Path) -> None:
    """Test handling multiple simultaneous WebSocket connections."""
    build_site(package_location="examples.minimal", output_dir=tmp_path)
    app = create_app(tmp_path)

    with TestClient(app) as client:
        with client.websocket_connect("/ws/reload") as ws1:
            with client.websocket_connect("/ws/reload") as ws2:
                # Both connections should be active
                assert ws1 is not None
                assert ws2 is not None

                # Broadcast to all
                broadcast_reload()

                # Both should receive the message
                data1 = ws1.receive_json()
                data2 = ws2.receive_json()
                assert data1 == {"type": "reload"}
                assert data2 == {"type": "reload"}


def test_websocket_graceful_disconnection(tmp_path: Path) -> None:
    """Test graceful disconnection and cleanup."""
    build_site(package_location="examples.minimal", output_dir=tmp_path)
    app = create_app(tmp_path)

    with TestClient(app) as client:
        with client.websocket_connect("/ws/reload") as websocket:
            # Disconnect by closing
            websocket.close()

        # Connection should be cleaned up
        # Subsequent broadcast should not fail
        broadcast_reload()  # Should not raise exception


def test_websocket_broadcast_with_no_connections(tmp_path: Path) -> None:
    """Test broadcast when no clients are connected."""
    build_site(package_location="examples.minimal", output_dir=tmp_path)
    # Don't need the app for this test - just testing broadcast function
    _ = create_app(tmp_path)

    # Broadcast with no connections should not raise exception
    broadcast_reload()


def test_websocket_connection_cleanup_after_disconnect(tmp_path: Path) -> None:
    """Test that disconnected clients are removed from connection list."""
    build_site(package_location="examples.minimal", output_dir=tmp_path)
    app = create_app(tmp_path)

    with TestClient(app) as client:
        # Connect first client
        with client.websocket_connect("/ws/reload") as ws1:
            # Connect second client
            with client.websocket_connect("/ws/reload") as ws2:
                # Close first client
                ws1.close()

                # Broadcast should only reach ws2
                broadcast_reload()
                data = ws2.receive_json()
                assert data == {"type": "reload"}
