"""Path calculation utilities for static assets."""

from pathlib import Path

from storytime.static_assets.models import StaticFolder


def calculate_output_path(static_folder: StaticFolder, output_dir: Path) -> Path:
    """Calculate the output path for a static folder.

    This is a convenience function that delegates to StaticFolder.calculate_output_path.
    The output path preserves the full directory structure including the final `/static/`
    directory and prepends the appropriate prefix (storytime_static/ or static/).

    Args:
        static_folder: The StaticFolder instance to calculate path for
        output_dir: The base output directory for the built site

    Returns:
        Full path where the static folder should be copied

    Example:
        >>> from pathlib import Path
        >>> from storytime.static_assets.models import StaticFolder
        >>> folder = StaticFolder(
        ...     source_path=Path("src/storytime/components/nav/static"),
        ...     source_type="storytime",
        ...     relative_path=Path("components/nav")
        ... )
        >>> output = calculate_output_path(folder, Path("output"))
        >>> str(output)
        'output/storytime_static/components/nav/static'

    Note:
        Path structure examples:
        - src/storytime/components/navigation_tree/static/nav.css
          → output_dir/storytime_static/components/navigation_tree/static/nav.css
        - input_dir/components/button/static/icon.svg
          → output_dir/static/components/button/static/icon.svg
    """
    return static_folder.calculate_output_path(output_dir)
