"""Test the LayoutAside component."""

from aria_testing import get_by_tag_name, get_text_content
from tdom import Element, Fragment, Node

from storytime.components.aside.aside import LayoutAside


def _get_element(result: Node) -> Element:
    """Extract Element from result (handles Fragment wrapper)."""
    if isinstance(result, Fragment):
        for child in result.children:
            if isinstance(child, Element):
                return child
    if isinstance(result, Element):
        return result
    raise ValueError("Result is not an Element or Fragment containing an Element")


def test_layout_aside_handles_cached_navigation_html() -> None:
    """Test LayoutAside handles cached_navigation HTML using Markup."""
    cached_html = "<nav><ul><li>Cached Item</li></ul></nav>"
    aside = LayoutAside(
        sections={},
        current_path=None,
        cached_navigation=cached_html,
    )
    result = aside()
    element = _get_element(result)

    assert element.tag == "aside"

    # Check that cached HTML is present
    text_content = get_text_content(element)
    assert "Cached Item" in text_content


def test_layout_aside_renders_sections_label() -> None:
    """Test LayoutAside renders 'Sections' label."""
    aside = LayoutAside(sections={}, current_path=None)
    result = aside()
    element = _get_element(result)

    text_content = get_text_content(element)
    assert "Sections" in text_content


def test_layout_aside_renders_navigation_tree_without_cached() -> None:
    """Test LayoutAside renders NavigationTree when no cached navigation provided."""
    # We'll use empty sections dict for simplicity
    aside = LayoutAside(sections={}, current_path=None, cached_navigation=None)
    result = aside()
    element = _get_element(result)

    assert element.tag == "aside"

    # Should have a nav element from NavigationTree
    nav = get_by_tag_name(element, "nav")
    assert nav is not None
