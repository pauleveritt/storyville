"""Root catalog configuration for generated Storytime catalog."""

from tdom import Node
from storytime import Catalog

from .themed_layout.themed_layout import ThemedLayout


def themed_layout_wrapper(
    story_title: str | None = None, children: Node | None = None
) -> Node:
    """Wrapper function to create and call ThemedLayout instances.

    Args:
        story_title: The title of the story being rendered.
        children: The child nodes to render within the layout.

    Returns:
        Node: The rendered themed layout.
    """
    layout = ThemedLayout(story_title=story_title, children=children)
    return layout()


def this_catalog() -> Catalog:
    """Create and configure the catalog.

    Returns:
        Catalog: The configured catalog instance with themed layout.
    """
    return Catalog(title="Storytime Seed Catalog", themed_layout=themed_layout_wrapper)
