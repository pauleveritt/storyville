"""Path calculation utilities for static assets."""

from typing import Literal


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
