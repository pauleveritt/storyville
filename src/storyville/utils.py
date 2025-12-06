"""General utility functions for Storyville."""

from tdom import Element, Fragment, Node


def rewrite_static_paths(node: Node, depth: int) -> Node:
    """Rewrite static/ paths based on page depth.

    This function walks the node tree and rewrites href/src attributes
    that start with "static/" to include the correct ../ prefix based
    on the page's depth in the output directory.

    Args:
        node: The node tree to rewrite
        depth: The depth of the page in the output directory (0 = root)

    Returns:
        The same node (modified in place)

    Example:
        >>> from tdom import html
        >>> node = html(t'<link href="static/style.css" />')
        >>> rewritten = rewrite_static_paths(node, depth=1)
        >>> # href is now "../../static/style.css"
    """

    def walk_element(element: Element) -> None:
        # Rewrite static/ paths in href and src attributes
        if hasattr(element, "attrs") and isinstance(element.attrs, dict):
            for attr_name in ["href", "src"]:
                if attr_name in element.attrs:
                    attr_value = element.attrs[attr_name]
                    if isinstance(attr_value, str) and attr_value.startswith("static/"):
                        # Add ../ prefix based on depth
                        # depth=0: static/file.css (no prefix)
                        # depth=1: ../../static/file.css (up 2 levels to get to root from section/subject/)
                        # For section pages at root (components/index.html), depth=0 but need ../
                        # Wait, sections are at depth 0 too since they're at root level
                        # The issue is: index.html is at root (depth 0) -> needs "static/"
                        # components/index.html is ALSO at depth 0 (sections at root) -> needs "../static/"
                        # components/heading/index.html is at depth 1 -> needs "../../static/"

                        # Actually, for file-based paths:
                        # - index.html (0 dirs deep) -> static/
                        # - components/index.html (1 dir deep) -> ../static/
                        # - components/heading/index.html (2 dirs deep) -> ../../static/
                        # So we need ../ for each directory level, which IS depth
                        prefix = "../" * depth if depth > 0 else ""
                        element.attrs[attr_name] = f"{prefix}{attr_value}"

        # Recursively process children
        if hasattr(element, "children") and isinstance(element.children, list):
            for child in element.children:
                if isinstance(child, Element):
                    walk_element(child)

    # Handle both Element and Fragment types
    if isinstance(node, Element):
        walk_element(node)
    elif isinstance(node, Fragment):
        if hasattr(node, "children") and isinstance(node.children, list):
            for child in node.children:
                if isinstance(child, Element):
                    walk_element(child)

    return node
