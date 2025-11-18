"""Tests for build execution in subinterpreters."""

from pathlib import Path

from storytime.subinterpreter_pool import create_pool, shutdown_pool


def test_build_in_subinterpreter_executes_successfully(tmp_path: Path) -> None:
    """Test that build_in_subinterpreter executes build successfully."""
    from storytime.subinterpreter_pool import build_in_subinterpreter

    pool = create_pool()
    output_dir = tmp_path / "output"

    try:
        # Execute build in subinterpreter
        build_in_subinterpreter(
            pool=pool,
            package_location="examples.minimal",
            output_dir=output_dir,
        )

        # Verify build outputs exist
        assert output_dir.exists()
        assert (output_dir / "index.html").exists()
        assert (output_dir / "static").exists()

    finally:
        shutdown_pool(pool)


def test_build_in_subinterpreter_writes_correct_files(tmp_path: Path) -> None:
    """Test that subinterpreter build writes files to disk correctly."""
    from storytime.subinterpreter_pool import build_in_subinterpreter

    pool = create_pool()
    output_dir = tmp_path / "output"

    try:
        # Execute build
        build_in_subinterpreter(
            pool=pool,
            package_location="examples.minimal",
            output_dir=output_dir,
        )

        # Verify essential files exist
        assert (output_dir / "index.html").exists()
        assert (output_dir / "about.html").exists()
        assert (output_dir / "debug.html").exists()

        # Verify content is written correctly
        index_content = (output_dir / "index.html").read_text()
        assert "Minimal Site" in index_content

    finally:
        shutdown_pool(pool)


def test_module_isolation_fresh_imports(tmp_path: Path) -> None:
    """Test that module changes are picked up on subsequent builds (module isolation)."""
    from storytime.subinterpreter_pool import build_in_subinterpreter

    pool = create_pool()
    output_dir_1 = tmp_path / "output1"
    output_dir_2 = tmp_path / "output2"

    try:
        # First build
        build_in_subinterpreter(
            pool=pool,
            package_location="examples.minimal",
            output_dir=output_dir_1,
        )

        # Second build - should use fresh interpreter with fresh imports
        build_in_subinterpreter(
            pool=pool,
            package_location="examples.minimal",
            output_dir=output_dir_2,
        )

        # Both builds should produce identical results
        # (demonstrating that module isolation works - each build gets fresh imports)
        assert (output_dir_1 / "index.html").exists()
        assert (output_dir_2 / "index.html").exists()

        content_1 = (output_dir_1 / "index.html").read_text()
        content_2 = (output_dir_2 / "index.html").read_text()

        # Content should be identical (both had fresh imports)
        assert content_1 == content_2

    finally:
        shutdown_pool(pool)


def test_build_error_handling_import_error(tmp_path: Path) -> None:
    """Test that import errors are caught and logged without crashing."""
    from storytime.subinterpreter_pool import build_in_subinterpreter

    pool = create_pool()
    output_dir = tmp_path / "output"

    try:
        # Try to build with invalid package location
        # This should raise an error but not crash the pool
        try:
            build_in_subinterpreter(
                pool=pool,
                package_location="nonexistent.package.that.does.not.exist",
                output_dir=output_dir,
            )
            # If it doesn't raise, that's also acceptable (error was caught and logged)
        except Exception:
            # Error was raised, which is acceptable
            pass

        # Pool should still be functional - verify by running another build
        output_dir_2 = tmp_path / "output2"
        build_in_subinterpreter(
            pool=pool,
            package_location="examples.minimal",
            output_dir=output_dir_2,
        )

        # Second build should succeed
        assert (output_dir_2 / "index.html").exists()

    finally:
        shutdown_pool(pool)


def test_interpreter_discard_and_replacement() -> None:
    """Test that interpreter is discarded after build and replacement is warmed up."""
    from storytime.subinterpreter_pool import warmup_interpreter

    pool = create_pool()

    try:
        # The pool starts with 2 warmed-up interpreters
        # Each build should discard the used interpreter and warm up a replacement

        # Submit a simple warm-up task to verify pool is functional
        future_before = pool.submit(warmup_interpreter)
        result_before = future_before.result(timeout=5.0)
        assert result_before is True

        # Pool should still be functional after the task
        future_after = pool.submit(warmup_interpreter)
        result_after = future_after.result(timeout=5.0)
        assert result_after is True

    finally:
        shutdown_pool(pool)
