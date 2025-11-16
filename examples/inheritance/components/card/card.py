"""Card component."""


from dataclasses import dataclass

from tdom import Node, html


@dataclass
class Card:
    """A card component that displays a title and text."""

    title: str
    text: str

    def __call__(self) -> Node:
        """Render the card as HTML."""
        return html(t"<div><h2>{self.title}</h2><p>{self.text}</p></div>")
