"""Test the LayoutFooter component."""

from aria_testing import get_by_tag_name, get_text_content
from tdom import Element, Fragment, Node

from storytime.components.footer.footer import LayoutFooter


def _get_element(result: Node) -> Element:
    """Extract Element from result (handles Fragment wrapper)."""
    if isinstance(result, Fragment):
        for child in result.children:
            if isinstance(child, Element):
                return child
    if isinstance(result, Element):
        return result
    raise ValueError("Result is not an Element or Fragment containing an Element")


def test_layout_footer_renders_with_year_and_text() -> None:
    """Test LayoutFooter renders with year and text props."""
    footer = LayoutFooter(year=2025, text="Storytime")
    result = footer()
    element = _get_element(result)

    assert element.tag == "footer"

    # Check for year and text in paragraph
    text_content = get_text_content(element)
    assert "2025" in text_content
    assert "Storytime" in text_content


def test_layout_footer_uses_default_values() -> None:
    """Test LayoutFooter uses default year and text values."""
    footer = LayoutFooter()
    result = footer()
    element = _get_element(result)

    text_content = get_text_content(element)
    assert "2025" in text_content
    assert "Storytime" in text_content


def test_layout_footer_has_centered_paragraph() -> None:
    """Test LayoutFooter has paragraph with text-align center style."""
    footer = LayoutFooter()
    result = footer()
    element = _get_element(result)

    # Check for paragraph with centered text
    para = get_by_tag_name(element, "p")
    assert para is not None
    # The original layout uses inline style for center alignment
    assert "text-align: center" in para.attrs.get("style", "")
