"""The ``Site`` for the stories in this package."""

from tdom import Node

from storytime import Site

from examples.minimal.themed_layout import ThemedLayout


def themed_layout_wrapper(story_title: str | None = None, children: Node | None = None) -> Node:
    """Wrapper function to create and call ThemedLayout instances."""
    layout = ThemedLayout(story_title=story_title, children=children)
    return layout()


def this_site() -> Site:
    """The top of this package's story catalog."""
    return Site(
        title="Minimal Site",
        themed_layout=themed_layout_wrapper,
    )
