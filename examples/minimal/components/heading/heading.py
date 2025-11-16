"""Heading component."""

from __future__ import annotations

from dataclasses import dataclass

from tdom import Node, html


@dataclass
class Heading:
    """A heading component that displays a title."""

    name: str

    def __call__(self) -> Node:
        """Render the heading as HTML."""
        return html(t"<h1>{self.name}</h1>")
