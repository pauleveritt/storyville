"""A simple heading component."""
from dataclasses import dataclass

from hopscotch import injectable
from viewdom import VDOM
from viewdom import html


@injectable()
@dataclass()
class Heading:
    """An example component."""

    title: str = "Some Heading"

    def __call__(self) -> VDOM:
        """Return a VDOM for this component."""
        return html("<div>Hello {self.title}</div>")
