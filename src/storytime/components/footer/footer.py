"""LayoutFooter component for page footer."""

from dataclasses import dataclass

from tdom import Node, html


@dataclass
class LayoutFooter:
    """Footer component with copyright text.

    Renders footer element with centered paragraph containing
    year and text (typically copyright information).
    """

    year: str | int = 2025
    text: str = "Storytime"

    def __call__(self) -> Node:
        """Render the footer to a tdom Node.

        Returns:
            A tdom Node representing the footer element.
        """
        return html(t'''\
<footer>
  <p style="text-align: center;">{self.year} {self.text}</p>
</footer>
''')
