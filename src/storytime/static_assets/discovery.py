"""Static folder discovery utilities."""

from pathlib import Path
from typing import Literal

from storytime.static_assets.models import StaticFolder


def discover_static_folders(
    base_path: Path, source_type: Literal["storytime", "input_dir"]
) -> list[StaticFolder]:
    """Discover all static folders recursively under the given base path.

    This function scans the directory tree starting from base_path and finds all
    directories named "static". For each discovered folder, it creates a StaticFolder
    instance with the necessary metadata for copying.

    The function uses Path.rglob("**/static") to recursively find all static
    directories, similar to how make_site scans for stories.py files.

    Args:
        base_path: The root directory to scan for static folders
        source_type: Whether scanning "storytime" core or "input_dir"

    Returns:
        List of StaticFolder instances representing discovered folders

    Example:
        >>> from pathlib import Path
        >>> folders = discover_static_folders(
        ...     Path("src/storytime"),
        ...     "storytime"
        ... )
        >>> len(folders) > 0
        True
        >>> folders[0].source_type
        'storytime'

    Note:
        - Only directories named exactly "static" are discovered
        - Empty static folders are included in the results
        - The relative_path preserves the full path structure for collision prevention
    """
    # Check if base_path exists
    if not base_path.exists():
        return []

    static_folders: list[StaticFolder] = []

    # Use rglob to find all directories named "static" recursively
    for static_path in base_path.rglob("static"):
        # Only process directories, not files named "static"
        if not static_path.is_dir():
            continue

        # Calculate the relative path from base to the parent of static/
        # This preserves the full directory structure
        parent_path = static_path.parent
        try:
            relative_path = parent_path.relative_to(base_path)
        except ValueError:
            # This shouldn't happen with rglob, but handle gracefully
            continue

        # Create StaticFolder instance
        static_folder = StaticFolder(
            source_path=static_path,
            source_type=source_type,
            relative_path=relative_path,
        )
        static_folders.append(static_folder)

    return static_folders
