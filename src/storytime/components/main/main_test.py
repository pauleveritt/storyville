"""Test the LayoutMain component."""

from aria_testing import get_by_tag_name, get_text_content
from tdom import Element, Fragment, Node, html

from storytime.components.main.main import LayoutMain


def _get_element(result: Node) -> Element:
    """Extract Element from result (handles Fragment wrapper)."""
    if isinstance(result, Fragment):
        for child in result.children:
            if isinstance(child, Element):
                return child
    if isinstance(result, Element):
        return result
    raise ValueError("Result is not an Element or Fragment containing an Element")


def test_layout_main_renders_children() -> None:
    """Test LayoutMain renders children content."""
    test_content = html(t"<p>Test Content</p>")
    main = LayoutMain(current_path=None, children=test_content)
    result = main()
    element = _get_element(result)

    assert element.tag == "main"

    # Check that children content is present
    text_content = get_text_content(element)
    assert "Test Content" in text_content


def test_layout_main_renders_breadcrumbs() -> None:
    """Test LayoutMain renders Breadcrumbs component."""
    main = LayoutMain(current_path="getting-started/installation", children=None)
    result = main()
    element = _get_element(result)

    # Should have a nav element with aria-label="Breadcrumb" from Breadcrumbs
    nav = get_by_tag_name(element, "nav")
    assert nav.attrs.get("aria-label") == "Breadcrumb"


def test_layout_main_handles_none_children() -> None:
    """Test LayoutMain handles None children gracefully."""
    main = LayoutMain(current_path=None, children=None)
    result = main()
    element = _get_element(result)

    assert element.tag == "main"
