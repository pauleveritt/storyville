"""Integration tests for file watchers."""

import asyncio
from pathlib import Path

import pytest

from storytime.watchers import watch_input_directory, watch_output_directory


@pytest.mark.slow
@pytest.mark.anyio
async def test_input_watcher_detects_content_changes(tmp_path: Path) -> None:
    """Test INPUT watcher detects changes in content directory."""
    # Setup
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Create a mock rebuild callback
    rebuild_called = asyncio.Event()
    rebuild_args: list[tuple[str, Path]] = []

    def rebuild_callback(package_location: str, output_dir_arg: Path) -> None:
        rebuild_args.append((package_location, output_dir_arg))
        rebuild_called.set()

    # Start watcher in background
    watcher_task = asyncio.create_task(
        watch_input_directory(
            content_path=content_dir,
            storytime_path=None,
            rebuild_callback=rebuild_callback,
            package_location="test_package",
            output_dir=output_dir,
        )
    )

    try:
        # Give watcher time to start
        await asyncio.sleep(0.5)

        # Create a file in content directory
        test_file = content_dir / "test.txt"
        test_file.write_text("test content")

        # Wait for rebuild to be called (with timeout)
        try:
            await asyncio.wait_for(rebuild_called.wait(), timeout=3.0)
        except asyncio.TimeoutError:
            pytest.fail("Rebuild callback was not called within timeout")

        # Verify rebuild was called with correct arguments
        assert len(rebuild_args) > 0
        assert rebuild_args[0] == ("test_package", output_dir)

    finally:
        # Clean up watcher
        watcher_task.cancel()
        try:
            await watcher_task
        except asyncio.CancelledError:
            pass


@pytest.mark.slow
@pytest.mark.anyio
async def test_input_watcher_detects_static_asset_changes(tmp_path: Path) -> None:
    """Test INPUT watcher detects static asset changes in src/storytime/."""
    # Setup
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    storytime_dir = tmp_path / "storytime"
    storytime_dir.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Create a mock rebuild callback
    rebuild_called = asyncio.Event()

    def rebuild_callback(package_location: str, output_dir_arg: Path) -> None:
        rebuild_called.set()

    # Start watcher in background
    watcher_task = asyncio.create_task(
        watch_input_directory(
            content_path=content_dir,
            storytime_path=storytime_dir,
            rebuild_callback=rebuild_callback,
            package_location="test_package",
            output_dir=output_dir,
        )
    )

    try:
        # Give watcher time to start
        await asyncio.sleep(0.5)

        # Create a CSS file in storytime directory
        static_dir = storytime_dir / "static"
        static_dir.mkdir()
        css_file = static_dir / "style.css"
        css_file.write_text("body { color: red; }")

        # Wait for rebuild to be called (with timeout)
        try:
            await asyncio.wait_for(rebuild_called.wait(), timeout=3.0)
        except asyncio.TimeoutError:
            pytest.fail("Rebuild callback was not called within timeout")

    finally:
        # Clean up watcher
        watcher_task.cancel()
        try:
            await watcher_task
        except asyncio.CancelledError:
            pass


@pytest.mark.slow
@pytest.mark.anyio
async def test_input_watcher_ignores_python_files_in_storytime(tmp_path: Path) -> None:
    """Test INPUT watcher ignores Python files in src/storytime/."""
    # Setup
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    # Create dummy file to stabilize content directory
    (content_dir / ".gitkeep").write_text("")

    storytime_dir = tmp_path / "storytime"
    storytime_dir.mkdir()
    # Create dummy file to stabilize storytime directory
    (storytime_dir / ".gitkeep").write_text("")

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Create a mock rebuild callback
    rebuild_called = asyncio.Event()

    def rebuild_callback(package_location: str, output_dir_arg: Path) -> None:
        rebuild_called.set()

    # Start watcher in background
    watcher_task = asyncio.create_task(
        watch_input_directory(
            content_path=content_dir,
            storytime_path=storytime_dir,
            rebuild_callback=rebuild_callback,
            package_location="test_package",
            output_dir=output_dir,
        )
    )

    try:
        # Give watcher time to start and process initial directory events
        await asyncio.sleep(1.0)

        # Clear any initial events that may have been triggered
        rebuild_called.clear()

        # Create a Python file in storytime directory (should be ignored)
        py_file = storytime_dir / "test.py"
        py_file.write_text("print('hello')")

        # Wait a bit to ensure watcher doesn't trigger
        await asyncio.sleep(1.0)

        # Verify rebuild was NOT called
        assert not rebuild_called.is_set()

    finally:
        # Clean up watcher
        watcher_task.cancel()
        try:
            await watcher_task
        except asyncio.CancelledError:
            pass


@pytest.mark.slow
@pytest.mark.anyio
async def test_output_watcher_detects_build_changes(tmp_path: Path) -> None:
    """Test OUTPUT watcher detects changes in build output directory."""
    # Setup
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Create a mock broadcast callback
    broadcast_called = asyncio.Event()

    def broadcast_callback() -> None:
        broadcast_called.set()

    # Start watcher in background
    watcher_task = asyncio.create_task(
        watch_output_directory(
            output_dir=output_dir,
            broadcast_callback=broadcast_callback,
        )
    )

    try:
        # Give watcher time to start
        await asyncio.sleep(0.5)

        # Create a file in output directory
        test_file = output_dir / "index.html"
        test_file.write_text("<html><body>Hello</body></html>")

        # Wait for broadcast to be called (with timeout)
        try:
            await asyncio.wait_for(broadcast_called.wait(), timeout=3.0)
        except asyncio.TimeoutError:
            pytest.fail("Broadcast callback was not called within timeout")

    finally:
        # Clean up watcher
        watcher_task.cancel()
        try:
            await watcher_task
        except asyncio.CancelledError:
            pass


@pytest.mark.slow
@pytest.mark.anyio
async def test_watcher_can_be_started_and_stopped(tmp_path: Path) -> None:
    """Test watchers can be started and stopped cleanly."""
    # Setup
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Create mock callbacks
    def rebuild_callback(package_location: str, output_dir_arg: Path) -> None:
        pass

    def broadcast_callback() -> None:
        pass

    # Start INPUT watcher
    input_task = asyncio.create_task(
        watch_input_directory(
            content_path=content_dir,
            storytime_path=None,
            rebuild_callback=rebuild_callback,
            package_location="test",
            output_dir=output_dir,
        )
    )

    # Start OUTPUT watcher
    output_task = asyncio.create_task(
        watch_output_directory(
            output_dir=output_dir,
            broadcast_callback=broadcast_callback,
        )
    )

    # Give watchers time to start
    await asyncio.sleep(0.5)

    # Stop watchers
    input_task.cancel()
    output_task.cancel()

    # Verify tasks complete without errors
    try:
        await input_task
    except asyncio.CancelledError:
        pass  # Expected

    try:
        await output_task
    except asyncio.CancelledError:
        pass  # Expected

    # If we get here without exception, watchers stopped cleanly
    assert True


@pytest.mark.slow
@pytest.mark.anyio
async def test_input_watcher_handles_rebuild_errors(tmp_path: Path) -> None:
    """Test INPUT watcher continues watching after rebuild errors."""
    # Setup
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Create a mock rebuild callback that fails first time
    call_count = 0
    rebuild_events: list[asyncio.Event] = [asyncio.Event(), asyncio.Event()]

    def rebuild_callback(package_location: str, output_dir_arg: Path) -> None:
        nonlocal call_count
        if call_count == 0:
            call_count += 1
            rebuild_events[0].set()
            raise RuntimeError("Simulated build failure")
        else:
            call_count += 1
            rebuild_events[1].set()

    # Start watcher in background
    watcher_task = asyncio.create_task(
        watch_input_directory(
            content_path=content_dir,
            storytime_path=None,
            rebuild_callback=rebuild_callback,
            package_location="test_package",
            output_dir=output_dir,
        )
    )

    try:
        # Give watcher time to start
        await asyncio.sleep(0.5)

        # Create first file (will trigger error)
        test_file1 = content_dir / "test1.txt"
        test_file1.write_text("test content 1")

        # Wait for first rebuild attempt
        try:
            await asyncio.wait_for(rebuild_events[0].wait(), timeout=3.0)
        except asyncio.TimeoutError:
            pytest.fail("First rebuild callback was not called")

        # Give debounce time to pass
        await asyncio.sleep(0.5)

        # Create second file (should succeed)
        test_file2 = content_dir / "test2.txt"
        test_file2.write_text("test content 2")

        # Wait for second rebuild attempt
        try:
            await asyncio.wait_for(rebuild_events[1].wait(), timeout=3.0)
        except asyncio.TimeoutError:
            pytest.fail("Second rebuild callback was not called")

        # Verify both callbacks were called
        assert call_count == 2

    finally:
        # Clean up watcher
        watcher_task.cancel()
        try:
            await watcher_task
        except asyncio.CancelledError:
            pass


@pytest.mark.slow
@pytest.mark.anyio
async def test_output_watcher_handles_broadcast_errors(tmp_path: Path) -> None:
    """Test OUTPUT watcher continues watching after broadcast errors."""
    # Setup
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Create a mock broadcast callback that fails first time
    call_count = 0
    broadcast_events: list[asyncio.Event] = [asyncio.Event(), asyncio.Event()]

    def broadcast_callback() -> None:
        nonlocal call_count
        if call_count == 0:
            call_count += 1
            broadcast_events[0].set()
            raise RuntimeError("Simulated broadcast failure")
        else:
            call_count += 1
            broadcast_events[1].set()

    # Start watcher in background
    watcher_task = asyncio.create_task(
        watch_output_directory(
            output_dir=output_dir,
            broadcast_callback=broadcast_callback,
        )
    )

    try:
        # Give watcher time to start
        await asyncio.sleep(0.5)

        # Create first file (will trigger error)
        test_file1 = output_dir / "file1.html"
        test_file1.write_text("<html>1</html>")

        # Wait for first broadcast attempt
        try:
            await asyncio.wait_for(broadcast_events[0].wait(), timeout=3.0)
        except asyncio.TimeoutError:
            pytest.fail("First broadcast callback was not called")

        # Give debounce time to pass
        await asyncio.sleep(0.5)

        # Create second file (should succeed)
        test_file2 = output_dir / "file2.html"
        test_file2.write_text("<html>2</html>")

        # Wait for second broadcast attempt
        try:
            await asyncio.wait_for(broadcast_events[1].wait(), timeout=3.0)
        except asyncio.TimeoutError:
            pytest.fail("Second broadcast callback was not called")

        # Verify both callbacks were called
        assert call_count == 2

    finally:
        # Clean up watcher
        watcher_task.cancel()
        try:
            await watcher_task
        except asyncio.CancelledError:
            pass
