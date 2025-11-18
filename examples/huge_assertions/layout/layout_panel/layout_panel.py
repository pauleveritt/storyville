"""LayoutPanel component."""

from dataclasses import dataclass

from tdom import Node, html


@dataclass
class LayoutPanel:
    """A layoutpanel component."""

    text: str
    variant: str
    state: str

    def __call__(self) -> Node:
        """Render the component as HTML."""
        return html(t"<div class={self.variant} data-state={self.state}>{self.text}</div>")
