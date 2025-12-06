"""Validation utilities for static asset management."""

from storyville.static_assets.models import StaticFolder


def validate_no_collisions(static_folders: list[StaticFolder]) -> None:
    """Validate that there are no output path collisions between static folders.

    This function checks that no two static folders would be copied to the same
    output location. Due to path preservation and source type disambiguation
    (storyville_static/ vs static/), collisions should never happen in practice.
    However, this validation provides a safety check and helpful error messages.

    Args:
        static_folders: List of StaticFolder instances to validate

    Raises:
        ValueError: If a collision is detected between two folders

    Example:
        >>> from pathlib import Path
        >>> from storyville.static_assets.models import StaticFolder
        >>> folders = [
        ...     StaticFolder(Path("a/static"), "storyville", Path("a")),
        ...     StaticFolder(Path("b/static"), "input_dir", Path("b")),
        ... ]
        >>> validate_no_collisions(folders)  # No collision - different prefixes

    Note:
        - Collisions are virtually impossible due to:
          1. Full path preservation (components/nav vs components/button)
          2. Source type disambiguation (storyville_static/ vs static/)
        - This function is defensive programming for unexpected edge cases
    """
    # Build a map of output paths to source paths for collision detection
    output_paths: dict[str, StaticFolder] = {}

    for static_folder in static_folders:
        # Use a temporary output_dir just for comparison
        # We use str() for consistent comparison
        output_key = f"{static_folder.output_prefix}/{static_folder.relative_path}/static"

        # Check if this output path already exists
        if output_key in output_paths:
            existing_folder = output_paths[output_key]
            error_msg = (
                f"Static folder collision detected:\n"
                f"  Folder 1: {existing_folder.source_path} "
                f"(type: {existing_folder.source_type})\n"
                f"  Folder 2: {static_folder.source_path} "
                f"(type: {static_folder.source_type})\n"
                f"  Both would copy to: {output_key}\n"
                f"This should not happen due to path preservation. "
                f"Please report this issue."
            )
            raise ValueError(error_msg)

        # Record this output path
        output_paths[output_key] = static_folder
