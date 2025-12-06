"""Test the LayoutFooter component."""

from aria_testing import get_by_tag_name, get_text_content
from storyville.components.footer.footer import LayoutFooter


def test_layout_footer_renders_with_year_and_text() -> None:
    """Test LayoutFooter renders with year and text props."""
    footer = LayoutFooter(year=2025, text="Storyville")
    result = footer()
    element = result

    # Find the footer element (handles both Element and Fragment)
    footer_elem = get_by_tag_name(element, "footer")
    assert footer_elem is not None

    # Check for year and text in paragraph
    text_content = get_text_content(footer_elem)
    assert "2025" in text_content
    assert "Storyville" in text_content


def test_layout_footer_uses_default_values() -> None:
    """Test LayoutFooter uses default year and text values."""
    footer = LayoutFooter()
    result = footer()
    element = result

    text_content = get_text_content(element)
    assert "2025" in text_content
    assert "Storyville" in text_content


def test_layout_footer_has_centered_paragraph() -> None:
    """Test LayoutFooter has paragraph with text-align center style."""
    footer = LayoutFooter()
    result = footer()
    element = result

    # Check for paragraph with centered text
    para = get_by_tag_name(element, "p")
    assert para is not None
    # The original layout uses inline style for center alignment
    style_attr = para.attrs.get("style") or ""
    assert "text-align: center" in style_attr
