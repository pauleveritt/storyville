"""LayoutAside component for sidebar navigation."""

from dataclasses import dataclass

from tdom import Node, html

from storyville.components.navigation_tree import NavigationTree
from storyville.section.models import Section


@dataclass
class LayoutAside:
    """Aside component with hierarchical navigation tree.

    Renders aside element with navigation tree.
    Handles cached navigation HTML when provided, otherwise renders
    NavigationTree component fresh.
    """

    sections: dict[str, Section]
    resource_path: str = ""
    cached_navigation: str | None = None

    def __call__(self) -> Node:
        """Render the aside to a tdom Node.

        Returns:
            A tdom Node representing the aside element.
        """
        # Use cached navigation if available, otherwise render fresh
        if self.cached_navigation is not None:
            from markupsafe import Markup

            navigation_html = Markup(self.cached_navigation)
        else:
            navigation_html = NavigationTree(
                sections=self.sections, resource_path=self.resource_path
            )()

        return html(t"""\
<aside>
  {navigation_html}
</aside>
""")
