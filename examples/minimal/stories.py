"""The ``Catalog`` for the stories in this package."""

from tdom import Node

from examples.minimal.themed_layout import ThemedLayout
from storytime import Catalog


def themed_layout_wrapper(story_title: str | None = None, children: Node | None = None) -> Node:
    """Wrapper function to create and call ThemedLayout instances."""
    layout = ThemedLayout(story_title=story_title, children=children)
    return layout()


def this_catalog() -> Catalog:
    """The top of this package's story catalog."""
    return Catalog(
        title="Minimal Catalog",
        themed_layout=themed_layout_wrapper,
    )
