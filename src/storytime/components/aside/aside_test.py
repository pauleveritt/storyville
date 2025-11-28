"""Test the LayoutAside component."""

from aria_testing import get_by_tag_name, get_text_content
from storytime.components.aside.aside import LayoutAside

def test_layout_aside_handles_cached_navigation_html() -> None:
    """Test LayoutAside handles cached_navigation HTML using Markup."""
    cached_html = "<nav><ul><li>Cached Item</li></ul></nav>"
    aside = LayoutAside(
        sections={},
        current_path=None,
        cached_navigation=cached_html,
    )
    result = aside()
    element = result

    # Find the aside element (handles both Element and Fragment)
    aside_elem = get_by_tag_name(element, "aside")
    assert aside_elem is not None

    # Check that cached HTML is present
    text_content = get_text_content(aside_elem)
    assert "Cached Item" in text_content

def test_layout_aside_renders_sections_label() -> None:
    """Test LayoutAside renders 'Sections' label."""
    aside = LayoutAside(sections={}, current_path=None)
    result = aside()
    element = result

    text_content = get_text_content(element)
    assert "Sections" in text_content

def test_layout_aside_renders_navigation_tree_without_cached() -> None:
    """Test LayoutAside renders NavigationTree when no cached navigation provided."""
    # We'll use empty sections dict for simplicity
    aside = LayoutAside(sections={}, current_path=None, cached_navigation=None)
    result = aside()
    element = result

    # Find the aside element (handles both Element and Fragment)
    aside_elem = get_by_tag_name(element, "aside")
    assert aside_elem is not None

    # Should have a nav element from NavigationTree
    nav = get_by_tag_name(aside_elem, "nav")
    assert nav is not None
