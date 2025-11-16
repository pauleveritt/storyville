"""Button component."""

from __future__ import annotations

from dataclasses import dataclass

from tdom import Node, html


@dataclass
class Button:
    """A button component with text and variant styling."""

    text: str
    variant: str

    def __call__(self) -> Node:
        """Render the button as HTML."""
        return html(t"<button class={self.variant}>{self.text}</button>")
