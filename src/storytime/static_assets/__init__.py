"""Static assets management for Storytime.

This module provides utilities for discovering, copying, and managing static assets
from both storytime core components and input directories.
"""

from pathlib import Path

from storytime.static_assets.copying import copy_static_folder
from storytime.static_assets.discovery import discover_static_folders
from storytime.static_assets.models import StaticFolder
from storytime.static_assets.validation import validate_no_collisions

__all__ = [
    "StaticFolder",
    "copy_all_static_assets",
    "copy_static_folder",
    "discover_static_folders",
    "validate_no_collisions",
]


def copy_all_static_assets(
    storytime_base: Path, input_dir: Path, output_dir: Path
) -> list[Path]:
    """Discover and copy all static assets from both sources to output directory.

    This function:
    1. Discovers static folders from storytime core (src/storytime)
    2. Discovers static folders from input directory
    3. Validates for collisions (should never happen due to path preservation)
    4. Copies all discovered static folders to appropriate output locations
    5. Returns list of output paths for verification

    Args:
        storytime_base: Path to storytime installation (e.g., src/storytime)
        input_dir: Path to user's input directory
        output_dir: Path to output directory for built site

    Returns:
        List of output paths where static folders were copied

    Example:
        >>> from pathlib import Path
        >>> output_paths = copy_all_static_assets(
        ...     Path("src/storytime"),
        ...     Path("examples/minimal"),
        ...     Path("output")
        ... )
        >>> print(output_paths)
        [Path('output/storytime_static/...'), Path('output/static/...')]
    """
    # Discover from both sources
    storytime_folders = discover_static_folders(storytime_base, "storytime")
    input_folders = discover_static_folders(input_dir, "input_dir")

    # Combine all folders
    all_folders = storytime_folders + input_folders

    # Validate for collisions (should never happen but good to check)
    validate_no_collisions(all_folders)

    # Copy all folders and collect output paths
    output_paths: list[Path] = []
    for static_folder in all_folders:
        copy_static_folder(static_folder, output_dir)
        output_paths.append(static_folder.calculate_output_path(output_dir))

    return output_paths
