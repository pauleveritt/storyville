"""HTML path rewriting utilities for static assets.

This module provides utilities for rewriting static asset paths in HTML to be
relative based on page depth using tdom tree walking. This is an opt-in feature
that components must explicitly use by calling rewrite_static_paths().
"""

from pathlib import Path
from typing import Literal

from tdom import Element, Fragment, Node


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


def _walk_and_rewrite_element(
    element: Element,
    page_depth: int,
    discovered_assets: dict[str, Path],
) -> None:
    """Walk an element and its children, rewriting static paths in place.

    This function recursively traverses the node tree and modifies attribute
    values for static asset references directly on the nodes.

    Args:
        element: The element to process
        page_depth: The depth of the page in the site hierarchy
        discovered_assets: Dictionary mapping asset references to full output paths

    Note:
        - Modifies the element and its children in place
        - Only processes 'src' and 'href' attributes
        - Only rewrites paths starting with "static/" or "storytime_static/"
    """
    # Check if this element has attributes
    if hasattr(element, 'attrs') and isinstance(element.attrs, dict):
        # Check for src and href attributes
        for attr_name in ['src', 'href']:
            if attr_name in element.attrs:
                attr_value = element.attrs[attr_name]

                # Only process static paths
                if isinstance(attr_value, str) and (
                    attr_value.startswith('static/')
                    or attr_value.startswith('storytime_static/')
                ):
                    # Resolve the asset
                    resolved = resolve_static_asset_path(attr_value, discovered_assets)

                    if resolved is not None:
                        # Determine source type
                        source_type: Literal["storytime", "input_dir"] = (
                            "storytime" if attr_value.startswith("storytime_static")
                            else "input_dir"
                        )

                        # Calculate relative path and rewrite in place
                        new_path = calculate_relative_static_path(
                            resolved, page_depth, source_type
                        )
                        element.attrs[attr_name] = new_path

    # Recursively process children
    if hasattr(element, 'children') and isinstance(element.children, list):
        for child in element.children:
            if isinstance(child, Element):
                _walk_and_rewrite_element(child, page_depth, discovered_assets)


def resolve_static_asset_path(
    asset_ref: str, discovered_assets: dict[str, Path]
) -> str | None:
    """Resolve a short asset reference to its full output path.

    Takes a reference like "static/nav.css" or "storytime_static/components/nav/static/nav.css"
    and looks it up in the discovered assets dictionary to find the full output path.

    Args:
        asset_ref: The asset reference to resolve
        discovered_assets: Dictionary mapping asset references to full output paths

    Returns:
        Full asset path if found, None if not found

    Example:
        >>> assets = {"static/nav.css": Path("output/static/components/nav/static/nav.css")}
        >>> resolve_static_asset_path("static/nav.css", assets)
        'static/components/nav/static/nav.css'

    Note:
        - Handles both short references ("static/nav.css") and full references
        - Returns None if asset is not found in discovered_assets
        - The returned path is relative to the output directory
    """
    # Try direct lookup first
    if asset_ref in discovered_assets:
        # Return the path as a string, relative to output dir
        full_path = discovered_assets[asset_ref]
        # Extract just the parts after output dir (e.g., "static/components/...")
        # The full_path should already be structured correctly from discovery
        return str(full_path)

    # Try to find a matching asset by filename
    # asset_ref might be "static/nav.css" but discovered might be
    # "static/components/nav/static/nav.css"
    filename = asset_ref.split("/")[-1]
    prefix = asset_ref.split("/")[0]  # "static" or "storytime_static"

    for key, path in discovered_assets.items():
        if key.endswith(filename) and key.startswith(prefix):
            return str(path)

    return None


def validate_static_reference(
    asset_ref: str, discovered_assets: dict[str, Path]
) -> tuple[bool, str | None]:
    """Validate that a static asset reference exists in discovered assets.

    Checks if a referenced asset exists in the discovered_assets dictionary.

    Args:
        asset_ref: The asset reference to validate
        discovered_assets: Dictionary mapping asset references to full output paths

    Returns:
        Tuple of (is_valid, error_message_or_full_path)
        - (True, full_path) if found
        - (False, error_message) if not found

    Example:
        >>> assets = {"static/nav.css": Path("output/static/components/nav/static/nav.css")}
        >>> validate_static_reference("static/nav.css", assets)
        (True, 'static/components/nav/static/nav.css')
        >>> validate_static_reference("static/missing.css", assets)
        (False, 'Asset not found: static/missing.css')
    """
    resolved = resolve_static_asset_path(asset_ref, discovered_assets)

    if resolved is not None:
        return (True, resolved)

    return (False, f"Asset not found: {asset_ref}")


def rewrite_static_paths(
    node: Node,
    page_depth: int,
    discovered_assets: dict[str, Path],
) -> Node:
    """Rewrite all static asset paths in a Node tree to be relative based on page depth.

    This is the main opt-in utility function that components must explicitly call
    to rewrite static paths. It uses tdom tree walking to find and modify all static
    references directly on the node tree.

    Args:
        node: HTML content as tdom Node
        page_depth: The depth of the page in the site hierarchy
            - 0: Site root or section index
            - 1: Subject index
            - 2: Story page
        discovered_assets: Dictionary mapping asset references to full output paths

    Returns:
        The same Node with paths rewritten (modified in place)

    Example:
        >>> from tdom import html
        >>> test_node = html(t'<div><link href="static/nav.css" /></div>')
        >>> assets = {"static/nav.css": Path("static/components/nav/static/nav.css")}
        >>> result = rewrite_static_paths(test_node, 2, assets)
        >>> "../../static/components/nav/static/nav.css" in str(result)
        True

    Note:
        - Only rewrites paths starting with "static/" or "storytime_static/"
        - Preserves external URLs, absolute paths, and data: URIs
        - Works directly with node tree, avoiding string conversion and regex
        - Modifies the node tree in place and returns it
    """
    # Handle different node types
    if isinstance(node, Element):
        _walk_and_rewrite_element(node, page_depth, discovered_assets)
    elif isinstance(node, Fragment):
        # Fragment contains a list of children - walk each one
        if hasattr(node, 'children') and isinstance(node.children, list):
            for child in node.children:
                if isinstance(child, Element):
                    _walk_and_rewrite_element(child, page_depth, discovered_assets)

    return node


def build_discovered_assets_map(
    storytime_base: Path, input_dir: Path, output_dir: Path
) -> dict[str, Path]:
    """Build a mapping of asset references to full output paths.

    Discovers all static folders from both sources and builds a dictionary
    mapping short asset references to their full output paths for use with
    rewrite_static_paths().

    Args:
        storytime_base: Path to storytime installation (e.g., src/storytime)
        input_dir: Path to user's input directory
        output_dir: Path to output directory for built site

    Returns:
        Dictionary mapping asset references like "static/nav.css" to full paths

    Example:
        >>> from pathlib import Path
        >>> assets = build_discovered_assets_map(
        ...     Path("src/storytime"),
        ...     Path("examples/minimal"),
        ...     Path("output")
        ... )
        >>> "static/nav.css" in assets  # doctest: +SKIP
        True

    Note:
        - Discovers assets from both src/storytime and input_dir
        - Maps short references to full output paths
        - Used by rewrite_static_paths() for path resolution
    """
    from storytime.static_assets.discovery import discover_static_folders

    # Discover from both sources
    storytime_folders = discover_static_folders(storytime_base, "storytime")
    input_folders = discover_static_folders(input_dir, "input_dir")

    # Build the mapping
    assets: dict[str, Path] = {}

    # Process storytime folders
    for static_folder in storytime_folders:
        output_path = static_folder.calculate_output_path(output_dir)

        # List all files in the static folder
        if static_folder.source_path.exists():
            for file_path in static_folder.source_path.rglob("*"):
                if file_path.is_file():
                    # Calculate the relative path from static folder to file
                    rel_file = file_path.relative_to(static_folder.source_path)

                    # Create short reference: "storytime_static/filename"
                    short_ref = f"storytime_static/{rel_file.name}"

                    # Create full path: "storytime_static/components/nav/static/filename"
                    full_rel = output_path.relative_to(output_dir) / rel_file

                    assets[short_ref] = full_rel

    # Process input_dir folders
    for static_folder in input_folders:
        output_path = static_folder.calculate_output_path(output_dir)

        # List all files in the static folder
        if static_folder.source_path.exists():
            for file_path in static_folder.source_path.rglob("*"):
                if file_path.is_file():
                    # Calculate the relative path from static folder to file
                    rel_file = file_path.relative_to(static_folder.source_path)

                    # Create short reference: "static/filename"
                    short_ref = f"static/{rel_file.name}"

                    # Create full path: "static/components/nav/static/filename"
                    full_rel = output_path.relative_to(output_dir) / rel_file

                    assets[short_ref] = full_rel

    return assets
