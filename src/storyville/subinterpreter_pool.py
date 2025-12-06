"""Subinterpreter pool management for hot reloading.

This module provides functionality to create and manage a pool of Python
subinterpreters using InterpreterPoolExecutor. Subinterpreters allow fresh
module imports on each build, enabling true hot reloading of stories.py files.
"""

import asyncio
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
        - storyville: Core framework module
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
        # Pre-import storyville module
        import storyville  # noqa: F401

        # Pre-import tdom module
        import tdom  # noqa: F401

        logger.info("Interpreter warm-up completed successfully")
        return True

    except ImportError as e:
        logger.error(f"Warm-up import failed: {e}")
        return False


def _clear_user_modules(package_location: str) -> None:
    """Clear user package modules from sys.modules.

    This function removes all modules belonging to the user's package
    from sys.modules, ensuring fresh imports on the next build.

    Args:
        package_location: Package location string (e.g., "examples.basic")

    Note:
        This function must be called from within a subinterpreter.
        It preserves core modules (storyville, tdom) while clearing user modules.
    """
    import logging
    import sys

    logger = logging.getLogger(__name__)

    # Extract the top-level package name from package_location
    # e.g., "examples.basic" -> "examples"
    package_prefix = package_location.split(".")[0]

    # Find all modules that belong to the user's package
    modules_to_clear = [
        module_name
        for module_name in list(sys.modules.keys())
        if module_name.startswith(package_prefix + ".") or module_name == package_prefix
    ]

    # Clear the modules
    for module_name in modules_to_clear:
        del sys.modules[module_name]

    if modules_to_clear:
        logger.info(
            f"Cleared {len(modules_to_clear)} user modules from sys.modules: {package_prefix}.*"
        )
    else:
        logger.info(f"No cached modules found for {package_prefix}.*")


def _build_site_in_interpreter(
    package_location: str,
    output_dir_str: str,
    sys_path: list[str],
    with_assertions: bool = True,
) -> None:
    """Execute build_site in a subinterpreter.

    This function is designed to be submitted to an InterpreterPoolExecutor.
    It imports build_site and executes it, allowing fresh module imports
    each time it runs in a new subinterpreter.

    Args:
        package_location: Package location to build from
        output_dir_str: Output directory path as string (Path objects can't cross interpreter boundary)
        sys_path: Python sys.path to use in the subinterpreter
        with_assertions: Whether to enable assertions during rendering (default: True)

    Note:
        This function runs inside a subinterpreter and writes directly to disk.
        User package modules are cleared from sys.modules BEFORE the build to ensure
        fresh imports, since the pool reuses interpreters and a different interpreter
        might be used for each build.
    """
    import logging
    import os
    import sys
    from pathlib import Path

    # Set up sys.path in the subinterpreter to match the main interpreter
    sys.path.clear()
    sys.path.extend(sys_path)

    logger = logging.getLogger(__name__)

    # Log which interpreter we're in (for debugging)
    logger.info(f"Running in subinterpreter (PID: {os.getpid()})")

    # IMPORTANT: Clear user modules BEFORE building
    # This ensures fresh imports even if this interpreter was previously used
    # Since the pool has multiple interpreters, we can't rely on clearing after build
    _clear_user_modules(package_location)

    try:
        # Import build_site fresh in this subinterpreter
        from storyville.build import build_site

        # Convert string path back to Path object
        output_dir = Path(output_dir_str)

        logger.info(
            f"Starting build in subinterpreter: {package_location} -> {output_dir}"
        )

        # Execute the build - this will have fresh imports of all modules
        build_site(
            package_location=package_location,
            output_dir=output_dir,
            with_assertions=with_assertions,
        )

        logger.info("Build in subinterpreter completed successfully")

    except Exception as e:
        logger.error(f"Build in subinterpreter failed: {e}", exc_info=True)
        raise


def build_in_subinterpreter(
    pool: InterpreterPoolExecutor,
    package_location: str,
    output_dir: Path,
    with_assertions: bool = True,
) -> None:
    """Execute a build in a subinterpreter with module isolation.

    This function:
    1. Submits the build task to the interpreter pool
    2. The subinterpreter clears user modules before building (fresh imports)
    3. Waits for completion

    Args:
        pool: The InterpreterPoolExecutor to use
        package_location: Package location to build from
        output_dir: Output directory to write the built site to
        with_assertions: Whether to enable assertions during rendering (default: True)

    Raises:
        Exception: If build fails in the subinterpreter

    Note:
        User package modules are cleared from sys.modules BEFORE each build
        to ensure fresh imports. This handles the case where different interpreters
        from the pool are used for consecutive builds. Core modules (storyville, tdom)
        remain cached for performance across builds in the same interpreter.
    """
    logger.info(
        f"Submitting build to subinterpreter pool: {package_location} -> {output_dir}"
    )

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
            with_assertions,
        )
        future.result(timeout=60.0)  # 60 second timeout for build

        logger.info("Build in subinterpreter completed successfully")

    except Exception as e:
        logger.error(f"Build in subinterpreter failed: {e}", exc_info=True)
        # Re-raise to allow caller to handle the error
        raise


async def rebuild_callback_subinterpreter(
    package_location: str,
    output_dir: Path,
    pool: InterpreterPoolExecutor,
    with_assertions: bool = True,
) -> None:
    """Async callback for rebuilding using subinterpreters.

    This function is designed to be used as a rebuild callback for the watcher.
    It runs the synchronous build_in_subinterpreter() function in a thread pool
    to avoid blocking the async event loop.

    Args:
        package_location: Package location to build from
        output_dir: Output directory to write the built site to
        pool: The InterpreterPoolExecutor to use for building
        with_assertions: Whether to enable assertions during rendering (default: True)

    Raises:
        Exception: If build fails in the subinterpreter

    Note:
        This uses asyncio.to_thread() to run the synchronous subinterpreter
        build without blocking the event loop. Error handling is delegated
        to build_in_subinterpreter().
    """
    logger.info(f"Async rebuild callback: {package_location} -> {output_dir}")

    try:
        # Run synchronous build_in_subinterpreter in thread pool
        await asyncio.to_thread(
            build_in_subinterpreter,
            pool,
            package_location,
            output_dir,
            with_assertions,
        )

        logger.info("Async rebuild callback completed successfully")

    except Exception as e:
        logger.error(f"Async rebuild callback failed: {e}", exc_info=True)
        # Re-raise to allow watcher to handle the error
        raise


def create_pool() -> InterpreterPoolExecutor:
    """Create a pool of subinterpreters for running builds.

    Creates an InterpreterPoolExecutor with a pool size of 2 interpreters.
    The interpreters start clean with no pre-imported modules to ensure
    complete module isolation.

    Returns:
        InterpreterPoolExecutor: The created pool with 2 clean interpreters

    Note:
        The pool should be shut down using shutdown_pool() when no longer needed.
    """
    pool_size = 2

    logger.info(f"Creating interpreter pool with size={pool_size}")

    # Create the pool with exactly 2 interpreters
    # No warmup - start with completely clean interpreters for guaranteed fresh imports
    pool = InterpreterPoolExecutor(max_workers=pool_size)

    logger.info(f"Interpreter pool created with {pool_size} clean interpreters")

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
