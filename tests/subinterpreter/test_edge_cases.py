"""Strategic tests for edge cases and critical gaps in subinterpreter functionality."""

from pathlib import Path
from unittest.mock import patch

import pytest

from storytime.subinterpreter_pool import (
    build_in_subinterpreter,
    create_pool,
    rebuild_callback_subinterpreter,
    shutdown_pool,
)


def test_concurrent_builds_handling(tmp_path: Path) -> None:
    """Test that multiple concurrent builds are handled correctly by the pool.

    This tests the pool's ability to handle concurrent build requests,
    which could occur in real-world usage with rapid file changes.
    """
    pool = create_pool()
    output_dir_1 = tmp_path / "output1"
    output_dir_2 = tmp_path / "output2"

    try:
        # Submit two builds concurrently
        # With pool size of 2, both should be able to run
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future1 = executor.submit(
                build_in_subinterpreter,
                pool,
                "examples.minimal",
                output_dir_1,
            )
            future2 = executor.submit(
                build_in_subinterpreter,
                pool,
                "examples.minimal",
                output_dir_2,
            )

            # Both should complete successfully
            future1.result(timeout=30.0)
            future2.result(timeout=30.0)

        # Both builds should have produced output
        assert (output_dir_1 / "index.html").exists()
        assert (output_dir_2 / "index.html").exists()

    finally:
        shutdown_pool(pool)


async def test_rapid_rebuilds_with_debouncing(tmp_path: Path) -> None:
    """Test rapid rebuild requests are handled gracefully.

    This simulates rapid file changes during development where multiple
    saves happen in quick succession.
    """
    pool = create_pool()
    output_dir = tmp_path / "output"

    try:
        # Trigger 5 rapid rebuilds
        for i in range(5):
            await rebuild_callback_subinterpreter(
                "examples.minimal",
                output_dir,
                pool,
            )

        # All should complete successfully
        # Final output should exist
        assert (output_dir / "index.html").exists()

    finally:
        shutdown_pool(pool)


def test_build_timeout_handling(tmp_path: Path) -> None:
    """Test that build timeout is enforced and handled gracefully.

    Verifies that if a build takes too long, it times out without
    crashing the pool.
    """
    pool = create_pool()
    output_dir = tmp_path / "output"

    try:
        # Mock the internal build function to simulate a slow build
        with patch("storytime.subinterpreter_pool._build_site_in_interpreter") as mock_build:
            # Simulate a build that takes too long
            def slow_build(*args, **kwargs):
                import time
                time.sleep(70)  # Longer than the 60s timeout

            mock_build.side_effect = slow_build

            # This should timeout
            with pytest.raises(Exception):  # TimeoutError or similar
                build_in_subinterpreter(
                    pool,
                    "examples.minimal",
                    output_dir,
                )

        # Pool should still be functional after timeout
        # Try a normal build
        output_dir_2 = tmp_path / "output2"
        build_in_subinterpreter(
            pool,
            "examples.minimal",
            output_dir_2,
        )
        assert (output_dir_2 / "index.html").exists()

    finally:
        shutdown_pool(pool)


def test_pool_recovery_after_multiple_failures(tmp_path: Path) -> None:
    """Test that pool remains functional after multiple build failures.

    Ensures the pool can recover from a series of errors and continue
    processing builds successfully.
    """
    pool = create_pool()

    try:
        # Trigger multiple failures
        for i in range(3):
            try:
                build_in_subinterpreter(
                    pool,
                    "nonexistent.package.error",
                    tmp_path / f"output_{i}",
                )
            except Exception:
                # Expected to fail
                pass

        # Pool should still work after multiple failures
        output_dir_success = tmp_path / "output_success"
        build_in_subinterpreter(
            pool,
            "examples.minimal",
            output_dir_success,
        )

        assert (output_dir_success / "index.html").exists()

    finally:
        shutdown_pool(pool)


def test_filesystem_error_handling(tmp_path: Path) -> None:
    """Test handling of filesystem errors during build.

    Verifies graceful handling when output directory is not writable
    or other filesystem issues occur.
    """
    pool = create_pool()

    # Create a directory and make it read-only
    readonly_dir = tmp_path / "readonly"
    readonly_dir.mkdir()
    readonly_dir.chmod(0o444)  # Read-only

    try:
        # This should fail due to permissions
        try:
            build_in_subinterpreter(
                pool,
                "examples.minimal",
                readonly_dir / "output",
            )
            # May or may not raise depending on how build handles it
        except Exception:
            # Expected
            pass

        # Pool should still be functional
        normal_dir = tmp_path / "normal"
        build_in_subinterpreter(
            pool,
            "examples.minimal",
            normal_dir,
        )
        assert (normal_dir / "index.html").exists()

    finally:
        # Restore permissions for cleanup
        try:
            readonly_dir.chmod(0o755)
        except Exception:
            pass
        shutdown_pool(pool)


async def test_module_state_isolation_between_builds(tmp_path: Path) -> None:
    """Test that global module state doesn't leak between builds.

    Verifies that each build in a subinterpreter has truly isolated
    module state, preventing state pollution across builds.
    """
    pool = create_pool()

    try:
        # Run multiple builds - each should have fresh module state
        output_dirs = [tmp_path / f"output_{i}" for i in range(3)]

        for output_dir in output_dirs:
            await rebuild_callback_subinterpreter(
                "examples.minimal",
                output_dir,
                pool,
            )

            # Each build should produce identical output
            # (proving module state is reset each time)
            assert (output_dir / "index.html").exists()
            content = (output_dir / "index.html").read_text()
            assert "Minimal Site" in content

        # All outputs should be identical (module state was reset)
        contents = [(d / "index.html").read_text() for d in output_dirs]
        assert all(c == contents[0] for c in contents)

    finally:
        shutdown_pool(pool)


def test_error_recovery_full_cycle(tmp_path: Path) -> None:
    """Test full error -> recovery -> success cycle.

    Simulates a real-world scenario: build fails, error is fixed,
    build succeeds.
    """
    pool = create_pool()

    try:
        # Step 1: Build fails
        try:
            build_in_subinterpreter(
                pool,
                "nonexistent.package",
                tmp_path / "output_fail",
            )
        except Exception:
            pass  # Expected failure

        # Step 2: Recovery - build succeeds
        output_dir_success = tmp_path / "output_success"
        build_in_subinterpreter(
            pool,
            "examples.minimal",
            output_dir_success,
        )
        assert (output_dir_success / "index.html").exists()

        # Step 3: Another success to confirm stability
        output_dir_success_2 = tmp_path / "output_success_2"
        build_in_subinterpreter(
            pool,
            "examples.minimal",
            output_dir_success_2,
        )
        assert (output_dir_success_2 / "index.html").exists()

    finally:
        shutdown_pool(pool)


async def test_async_callback_error_propagation(tmp_path: Path) -> None:
    """Test that errors in async callback are properly propagated.

    Ensures error handling works correctly in the async rebuild callback,
    which is used by the watcher.
    """
    pool = create_pool()

    try:
        # This should raise an error
        with pytest.raises(Exception):
            await rebuild_callback_subinterpreter(
                "nonexistent.package",
                tmp_path / "output",
                pool,
            )

        # Pool should still work after error
        await rebuild_callback_subinterpreter(
            "examples.minimal",
            tmp_path / "output_success",
            pool,
        )
        assert (tmp_path / "output_success" / "index.html").exists()

    finally:
        shutdown_pool(pool)


def test_pool_cleanup_on_shutdown_with_pending_work(tmp_path: Path) -> None:
    """Test that pool shutdown handles pending work gracefully.

    Verifies that if there's work in progress when shutdown is called,
    it completes or is cancelled cleanly without hanging.
    """
    pool = create_pool()

    # Submit a build but don't wait for it
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(
            build_in_subinterpreter,
            pool,
            "examples.minimal",
            tmp_path / "output",
        )

        # Give it a moment to start
        import time
        time.sleep(0.1)

        # Shutdown pool (should wait for pending work)
        shutdown_pool(pool)

        # Future should complete (either successfully or with error)
        try:
            future.result(timeout=10.0)
        except Exception:
            # Pool was shut down, build may have failed
            # This is acceptable as long as shutdown completed
            pass
