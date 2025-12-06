"""End-to-end integration tests for hot reload feature.

These tests verify the complete hot reload workflow from file changes
through rebuilds to WebSocket notifications.
"""

import asyncio
from pathlib import Path
from unittest.mock import patch

import pytest
from starlette.testclient import TestClient

from storyville.app import create_app
from storyville.build import build_site
from storyville.watchers import watch_and_rebuild
from storyville.websocket import broadcast_reload


@pytest.mark.slow
@pytest.mark.anyio
async def test_end_to_end_content_change_flow(tmp_path: Path, watcher_runner) -> None:
    """Test complete flow: content change -> rebuild -> broadcast.

    This test verifies the unified hot reload pipeline:
    1. File changes in content directory
    2. Unified watcher detects change
    3. Rebuild is triggered
    4. WebSocket broadcast is sent after successful rebuild
    """
    # Setup directories
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Track callbacks
    rebuild_called = asyncio.Event()
    broadcast_called = asyncio.Event()
    rebuild_count = 0
    broadcast_count = 0

    def rebuild_callback(package_location: str, output_dir_arg: Path) -> None:
        nonlocal rebuild_count
        rebuild_count += 1
        rebuild_called.set()
        # Simulate rebuild by creating a file in output directory
        output_file = output_dir_arg / f"output_{rebuild_count}.html"
        output_file.write_text(f"<html>Build {rebuild_count}</html>")

    async def broadcast_callback() -> None:
        nonlocal broadcast_count
        broadcast_count += 1
        broadcast_called.set()

    # Start unified watcher
    async with watcher_runner(
        watch_and_rebuild,
        content_path=content_dir,
        storyville_path=None,
        rebuild_callback=rebuild_callback,
        broadcast_callback=broadcast_callback,
        package_location="test",
        output_dir=output_dir,
    ):
        # Trigger the flow: create a content file
        content_file = content_dir / "page.txt"
        content_file.write_text("Hello World")

        # Wait for rebuild to be called
        try:
            await asyncio.wait_for(rebuild_called.wait(), timeout=3.0)
        except asyncio.TimeoutError:
            pytest.fail("Rebuild was not triggered within timeout")

        # Wait for broadcast to be called (after rebuild)
        try:
            await asyncio.wait_for(broadcast_called.wait(), timeout=3.0)
        except asyncio.TimeoutError:
            pytest.fail("Broadcast was not triggered within timeout")

        # Verify both callbacks were called
        assert rebuild_count >= 1, "Rebuild should have been called"
        assert broadcast_count >= 1, "Broadcast should have been called"

        # Verify output file was created by rebuild
        output_files = list(output_dir.glob("*.html"))
        assert len(output_files) > 0, "Rebuild should have created output files"


@pytest.mark.slow
@pytest.mark.anyio
async def test_multiple_rapid_file_changes_debounced(tmp_path: Path, watcher_runner) -> None:
    """Test that multiple rapid file changes result in a single rebuild.

    Verifies server-side debouncing prevents multiple rebuilds when
    many files change at once (e.g., during git checkout).
    """
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    rebuild_count = 0
    rebuild_event = asyncio.Event()

    def rebuild_callback(package_location: str, output_dir_arg: Path) -> None:
        nonlocal rebuild_count
        rebuild_count += 1
        rebuild_event.set()

    async def broadcast_callback() -> None:
        pass  # No-op for this test

    # Start unified watcher
    async with watcher_runner(
        watch_and_rebuild,
        content_path=content_dir,
        storyville_path=None,
        rebuild_callback=rebuild_callback,
        broadcast_callback=broadcast_callback,
        package_location="test",
        output_dir=output_dir,
    ):
        # Create multiple files rapidly (within debounce window)
        for i in range(5):
            test_file = content_dir / f"file{i}.txt"
            test_file.write_text(f"Content {i}")
            await asyncio.sleep(0.05)  # Very short delay between changes

        # Wait for rebuild
        try:
            await asyncio.wait_for(rebuild_event.wait(), timeout=3.0)
        except asyncio.TimeoutError:
            pytest.fail("Rebuild was not called within timeout")

        # Give time to ensure no additional rebuilds happen (reduced from 1.0s)
        await asyncio.sleep(0.5)

        # Due to debouncing, we should have only 1-2 rebuilds, not 5
        assert rebuild_count <= 2, (
            f"Expected at most 2 rebuilds due to debouncing, got {rebuild_count}"
        )


@pytest.mark.slow
def test_websocket_client_receives_reload_message(tmp_path: Path) -> None:
    """Test that WebSocket client receives reload message after broadcast.

    This test verifies the WebSocket communication between server and client.
    """
    build_site(package_location="examples.minimal", output_dir=tmp_path)
    app = create_app(tmp_path)

    with TestClient(app) as client:
        with client.websocket_connect("/ws/reload") as websocket:
            # Trigger a broadcast
            broadcast_reload()

            # Client should receive the reload message
            data = websocket.receive_json()
            assert data == {"type": "reload"}


@pytest.mark.slow
@pytest.mark.anyio
async def test_static_asset_change_triggers_rebuild(tmp_path: Path, watcher_runner) -> None:
    """Test that static asset changes in src/storyville/ trigger rebuild.

    Verifies that the INPUT watcher correctly monitors and responds to
    changes in static files (CSS, JS, etc.) in the Storyville directory.
    """
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    storyville_dir = tmp_path / "storyville"
    storyville_dir.mkdir()
    static_dir = storyville_dir / "static"
    static_dir.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    rebuild_called = asyncio.Event()
    rebuild_args_list: list[tuple[str, Path]] = []

    def rebuild_callback(package_location: str, output_dir_arg: Path) -> None:
        rebuild_args_list.append((package_location, output_dir_arg))
        rebuild_called.set()

    async def broadcast_callback() -> None:
        pass  # No-op for this test

    # Start unified watcher with both content and storyville paths
    async with watcher_runner(
        watch_and_rebuild,
        content_path=content_dir,
        storyville_path=storyville_dir,
        rebuild_callback=rebuild_callback,
        broadcast_callback=broadcast_callback,
        package_location="test_package",
        output_dir=output_dir,
    ):
        # Create a CSS file (static asset)
        css_file = static_dir / "styles.css"
        css_file.write_text("body { background: blue; }")

        # Wait for rebuild to be called
        try:
            await asyncio.wait_for(rebuild_called.wait(), timeout=3.0)
        except asyncio.TimeoutError:
            pytest.fail("Rebuild was not called for static asset change")

        # Verify rebuild was called with correct args
        assert len(rebuild_args_list) > 0
        assert rebuild_args_list[0] == ("test_package", output_dir)


def test_app_lifespan_starts_and_stops_watchers_cleanly(tmp_path: Path) -> None:
    """Test that app lifespan properly manages watcher lifecycle.

    Verifies that the unified watcher starts when the app starts and stops cleanly
    when the app shuts down, simulating a full server lifecycle.
    """
    build_site(package_location="examples.minimal", output_dir=tmp_path)

    # Track watcher lifecycle
    watcher_started = False
    watcher_stopped = False

    async def mock_unified_watcher(*args, **kwargs):
        nonlocal watcher_started, watcher_stopped
        watcher_started = True
        try:
            while True:
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            watcher_stopped = True
            raise

    with patch("storyville.app.watch_and_rebuild", side_effect=mock_unified_watcher):

        app = create_app(
            path=tmp_path,
            input_path="examples.minimal",
            package_location="examples.minimal",
            output_dir=tmp_path,
        )

        # TestClient triggers lifespan startup and shutdown
        with TestClient(app) as client:
            # Verify app works
            response = client.get("/")
            assert response.status_code == 200

            # Unified watcher should be started
            assert watcher_started, "Unified watcher should have started"

        # After context exit, watcher should be stopped
        assert watcher_stopped, "Unified watcher should have been stopped"


@pytest.mark.slow
def test_websocket_reconnection_after_server_restart(tmp_path: Path) -> None:
    """Test WebSocket behavior when server restarts.

    Simulates server restart by creating new app instance and verifies
    that client can reconnect to new WebSocket endpoint.
    """
    build_site(package_location="examples.minimal", output_dir=tmp_path)

    # First server instance
    app1 = create_app(tmp_path)
    with TestClient(app1) as client1:
        with client1.websocket_connect("/ws/reload") as ws1:
            # Verify connection works
            broadcast_reload()
            data = ws1.receive_json()
            assert data == {"type": "reload"}

    # Server "restarts" - new app instance
    app2 = create_app(tmp_path)
    with TestClient(app2) as client2:
        with client2.websocket_connect("/ws/reload") as ws2:
            # Verify new connection works
            broadcast_reload()
            data = ws2.receive_json()
            assert data == {"type": "reload"}


@pytest.mark.slow
@pytest.mark.anyio
async def test_rebuild_error_does_not_crash_watcher(tmp_path: Path, watcher_runner) -> None:
    """Test that rebuild errors are handled gracefully without crashing watcher.

    Verifies that the INPUT watcher continues watching even after a rebuild
    fails, ensuring resilience during development.
    """
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Track rebuild attempts
    rebuild_attempts = []
    rebuild_events: list[asyncio.Event] = [
        asyncio.Event(),
        asyncio.Event(),
    ]

    def rebuild_callback(package_location: str, output_dir_arg: Path) -> None:
        attempt = len(rebuild_attempts)
        rebuild_attempts.append((package_location, output_dir_arg))

        if attempt == 0:
            # First attempt fails
            rebuild_events[0].set()
            raise RuntimeError("Simulated rebuild error")
        else:
            # Second attempt succeeds
            rebuild_events[1].set()

    async def broadcast_callback() -> None:
        pass  # No-op for this test

    # Start unified watcher
    async with watcher_runner(
        watch_and_rebuild,
        content_path=content_dir,
        storyville_path=None,
        rebuild_callback=rebuild_callback,
        broadcast_callback=broadcast_callback,
        package_location="test",
        output_dir=output_dir,
    ):
        # First file change (will cause error)
        file1 = content_dir / "file1.txt"
        file1.write_text("Content 1")

        # Wait for first rebuild attempt
        try:
            await asyncio.wait_for(rebuild_events[0].wait(), timeout=3.0)
        except asyncio.TimeoutError:
            pytest.fail("First rebuild attempt was not called")

        # Give debounce time to clear (reduced from 0.5s to just above DEBOUNCE_DELAY)
        await asyncio.sleep(0.35)

        # Second file change (should succeed)
        file2 = content_dir / "file2.txt"
        file2.write_text("Content 2")

        # Wait for second rebuild attempt
        try:
            await asyncio.wait_for(rebuild_events[1].wait(), timeout=3.0)
        except asyncio.TimeoutError:
            pytest.fail("Second rebuild attempt was not called")

        # Verify both attempts were made
        assert len(rebuild_attempts) >= 2, "Watcher should continue after error"


@pytest.mark.slow
def test_multiple_websocket_clients_all_receive_broadcast(tmp_path: Path) -> None:
    """Test that broadcast message reaches all connected WebSocket clients.

    Verifies that when output changes trigger a broadcast, all connected
    browser clients receive the reload message simultaneously.
    """
    build_site(package_location="examples.minimal", output_dir=tmp_path)
    app = create_app(tmp_path)

    with TestClient(app) as client:
        # Connect multiple clients
        with client.websocket_connect("/ws/reload") as ws1:
            with client.websocket_connect("/ws/reload") as ws2:
                with client.websocket_connect("/ws/reload") as ws3:
                    # Broadcast reload
                    broadcast_reload()

                    # All clients should receive the message
                    data1 = ws1.receive_json()
                    data2 = ws2.receive_json()
                    data3 = ws3.receive_json()

                    assert data1 == {"type": "reload"}
                    assert data2 == {"type": "reload"}
                    assert data3 == {"type": "reload"}
