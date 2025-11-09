"""A simple heading component."""

from dataclasses import dataclass

from tdom import html, Node


@dataclass()
class Heading:
    """An example component."""

    title: str = "Some Heading"

    def __call__(self) -> Node:
        """Return a VDOM for this component."""
        return html(t"<div>Hello {self.title}</div>")
