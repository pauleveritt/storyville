"""LayoutMain component for main content area."""

from dataclasses import dataclass

from tdom import Element, Fragment, Node, html

from storytime.components.breadcrumbs import Breadcrumbs


@dataclass
class LayoutMain:
    """Main component with breadcrumbs and content.

    Renders main element containing Breadcrumbs navigation
    and children content.
    """

    current_path: str | None = None
    children: Element | Fragment | Node | None = None

    def __call__(self) -> Node:
        """Render the main element to a tdom Node.

        Returns:
            A tdom Node representing the main element.
        """
        return html(t'''\
<main>
  <{Breadcrumbs} current_path={self.current_path} />
  {self.children}
</main>
''')
