"""LayoutAside component for sidebar navigation."""

from dataclasses import dataclass

from tdom import Node, html

from storytime.components.navigation_tree import NavigationTree
from storytime.section.models import Section


@dataclass
class LayoutAside:
    """Aside component with hierarchical navigation tree.

    Renders aside element with "Sections" label and navigation.
    Handles cached navigation HTML when provided, otherwise renders
    NavigationTree component fresh.
    """

    sections: dict[str, Section]
    current_path: str | None = None
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
                sections=self.sections, current_path=self.current_path
            )()

        return html(t'''\
<aside>
  <strong>Sections</strong>
  {navigation_html}
</aside>
''')
