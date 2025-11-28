"""Path calculation utilities for static assets."""

from pathlib import Path
from typing import Literal

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


def calculate_relative_static_path(
    asset_path: str,
    page_depth: int,
    source_type: Literal["storytime", "input_dir"],
) -> str:
    """Calculate a relative path to a static asset based on page depth.

    Takes an asset reference like "static/nav.css" or "storytime_static/nav.css"
    and calculates the appropriate relative path based on the page's depth in
    the site hierarchy.

    Args:
        asset_path: The asset path to rewrite (e.g., "static/components/nav/static/nav.css")
        page_depth: The depth of the page in the site hierarchy
            - 0: Site root or section index
            - 1: Subject index
            - 2: Story page
        source_type: Whether the asset is from "storytime" or "input_dir"

    Returns:
        Relative path with appropriate "../" prefixes

    Example:
        >>> calculate_relative_static_path("static/components/nav/static/nav.css", 2, "input_dir")
        '../../../static/components/nav/static/nav.css'
        >>> calculate_relative_static_path("storytime_static/layout/static/style.css", 1, "storytime")
        '../../storytime_static/layout/static/style.css'

    Note:
        Depth calculation follows the same pattern as Layout component:
        - depth=0: ../static/ or ../storytime_static/
        - depth=1: ../../static/ or ../../storytime_static/
        - depth=2: ../../../static/ or ../../../storytime_static/
    """
    # Calculate the relative prefix (number of "../" segments)
    relative_prefix = "../" * (page_depth + 1)

    # Return the complete relative path
    return f"{relative_prefix}{asset_path}"
