"""ThemedStory component for rendering stories with custom themed layouts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from tdom import Node

from storyville.components.layout import Layout

if TYPE_CHECKING:
    from storyville.catalog.models import Catalog


@dataclass
class ThemedStory:
    """ThemedStory component wrapping story content in themed layout.

    Renders story content within the catalog's configured ThemedLayout,
    or falls back to the standard Layout if no themed layout is configured.
    """

    story_title: str
    children: Node | None
    site: Catalog

    def __call__(self) -> Node:
        """Render the themed story to a tdom Node.

        Returns:
            A tdom Node representing the complete HTML document.
        """
        # Check if catalog has a themed_layout configured
        if self.site.themed_layout is not None:
            # Use the custom themed layout callable
            # Call it with story_title and children parameters
            return self.site.themed_layout(
                story_title=self.story_title, children=self.children
            )
        else:
            # Fall back to standard Layout
            layout = Layout(
                view_title=self.story_title,
                site=self.site,
                children=self.children,
                depth=0,
            )
            return layout()
