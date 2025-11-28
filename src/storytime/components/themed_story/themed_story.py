"""ThemedStory component for rendering stories with custom themed layouts."""

from dataclasses import dataclass

from tdom import Node

from storytime.components.layout import Layout
from storytime.site.models import Site


@dataclass
class ThemedStory:
    """ThemedStory component wrapping story content in themed layout.

    Renders story content within the site's configured ThemedLayout,
    or falls back to the standard Layout if no themed layout is configured.
    """

    story_title: str
    children: Node | None
    site: Site

    def __call__(self) -> Node:
        """Render the themed story to a tdom Node.

        Returns:
            A tdom Node representing the complete HTML document.
        """
        # Check if site has a themed_layout configured
        if self.site.themed_layout is not None:
            # Use the custom themed layout callable
            # Call it with story_title and children parameters
            return self.site.themed_layout(
                story_title=self.story_title,
                children=self.children
            )
        else:
            # Fall back to standard Layout
            layout = Layout(
                view_title=self.story_title,
                site=self.site,
                children=self.children,
                depth=0
            )
            return layout()
