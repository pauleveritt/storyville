"""Integration tests for file watchers."""

import asyncio
from pathlib import Path

import pytest

from storyville.watchers import watch_and_rebuild


@pytest.mark.slow
@pytest.mark.anyio
async def test_input_watcher_detects_content_changes(tmp_path: Path) -> None:
    """Test unified watcher detects changes in content directory."""
    # Setup
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Create mock callbacks
    rebuild_called = asyncio.Event()
    rebuild_args: list[tuple[str, Path]] = []

    def rebuild_callback(package_location: str, output_dir_arg: Path) -> None:
        rebuild_args.append((package_location, output_dir_arg))
        rebuild_called.set()

    async def broadcast_callback() -> None:
        pass  # No-op for this test

    # Start watcher in background
    watcher_task = asyncio.create_task(
        watch_and_rebuild(
            content_path=content_dir,
            storyville_path=None,
            rebuild_callback=rebuild_callback,
            broadcast_callback=broadcast_callback,
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
    """Test unified watcher detects static asset changes in src/storyville/."""
    # Setup
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    storyville_dir = tmp_path / "storyville"
    storyville_dir.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Create mock callbacks
    rebuild_called = asyncio.Event()

    def rebuild_callback(package_location: str, output_dir_arg: Path) -> None:
        rebuild_called.set()

    async def broadcast_callback() -> None:
        pass  # No-op for this test

    # Start watcher in background
    watcher_task = asyncio.create_task(
        watch_and_rebuild(
            content_path=content_dir,
            storyville_path=storyville_dir,
            rebuild_callback=rebuild_callback,
            broadcast_callback=broadcast_callback,
            package_location="test_package",
            output_dir=output_dir,
        )
    )

    try:
        # Give watcher time to start
        await asyncio.sleep(0.5)

        # Create a CSS file in storyville directory
        static_dir = storyville_dir / "static"
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
async def test_input_watcher_ignores_python_files_in_storyville(tmp_path: Path) -> None:
    """Test unified watcher ignores Python files in src/storyville/."""
    # Setup
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    # Create dummy file to stabilize content directory
    (content_dir / ".gitkeep").write_text("")

    storyville_dir = tmp_path / "storyville"
    storyville_dir.mkdir()
    # Create dummy file to stabilize storyville directory
    (storyville_dir / ".gitkeep").write_text("")

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Create mock callbacks
    rebuild_called = asyncio.Event()

    def rebuild_callback(package_location: str, output_dir_arg: Path) -> None:
        rebuild_called.set()

    async def broadcast_callback() -> None:
        pass  # No-op for this test

    # Start watcher in background
    watcher_task = asyncio.create_task(
        watch_and_rebuild(
            content_path=content_dir,
            storyville_path=storyville_dir,
            rebuild_callback=rebuild_callback,
            broadcast_callback=broadcast_callback,
            package_location="test_package",
            output_dir=output_dir,
        )
    )

    try:
        # Give watcher time to start and process initial directory events
        await asyncio.sleep(1.0)

        # Clear any initial events that may have been triggered
        rebuild_called.clear()

        # Create a Python file in storyville directory (should be ignored)
        py_file = storyville_dir / "test.py"
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
async def test_watcher_can_be_started_and_stopped(tmp_path: Path) -> None:
    """Test unified watcher can be started and stopped cleanly."""
    # Setup
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Create mock callbacks
    def rebuild_callback(package_location: str, output_dir_arg: Path) -> None:
        pass

    async def broadcast_callback() -> None:
        pass

    # Start unified watcher
    watcher_task = asyncio.create_task(
        watch_and_rebuild(
            content_path=content_dir,
            storyville_path=None,
            rebuild_callback=rebuild_callback,
            broadcast_callback=broadcast_callback,
            package_location="test",
            output_dir=output_dir,
        )
    )

    # Give watcher time to start
    await asyncio.sleep(0.5)

    # Stop watcher
    watcher_task.cancel()

    # Verify task completes without errors
    try:
        await watcher_task
    except asyncio.CancelledError:
        pass  # Expected

    # If we get here without exception, watcher stopped cleanly
    assert True


@pytest.mark.slow
@pytest.mark.anyio
async def test_input_watcher_handles_rebuild_errors(tmp_path: Path) -> None:
    """Test unified watcher continues watching after rebuild errors."""
    # Setup
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Create mock callbacks - rebuild fails first time
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

    async def broadcast_callback() -> None:
        pass  # No-op for this test

    # Start watcher in background
    watcher_task = asyncio.create_task(
        watch_and_rebuild(
            content_path=content_dir,
            storyville_path=None,
            rebuild_callback=rebuild_callback,
            broadcast_callback=broadcast_callback,
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
async def test_unified_watcher_triggers_rebuild_and_broadcast(tmp_path: Path) -> None:
    """Test unified watcher detects changes, triggers rebuild, and broadcasts reload."""
    # Setup
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Create mock callbacks
    rebuild_called = asyncio.Event()
    broadcast_called = asyncio.Event()
    rebuild_args: list[tuple[str, Path]] = []

    def rebuild_callback(package_location: str, output_dir_arg: Path) -> None:
        rebuild_args.append((package_location, output_dir_arg))
        rebuild_called.set()

    async def broadcast_callback() -> None:
        broadcast_called.set()

    # Start unified watcher in background
    watcher_task = asyncio.create_task(
        watch_and_rebuild(
            content_path=content_dir,
            storyville_path=None,
            rebuild_callback=rebuild_callback,
            broadcast_callback=broadcast_callback,
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

        # Wait for broadcast to be called (with timeout)
        try:
            await asyncio.wait_for(broadcast_called.wait(), timeout=3.0)
        except asyncio.TimeoutError:
            pytest.fail("Broadcast callback was not called within timeout")

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
async def test_unified_watcher_does_not_broadcast_on_build_failure(tmp_path: Path) -> None:
    """Test unified watcher does not broadcast when rebuild fails."""
    # Setup
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Create mock callbacks - rebuild will fail
    rebuild_called = asyncio.Event()
    broadcast_called = asyncio.Event()

    def rebuild_callback(package_location: str, output_dir_arg: Path) -> None:
        rebuild_called.set()
        raise RuntimeError("Simulated build failure")

    async def broadcast_callback() -> None:
        broadcast_called.set()

    # Start unified watcher in background
    watcher_task = asyncio.create_task(
        watch_and_rebuild(
            content_path=content_dir,
            storyville_path=None,
            rebuild_callback=rebuild_callback,
            broadcast_callback=broadcast_callback,
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

        # Give time for broadcast to be called (if it would be)
        await asyncio.sleep(1.0)

        # Verify broadcast was NOT called (because rebuild failed)
        assert not broadcast_called.is_set()

    finally:
        # Clean up watcher
        watcher_task.cancel()
        try:
            await watcher_task
        except asyncio.CancelledError:
            pass
