"""Badge component."""

from dataclasses import dataclass

from tdom import Node, html


@dataclass
class Badge:
    """A badge component that displays a count."""

    count: int

    def __call__(self) -> Node:
        """Render the badge as HTML."""
        return html(t"<span>{self.count}</span>")
