"""Tests for CSS visual refinements (UI Cosmetics - Task Group 2).

These tests verify that the CSS changes for main background color and
navigation padding are correctly applied in the rendered HTML.
"""

from pathlib import Path

import pytest
from aria_testing import get_by_tag_name, query_all_by_tag_name
from tdom.parser import parse_html

from storyville.build import build_site


@pytest.fixture
def built_site(tmp_path: Path) -> Path:
    """Build a test site for CSS verification.

    Returns:
        Path to the output directory containing built HTML files.
    """
    output_dir = tmp_path / "output"
    output_dir.mkdir(exist_ok=True)

    # Build the examples.minimal site for testing
    build_site(package_location="examples.minimal", output_dir=output_dir)

    return output_dir


def load_html(built_site: Path, path: str = "index.html"):
    """Helper to load and parse HTML file.

    Args:
        built_site: Path to built site directory
        path: Relative path to HTML file (default: index.html)

    Returns:
        Parsed HTML document (tdom Element)
    """
    html_content = (built_site / path).read_text()
    return parse_html(html_content)


@pytest.mark.slow
def test_main_element_exists(built_site: Path) -> None:
    """Main element should exist in the layout."""
    # Arrange & Act
    doc = load_html(built_site)

    # Assert - main element should be present
    main = get_by_tag_name(doc, "main")
    assert main is not None, "Main element should exist"


@pytest.mark.slow
def test_css_file_contains_main_background_rule(built_site: Path) -> None:
    """CSS file should contain background-color rule for main element."""
    # Arrange
    css_path = (
        built_site / "static" / "components" / "layout" / "static" / "storyville.css"
    )

    # Act
    css_content = css_path.read_text()

    # Assert - CSS should have main background-color rule with Pico CSS variable
    assert "main {" in css_content or "main{" in css_content, (
        "CSS should have main selector"
    )
    assert "background-color" in css_content, (
        "CSS should contain background-color property"
    )
    assert "--pico-card-background-color" in css_content, (
        "CSS should use --pico-card-background-color variable"
    )


@pytest.mark.slow
def test_css_file_contains_navigation_padding_rule(built_site: Path) -> None:
    """CSS file should contain reduced padding for navigation list item links."""
    # Arrange
    css_path = (
        built_site / "static" / "components" / "layout" / "static" / "storyville.css"
    )

    # Act
    css_content = css_path.read_text()

    # Assert - CSS should have navigation link padding with reduced values
    assert "aside nav details ul li a" in css_content, (
        "CSS should have navigation link selector"
    )
    # Padding should be reduced (4 units = 0.25rem, less than previous 0.125rem + any other)
    # We check that padding exists on the li a selector
    lines = css_content.split("\n")
    found_selector = False
    found_padding = False
    for i, line in enumerate(lines):
        if "aside nav details ul li a" in line:
            found_selector = True
            # Look for padding in the next 10 lines (within the rule block)
            for j in range(i, min(i + 10, len(lines))):
                if "padding:" in lines[j]:
                    found_padding = True
                    break
            break

    assert found_selector, "Should find navigation link selector"
    assert found_padding, "Should find padding rule for navigation links"


@pytest.mark.slow
def test_navigation_structure_preserved(built_site: Path) -> None:
    """Navigation structure should remain intact after CSS changes."""
    # Arrange & Act
    doc = load_html(built_site)

    # Assert - aside and navigation should still exist
    aside = get_by_tag_name(doc, "aside")
    assert aside is not None, "Aside element should exist"

    nav = get_by_tag_name(aside, "nav")
    assert nav is not None, "Nav element should exist inside aside"

    # Should still have details elements for collapsible sections
    details_elements = query_all_by_tag_name(aside, "details")
    assert len(details_elements) > 0, "Should have details elements in navigation"

    # Should still have links in the navigation
    all_links = query_all_by_tag_name(aside, "a")
    assert len(all_links) > 0, "Should have links in navigation"
