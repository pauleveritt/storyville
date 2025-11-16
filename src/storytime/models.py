"""Protocols for type-safe structural typing in Storytime."""


from typing import Callable, Protocol

from tdom import Node

type Target = type | Callable
type Template = Callable[[], Node]


class View(Protocol):
    """Protocol for view classes that render to tdom Nodes.

    This Protocol enables type-safe structural typing for all view
    implementations without requiring inheritance. Any class that
    implements a `__call__(self) -> Node` method satisfies this
    Protocol and can be used as a View.

    Type guards should be used in tests to verify the result is an
    Element when needed for type checking.

    Example:
        @dataclass
        class MyView:
            title: str

            def __call__(self) -> Node:
                return html(t"<h1>{self.title}</h1>")

        # MyView satisfies the View Protocol
        view: View = MyView(title="Hello")
        node = view()

        # In tests, use type guards:
        assert isinstance(node, Element)
    """

    def __call__(self) -> Node:
        """Render the view to a tdom Node.

        Returns:
            A tdom Node representing the rendered view.
        """
        ...
