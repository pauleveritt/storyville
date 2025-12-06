"""Test the minimal example ThemedLayout component."""

from aria_testing import get_by_tag_name, get_text_content
from tdom import html

from examples.minimal.themed_layout import ThemedLayout


def test_themed_layout_renders_full_html_document_structure() -> None:
    """Test ThemedLayout renders full HTML document structure."""
    # Create test content
    story_content = html(t"<p>Test story content</p>")

    # Create ThemedLayout instance
    themed_layout = ThemedLayout(story_title="My Test Story", children=story_content)

    # Render
    result = themed_layout()
    element = result

    # Verify full HTML structure (result might be Fragment with DOCTYPE + html)
    html_elem = get_by_tag_name(element, "html")
    assert html_elem is not None

    # Verify lang attribute
    assert html_elem.attrs.get("lang") == "EN"

    # Verify has head and body
    head = get_by_tag_name(html_elem, "head")
    assert head is not None

    body = get_by_tag_name(html_elem, "body")
    assert body is not None

    # Verify DOCTYPE is in result (check string representation)
    html_string = str(result)
    assert "<!DOCTYPE html>" in html_string


def test_themed_layout_passes_through_children_content() -> None:
    """Test ThemedLayout passes through children content."""
    # Create unique test content
    story_content = html(t'<div id="unique-test-id">Unique test content here</div>')

    # Create ThemedLayout instance
    themed_layout = ThemedLayout(story_title="Test Story", children=story_content)

    # Render
    result = themed_layout()
    element = result

    # Verify children content is present in the rendered output
    body = get_by_tag_name(element, "body")
    # Find the theme-wrapper div specifically
    wrapper_div = get_by_tag_name(body, "div", attrs={"class": "theme-wrapper"})

    # Check for our unique test content inside the wrapper
    text_content = get_text_content(wrapper_div)
    assert "Unique test content here" in text_content


def test_themed_layout_includes_custom_css_styling() -> None:
    """Test ThemedLayout includes custom CSS styling."""
    # Create test content
    story_content = html(t"<p>Content</p>")

    # Create ThemedLayout instance
    themed_layout = ThemedLayout(story_title="Styled Story", children=story_content)

    # Render
    result = themed_layout()
    element = result

    # Verify head contains style tag with custom CSS
    head = get_by_tag_name(element, "head")
    style = get_by_tag_name(head, "style")

    # Verify style tag exists
    assert style is not None

    # Verify it contains custom styling (check for body or theme-wrapper rules)
    style_content = get_text_content(style)
    assert len(style_content) > 0  # Has some CSS content
