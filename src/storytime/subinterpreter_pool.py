"""Subinterpreter pool management for hot reloading.

This module provides functionality to create and manage a pool of Python
subinterpreters using InterpreterPoolExecutor. Subinterpreters allow fresh
module imports on each build, enabling true hot reloading of stories.py files.
"""

import logging
from concurrent.futures import InterpreterPoolExecutor

logger = logging.getLogger(__name__)


def warmup_interpreter() -> bool:
    """Warm up a subinterpreter by pre-importing common modules.

    This function is designed to be submitted to an InterpreterPoolExecutor
    to pre-load commonly used modules, reducing build latency.

    Imports:
        - storytime: Core framework module
        - tdom: Template rendering module

    Returns:
        bool: True if warm-up completed successfully, False on error

    Note:
        This is a module-level callable compatible with InterpreterPoolExecutor.
        Import errors are logged but don't cause the warm-up to fail completely.
    """
    import logging

    logger = logging.getLogger(__name__)

    try:
        # Pre-import storytime module
        import storytime  # noqa: F401

        # Pre-import tdom module
        import tdom  # noqa: F401

        logger.info("Interpreter warm-up completed successfully")
        return True

    except ImportError as e:
        logger.error(f"Warm-up import failed: {e}")
        return False


def create_pool() -> InterpreterPoolExecutor:
    """Create a pool of subinterpreters for running builds.

    Creates an InterpreterPoolExecutor with a pool size of 2 interpreters.
    Both interpreters are immediately warmed up by importing common modules.

    Returns:
        InterpreterPoolExecutor: The created pool with 2 interpreters

    Note:
        The pool should be shut down using shutdown_pool() when no longer needed.
    """
    pool_size = 2

    logger.info(f"Creating interpreter pool with size={pool_size}")

    # Create the pool with exactly 2 interpreters
    pool = InterpreterPoolExecutor(max_workers=pool_size)

    # Warm up both interpreters immediately
    futures = [pool.submit(warmup_interpreter) for _ in range(pool_size)]

    # Wait for warm-up to complete
    for future in futures:
        try:
            future.result(timeout=10.0)
        except Exception as e:
            logger.error(f"Interpreter warm-up failed: {e}")

    logger.info(f"Interpreter pool created with {pool_size} interpreters")

    return pool


def shutdown_pool(pool: InterpreterPoolExecutor) -> None:
    """Gracefully shutdown the interpreter pool.

    Args:
        pool: The InterpreterPoolExecutor to shut down

    Note:
        This function handles shutdown errors gracefully and logs completion.
    """
    logger.info("Shutting down interpreter pool")

    try:
        # Shutdown the pool, waiting for pending tasks to complete
        pool.shutdown(wait=True, cancel_futures=False)
        logger.info("Interpreter pool shutdown completed")

    except Exception as e:
        logger.error(f"Error during pool shutdown: {e}")
