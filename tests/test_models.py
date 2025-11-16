"""Test the View Protocol."""

from tdom import Element

from storytime.models import View


def test_view_protocol_with_simple_dataclass(simple_view) -> None:
    """Test that a simple dataclass can satisfy the View Protocol."""
    # Test that SimpleView can be used as a View
    view: View = simple_view()
    result = view()
    assert isinstance(result, Element)


def test_view_protocol_return_type_is_element(element_view) -> None:
    """Test that View Protocol returns Node and tests verify Element."""
    view: View = element_view()
    result = view()

    # Tests verify the return type is Element, not just Node
    assert isinstance(result, Element)
    assert type(result).__name__ == "Element"


def test_view_protocol_with_dataclass_field(field_view) -> None:
    """Test View Protocol with a dataclass field."""
    view: View = field_view(title="Complex Test")
    result = view()
    assert isinstance(result, Element)
