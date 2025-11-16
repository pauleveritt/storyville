"""Alert component."""


from dataclasses import dataclass

from tdom import Node, html


@dataclass
class Alert:
    """An alert component that displays a message."""

    message: str

    def __call__(self) -> Node:
        """Render the alert as HTML."""
        return html(t"<div role='alert'>{self.message}</div>")
