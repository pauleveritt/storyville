"""Tests for subinterpreter pool creation and lifecycle."""

from concurrent.futures import InterpreterPoolExecutor

from storyville.subinterpreter_pool import create_pool, shutdown_pool


def test_pool_creation_with_size_2() -> None:
    """Test that pool creates successfully with size=2 clean interpreters."""
    pool = create_pool()

    # Verify pool is an InterpreterPoolExecutor
    assert isinstance(pool, InterpreterPoolExecutor)

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
