"""Heading component."""


from dataclasses import dataclass

from tdom import Node, html


@dataclass(frozen=True)
class Heading:
    """A heading component that displays a title."""

    name: str

    def __call__(self) -> Node:
        """Render the heading as HTML."""
        return html(t"<h1>{self.name}</h1>")
