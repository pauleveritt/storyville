"""ControlIconButton component."""

from dataclasses import dataclass

from tdom import Node, html


@dataclass
class ControlIconButton:
    """A controliconbutton component."""

    text: str
    variant: str
    state: str

    def __call__(self) -> Node:
        """Render the component as HTML."""
        return html(t"<button class={self.variant} data-state={self.state}>{self.text}</button>")
