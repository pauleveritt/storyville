"""Static assets management for Storytime.

This module provides utilities for discovering, copying, and managing static assets
from both storytime core components and input directories.
"""

from pathlib import Path

from storytime.static_assets.copying import copy_static_folder
from storytime.static_assets.discovery import discover_static_folders
from storytime.static_assets.models import StaticFolder
from storytime.static_assets.paths import calculate_relative_static_path
from storytime.static_assets.rewriting import (
    build_discovered_assets_map,
    rewrite_static_paths,
)
from storytime.static_assets.validation import validate_no_collisions

__all__ = [
    "StaticFolder",
    "build_discovered_assets_map",
    "calculate_relative_static_path",
    "copy_all_static_assets",
    "copy_static_folder",
    "discover_static_folders",
    "rewrite_static_paths",
    "validate_no_collisions",
]


def copy_all_static_assets(
    storytime_base: Path, input_dir: Path, output_dir: Path
) -> int:
    """Discover and copy all static assets to a single static/ directory.

    Simplified approach: All static folders (from storytime and input_dir)
    copy their contents into output_dir/static/. Collisions are acceptable.

    Args:
        storytime_base: Path to storytime installation (e.g., src/storytime)
        input_dir: Path to user's input directory
        output_dir: Path to output directory for built site

    Returns:
        Number of static files copied

    Example:
        >>> from pathlib import Path
        >>> count = copy_all_static_assets(
        ...     Path("src/storytime"),
        ...     Path("examples/minimal"),
        ...     Path("output")
        ... )
        >>> print(f"Copied {count} static files")
    """
    import shutil

    # Create single static output directory
    static_out = output_dir / "static"
    static_out.mkdir(parents=True, exist_ok=True)

    # Discover from both sources
    storytime_folders = discover_static_folders(storytime_base, "storytime")
    input_folders = discover_static_folders(input_dir, "input_dir")

    # Copy all files to single static/ directory
    file_count = 0
    for static_folder in storytime_folders + input_folders:
        for file_path in static_folder.source_path.rglob("*"):
            if file_path.is_file():
                shutil.copy2(file_path, static_out / file_path.name)
                file_count += 1

    return file_count
