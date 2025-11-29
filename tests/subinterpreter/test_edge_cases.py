"""Strategic tests for edge cases and critical gaps in subinterpreter functionality."""

from pathlib import Path

import pytest

from storytime.subinterpreter_pool import (
    build_in_subinterpreter,
    create_pool,
    rebuild_callback_subinterpreter,
    shutdown_pool,
)


@pytest.mark.slow
def test_concurrent_builds_handling(tmp_path: Path) -> None:
    """Test multiple concurrent builds are handled correctly.

    Tests pool's ability to handle concurrent build requests and rapid
    file changes during development.
    """
    pool = create_pool()
    output_dir_1 = tmp_path / "output1"
    output_dir_2 = tmp_path / "output2"

    try:
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

            future1.result(timeout=30.0)
            future2.result(timeout=30.0)

        assert (output_dir_1 / "index.html").exists()
        assert (output_dir_2 / "index.html").exists()

    finally:
        shutdown_pool(pool)


@pytest.mark.slow
def test_pool_recovery_after_failures(tmp_path: Path) -> None:
    """Test pool remains functional after build failures.

    Verifies error recovery: build fails, pool recovers, build succeeds.
    """
    pool = create_pool()

    try:
        # Trigger failures
        for i in range(2):
            try:
                build_in_subinterpreter(
                    pool,
                    "nonexistent.package.error",
                    tmp_path / f"output_{i}",
                )
            except Exception:
                pass

        # Pool should still work
        output_dir_success = tmp_path / "output_success"
        build_in_subinterpreter(
            pool,
            "examples.minimal",
            output_dir_success,
        )

        assert (output_dir_success / "index.html").exists()

    finally:
        shutdown_pool(pool)


@pytest.mark.slow
def test_filesystem_error_handling(tmp_path: Path) -> None:
    """Test handling of filesystem errors during build.

    Verifies graceful handling when output directory has permission issues.
    """
    pool = create_pool()

    readonly_dir = tmp_path / "readonly"
    readonly_dir.mkdir()
    readonly_dir.chmod(0o444)

    try:
        try:
            build_in_subinterpreter(
                pool,
                "examples.minimal",
                readonly_dir / "output",
            )
        except Exception:
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
        try:
            readonly_dir.chmod(0o755)
        except Exception:
            pass
        shutdown_pool(pool)


@pytest.mark.slow
async def test_module_state_isolation_between_builds(tmp_path: Path) -> None:
    """Test global module state doesn't leak between builds.

    Verifies each build has isolated module state and async callback works.
    """
    pool = create_pool()

    try:
        output_dirs = [tmp_path / f"output_{i}" for i in range(3)]

        for output_dir in output_dirs:
            await rebuild_callback_subinterpreter(
                "examples.minimal",
                output_dir,
                pool,
            )

            assert (output_dir / "index.html").exists()
            content = (output_dir / "index.html").read_text()
            assert "Minimal Catalog" in content

        # All outputs should be identical (module state was reset)
        contents = [(d / "index.html").read_text() for d in output_dirs]
        assert all(c == contents[0] for c in contents)

    finally:
        shutdown_pool(pool)


@pytest.mark.slow
async def test_async_callback_error_propagation(tmp_path: Path) -> None:
    """Test errors in async callback are properly propagated.

    Ensures error handling works correctly in the async rebuild callback.
    """
    pool = create_pool()

    try:
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
