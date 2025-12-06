"""Static folder copying utilities."""

import logging
from pathlib import Path
from shutil import copytree

from storyville.static_assets.models import StaticFolder

logger = logging.getLogger(__name__)


def copy_static_folder(static_folder: StaticFolder, output_dir: Path) -> None:
    """Copy a static folder to the output directory.

    This function uses shutil.copytree to recursively copy all contents from the
    source static folder to the calculated output location. It creates parent
    directories as needed and handles existing directories gracefully.

    Args:
        static_folder: The StaticFolder instance to copy
        output_dir: The base output directory for the built site

    Raises:
        OSError: If copying fails due to permissions or disk issues
        ValueError: If source path doesn't exist

    Example:
        >>> from pathlib import Path
        >>> from storyville.static_assets.models import StaticFolder
        >>> folder = StaticFolder(
        ...     source_path=Path("src/storyville/components/nav/static"),
        ...     source_type="storyville",
        ...     relative_path=Path("components/nav")
        ... )
        >>> copy_static_folder(folder, Path("output"))
        # Copies contents to output/storyville_static/components/nav/static/

    Note:
        - Uses dirs_exist_ok=True to handle overlapping paths gracefully
        - Creates parent directories automatically
        - Preserves file permissions and metadata
        - Similar pattern to existing build.py copytree usage (lines 172-174)
    """
    # Validate source exists
    if not static_folder.source_path.exists():
        error_msg = (
            f"Source static folder does not exist: {static_folder.source_path}"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Calculate output path
    output_path = static_folder.calculate_output_path(output_dir)

    # Create parent directories if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Copy the entire static folder
    try:
        copytree(
            static_folder.source_path,
            output_path,
            dirs_exist_ok=True,
        )
        logger.debug(
            f"Copied static folder from {static_folder.source_path} "
            f"to {output_path}"
        )
    except OSError as e:
        error_msg = (
            f"Failed to copy static folder from {static_folder.source_path} "
            f"to {output_path}: {e}"
        )
        logger.error(error_msg)
        raise
