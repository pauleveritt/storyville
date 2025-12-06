"""Tests for sidebar toggle button (UI Cosmetics - Task Group 3).

These tests verify that the sidebar toggle button is correctly rendered
in the header with the proper FontAwesome icon and ARIA attributes.
"""

from pathlib import Path

import pytest
from aria_testing import get_by_role, get_by_tag_name, query_all_by_tag_name
from tdom.parser import parse_html

from storyville.build import build_site


@pytest.fixture
def built_site(tmp_path: Path) -> Path:
    """Build a test site for toggle button verification.

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
def test_toggle_button_exists_in_header(built_site: Path) -> None:
    """Toggle button should exist in header with correct ARIA label."""
    # Arrange & Act
    doc = load_html(built_site)

    # Assert - button should be present with correct ARIA label
    toggle_button = get_by_role(doc, "button", name="Toggle sidebar")
    assert toggle_button is not None, "Toggle button should exist with aria-label"


@pytest.mark.slow
def test_toggle_button_has_correct_id(built_site: Path) -> None:
    """Toggle button should have the ID 'sidebar-toggle' for JavaScript targeting."""
    # Arrange & Act
    doc = load_html(built_site)

    # Assert
    toggle_button = get_by_role(doc, "button", name="Toggle sidebar")
    assert toggle_button is not None
    assert toggle_button.attrs.get("id") == "sidebar-toggle", (
        "Toggle button should have ID 'sidebar-toggle'"
    )


@pytest.mark.slow
def test_toggle_button_has_aria_expanded_attribute(built_site: Path) -> None:
    """Toggle button should have aria-expanded attribute set to 'true' initially."""
    # Arrange & Act
    doc = load_html(built_site)

    # Assert
    toggle_button = get_by_role(doc, "button", name="Toggle sidebar")
    assert toggle_button is not None
    assert toggle_button.attrs.get("aria-expanded") == "true", (
        "Toggle button should have aria-expanded='true' initially"
    )


@pytest.mark.slow
def test_toggle_button_contains_fontawesome_icon(built_site: Path) -> None:
    """Toggle button should contain FontAwesome fa-bars icon."""
    # Arrange & Act
    doc = load_html(built_site)

    # Get toggle button
    toggle_button = get_by_role(doc, "button", name="Toggle sidebar")
    assert toggle_button is not None

    # Assert - button should contain an <i> element with fas fa-bars classes
    icon_elements = query_all_by_tag_name(toggle_button, "i")
    assert len(icon_elements) > 0, "Button should contain an <i> element for icon"

    icon = icon_elements[0]
    icon_class = icon.attrs.get("class") or ""
    assert "fas" in icon_class, "Icon should have 'fas' class"
    assert "fa-bars" in icon_class, "Icon should have 'fa-bars' class"


@pytest.mark.slow
def test_toggle_button_positioned_before_site_title(built_site: Path) -> None:
    """Toggle button should appear before the site title in header."""
    # Arrange & Act
    doc = load_html(built_site)
    header = get_by_tag_name(doc, "header")
    assert header is not None

    # Get the container div inside header
    container = get_by_tag_name(header, "div")
    assert container is not None
    assert container.attrs.get("class") == "container"

    # Get all children of the container
    children = list(container.children)

    # Assert - first child should be the button (or close to it)
    # We need to find the button and hgroup among the children
    button_index = None
    hgroup_index = None

    for i, child in enumerate(children):
        if hasattr(child, "tag"):
            if child.tag == "button":
                button_index = i
            elif child.tag == "hgroup":
                hgroup_index = i

    assert button_index is not None, "Button should exist in header container"
    assert hgroup_index is not None, "Hgroup should exist in header container"
    assert button_index < hgroup_index, (
        "Toggle button should appear before hgroup (site title)"
    )
