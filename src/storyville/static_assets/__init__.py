"""Static assets management for Storyville.

This module provides utilities for discovering, copying, and managing static assets
from both storyville core components and input directories.
"""

from pathlib import Path

from storyville.static_assets.copying import copy_static_folder
from storyville.static_assets.discovery import discover_static_folders
from storyville.static_assets.models import StaticFolder
from storyville.static_assets.paths import calculate_relative_static_path
from storyville.static_assets.rewriting import (
    build_discovered_assets_map,
    rewrite_static_paths,
)
from storyville.static_assets.validation import validate_no_collisions

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
    storyville_base: Path, input_dir: Path, output_dir: Path
) -> int:
    """Discover and copy all static assets to a single static/ directory.

    Simplified approach: All static folders (from storyville and input_dir)
    copy their contents into output_dir/static/, preserving the relative path
    from the base directory. Collisions are acceptable.

    Args:
        storyville_base: Path to storyville installation (e.g., src/storyville)
        input_dir: Path to user's input directory
        output_dir: Path to output directory for built site

    Returns:
        Number of static files copied

    Example:
        >>> from pathlib import Path
        >>> count = copy_all_static_assets(
        ...     Path("src/storyville"),
        ...     Path("examples/minimal"),
        ...     Path("output")
        ... )
        >>> print(f"Copied {count} static files")

    Note:
        Files are copied with their relative path preserved:
        - src/storyville/components/layout/static/pico.css
          -> output/static/components/layout/static/pico.css
    """
    import shutil

    # Create single static output directory
    static_out = output_dir / "static"
    static_out.mkdir(parents=True, exist_ok=True)

    # Discover from both sources
    storyville_folders = discover_static_folders(storyville_base, "storyville")
    input_folders = discover_static_folders(input_dir, "input_dir")

    # Copy all files to single static/ directory, preserving relative paths
    file_count = 0
    for static_folder in storyville_folders + input_folders:
        # Get the base path for this source type
        base_path = (
            storyville_base if static_folder.source_type == "storyville" else input_dir
        )

        for file_path in static_folder.source_path.rglob("*"):
            if file_path.is_file():
                # Calculate relative path from base directory
                relative_file = file_path.relative_to(base_path)
                dest_path = static_out / relative_file

                # Create parent directories if needed
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                # Copy the file
                shutil.copy2(file_path, dest_path)
                file_count += 1

    return file_count
