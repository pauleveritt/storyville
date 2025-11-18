"""Subinterpreter pool management for hot reloading.

This module provides functionality to create and manage a pool of Python
subinterpreters using InterpreterPoolExecutor. Subinterpreters allow fresh
module imports on each build, enabling true hot reloading of stories.py files.
"""

import logging
import sys
from concurrent.futures import InterpreterPoolExecutor
from pathlib import Path

logger = logging.getLogger(__name__)

# Capture sys.path at module load time to pass to subinterpreters
_MAIN_SYS_PATH = sys.path.copy()


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


def _build_site_in_interpreter(
    package_location: str,
    output_dir_str: str,
    sys_path: list[str],
) -> None:
    """Execute build_site in a subinterpreter.

    This function is designed to be submitted to an InterpreterPoolExecutor.
    It imports build_site and executes it, allowing fresh module imports
    each time it runs in a new subinterpreter.

    Args:
        package_location: Package location to build from
        output_dir_str: Output directory path as string (Path objects can't cross interpreter boundary)
        sys_path: Python sys.path to use in the subinterpreter

    Note:
        This function runs inside a subinterpreter and writes directly to disk.
        Logging from within the subinterpreter will use the subinterpreter's
        logging configuration.
    """
    import logging
    import sys
    from pathlib import Path

    # Set up sys.path in the subinterpreter to match the main interpreter
    sys.path.clear()
    sys.path.extend(sys_path)

    logger = logging.getLogger(__name__)

    try:
        # Import build_site fresh in this subinterpreter
        from storytime.build import build_site

        # Convert string path back to Path object
        output_dir = Path(output_dir_str)

        logger.info(f"Starting build in subinterpreter: {package_location} -> {output_dir}")

        # Execute the build - this will have fresh imports of all modules
        build_site(package_location=package_location, output_dir=output_dir)

        logger.info("Build in subinterpreter completed successfully")

    except Exception as e:
        logger.error(f"Build in subinterpreter failed: {e}", exc_info=True)
        raise


def build_in_subinterpreter(
    pool: InterpreterPoolExecutor,
    package_location: str,
    output_dir: Path,
) -> None:
    """Execute a build in a subinterpreter with module isolation.

    This function:
    1. Submits the build task to the interpreter pool
    2. Waits for completion
    3. Discards the used interpreter (implicit via pool behavior)
    4. Warms up a replacement interpreter to maintain pool size

    Args:
        pool: The InterpreterPoolExecutor to use
        package_location: Package location to build from
        output_dir: Output directory to write the built site to

    Raises:
        Exception: If build fails in the subinterpreter

    Note:
        After each build, the used interpreter is discarded (implicit pool behavior)
        and a fresh interpreter is warmed up to maintain pool size of 2.
    """
    logger.info(f"Submitting build to subinterpreter pool: {package_location} -> {output_dir}")

    # Convert Path to string (Path objects can't cross interpreter boundary)
    output_dir_str = str(output_dir)

    try:
        # Submit build task to pool and wait for completion
        # Pass sys.path so subinterpreter can find all modules
        future = pool.submit(
            _build_site_in_interpreter,
            package_location,
            output_dir_str,
            _MAIN_SYS_PATH,
        )
        future.result(timeout=60.0)  # 60 second timeout for build

        logger.info("Build in subinterpreter completed successfully")

        # After build completes, warm up a replacement interpreter
        # This maintains pool size of 2 (one just used, one warming up)
        logger.info("Warming up replacement interpreter")
        warmup_future = pool.submit(warmup_interpreter)
        try:
            warmup_future.result(timeout=10.0)
            logger.info("Replacement interpreter warmed up successfully")
        except Exception as e:
            logger.error(f"Failed to warm up replacement interpreter: {e}")

    except Exception as e:
        logger.error(f"Build in subinterpreter failed: {e}", exc_info=True)
        # Re-raise to allow caller to handle the error
        raise


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
