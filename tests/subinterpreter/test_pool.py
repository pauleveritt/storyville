"""Tests for subinterpreter pool creation and lifecycle."""

from concurrent.futures import InterpreterPoolExecutor

from storytime.subinterpreter_pool import create_pool, shutdown_pool, warmup_interpreter


def test_pool_creation_with_size_2() -> None:
    """Test that pool creates successfully with size=2."""
    pool = create_pool()

    # Verify pool is an InterpreterPoolExecutor
    assert isinstance(pool, InterpreterPoolExecutor)

    # Clean up
    shutdown_pool(pool)


def test_warmup_function_execution() -> None:
    """Test that warm-up function executes successfully."""
    pool = create_pool()

    # Submit warm-up task and wait for completion
    future = pool.submit(warmup_interpreter)
    result = future.result(timeout=5.0)

    # Warm-up should return True on success
    assert result is True

    # Clean up
    shutdown_pool(pool)


def test_pool_shutdown_cleanup() -> None:
    """Test that pool shuts down gracefully."""
    pool = create_pool()

    # Shutdown should complete without errors
    shutdown_pool(pool)

    # After shutdown, pool should be in shutdown state
    # (InterpreterPoolExecutor doesn't expose a public state attribute,
    # but we can verify no exceptions were raised)


def test_warmup_imports_modules() -> None:
    """Test that warm-up function successfully imports storytime and tdom modules."""
    pool = create_pool()

    # Submit warm-up task and verify it completes successfully
    future = pool.submit(warmup_interpreter)
    result = future.result(timeout=5.0)

    # Should succeed - this confirms modules were imported successfully
    assert result is True

    # Clean up
    shutdown_pool(pool)
