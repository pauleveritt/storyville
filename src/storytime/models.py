"""Protocols for type-safe structural typing in Storytime."""

from typing import Protocol

from tdom import Element


class View(Protocol):
    """Protocol for view classes that render to tdom Elements.

    This Protocol enables type-safe structural typing for all view
    implementations without requiring inheritance. Any class that
    implements a `__call__(self) -> Element` method satisfies this
    Protocol and can be used as a View.

    Use a type guard to ensure the result is an Element when the
    rendering process might return a Node that needs to be narrowed.

    Example:
        @dataclass
        class MyView:
            title: str

            def __call__(self) -> Element:
                result = html(t"<h1>{self.title}</h1>")
                assert isinstance(result, Element)
                return result

        # MyView satisfies the View Protocol
        view: View = MyView(title="Hello")
        element = view()
    """

    def __call__(self) -> Element:
        """Render the view to a tdom Element.

        Returns:
            A tdom Element representing the rendered view.
        """
        ...
