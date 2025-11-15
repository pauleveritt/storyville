"""Test the View Protocol."""

from dataclasses import dataclass

from tdom import Element, html

from storytime.models import View


def test_view_protocol_with_simple_dataclass() -> None:
    """Test that a simple dataclass can satisfy the View Protocol."""

    @dataclass
    class SimpleView:
        def __call__(self) -> Element:
            this_result = html(t"<div>Hello</div>")
            assert isinstance(this_result, Element)
            return this_result

    # Test that SimpleView can be used as a View
    view: View = SimpleView()
    result = view()
    assert isinstance(result, Element)


def test_view_protocol_return_type_is_element() -> None:
    """Test that View Protocol enforces the Element return type."""

    @dataclass
    class ElementView:
        def __call__(self) -> Element:
            this_result = html(t"<p>Content</p>")
            assert isinstance(this_result, Element)
            return this_result

    view: View = ElementView()
    result = view()

    # Verify the return type is Element, not just Node
    assert isinstance(result, Element)
    assert type(result).__name__ == "Element"


def test_view_protocol_with_dataclass_field() -> None:
    """Test View Protocol with a dataclass field."""

    @dataclass
    class FieldView:
        title: str = "Test"

        def __call__(self) -> Element:
            this_result = html(t"<h1>{self.title}</h1>")
            assert isinstance(this_result, Element)
            return this_result

    view: View = FieldView(title="Complex Test")
    result = view()
    assert isinstance(result, Element)
