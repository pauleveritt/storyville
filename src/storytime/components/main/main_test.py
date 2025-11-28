"""Test the LayoutMain component."""

from aria_testing import get_by_tag_name, get_text_content
from tdom import html

from storytime.components.main.main import LayoutMain

def test_layout_main_renders_children() -> None:
    """Test LayoutMain renders children content."""
    test_content = html(t"<p>Test Content</p>")
    main = LayoutMain(current_path=None, children=test_content)
    result = main()
    element = result

    # Find the main element (handles both Element and Fragment)
    main_elem = get_by_tag_name(element, "main")
    assert main_elem is not None

    # Check that children content is present
    text_content = get_text_content(main_elem)
    assert "Test Content" in text_content

def test_layout_main_renders_breadcrumbs() -> None:
    """Test LayoutMain renders Breadcrumbs component."""
    main = LayoutMain(current_path="getting-started/installation", children=None)
    result = main()
    element = result

    # Should have a nav element with aria-label="Breadcrumb" from Breadcrumbs
    nav = get_by_tag_name(element, "nav")
    assert nav.attrs.get("aria-label") == "Breadcrumb"

def test_layout_main_handles_none_children() -> None:
    """Test LayoutMain handles None children gracefully."""
    main = LayoutMain(current_path=None, children=None)
    result = main()
    element = result

    # Find the main element (handles both Element and Fragment)
    main_elem = get_by_tag_name(element, "main")
    assert main_elem is not None
