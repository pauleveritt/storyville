"""Tests for sidebar collapse behavior (UI Cosmetics - Task Group 4).

These tests verify that the sidebar collapse CSS and JavaScript functionality
are correctly implemented, including localStorage persistence and responsive behavior.
"""

from pathlib import Path

import pytest

from storyville.build import build_site


@pytest.fixture
def built_site(tmp_path: Path) -> Path:
    """Build a test site for sidebar collapse verification.

    Returns:
        Path to the output directory containing built HTML files.
    """
    output_dir = tmp_path / "output"
    output_dir.mkdir(exist_ok=True)

    # Build the examples.minimal site for testing
    build_site(package_location="examples.minimal", output_dir=output_dir)

    return output_dir


def load_html(built_site: Path, path: str = "index.html") -> str:
    """Helper to load HTML file content.

    Args:
        built_site: Path to built site directory
        path: Relative path to HTML file (default: index.html)

    Returns:
        HTML content as string
    """
    return (built_site / path).read_text()


def load_css(built_site: Path) -> str:
    """Helper to load the storyville.css file content.

    Args:
        built_site: Path to built site directory

    Returns:
        CSS content as string
    """
    css_path = (
        built_site / "static" / "components" / "layout" / "static" / "storyville.css"
    )
    return css_path.read_text()


def load_js(built_site: Path, filename: str) -> str:
    """Helper to load a JavaScript file content.

    Args:
        built_site: Path to built site directory
        filename: Name of the JS file (e.g., 'sidebar.js')

    Returns:
        JavaScript content as string
    """
    js_path = built_site / "static" / "components" / "layout" / "static" / filename
    return js_path.read_text()


@pytest.mark.slow
def test_sidebar_js_file_exists(built_site: Path) -> None:
    """sidebar.js file should exist in the built output."""
    # Arrange
    js_path = built_site / "static" / "components" / "layout" / "static" / "sidebar.js"

    # Assert
    assert js_path.exists(), "sidebar.js should be copied to output directory"


@pytest.mark.slow
def test_sidebar_js_linked_in_html(built_site: Path) -> None:
    """sidebar.js should be linked in the HTML head/body."""
    # Arrange & Act
    html_content = load_html(built_site)

    # Assert - check for script tag referencing sidebar.js
    assert 'src="static/components/layout/static/sidebar.js"' in html_content, (
        "HTML should include script tag for sidebar.js"
    )


@pytest.mark.slow
def test_css_has_sidebar_collapsed_class(built_site: Path) -> None:
    """CSS should define .sidebar-collapsed class with appropriate styles."""
    # Arrange & Act
    css_content = load_css(built_site)

    # Assert - check for sidebar-collapsed class definition
    assert (
        ".sidebar-collapsed" in css_content or "body.sidebar-collapsed" in css_content
    ), "CSS should define .sidebar-collapsed class"


@pytest.mark.slow
def test_css_has_grid_transition(built_site: Path) -> None:
    """CSS should include transition for grid-template-columns."""
    # Arrange & Act
    css_content = load_css(built_site)

    # Assert - check for transition on body element
    # The transition should target grid-template-columns
    assert "transition:" in css_content, "CSS should include transition property"


@pytest.mark.slow
def test_css_has_responsive_mobile_behavior(built_site: Path) -> None:
    """CSS should have media query for mobile auto-collapse."""
    # Arrange & Act
    css_content = load_css(built_site)

    # Assert - check for media query at 768px breakpoint
    assert "@media" in css_content, "CSS should include media queries"
    assert "768px" in css_content, "CSS should include mobile breakpoint at 768px"


@pytest.mark.slow
def test_sidebar_js_uses_iife_pattern(built_site: Path) -> None:
    """sidebar.js should use IIFE pattern for encapsulation."""
    # Arrange & Act
    js_content = load_js(built_site, "sidebar.js")

    # Assert - check for IIFE pattern
    assert "(function" in js_content or "(() =>" in js_content, (
        "JavaScript should use IIFE pattern for encapsulation"
    )
    assert "'use strict'" in js_content or '"use strict"' in js_content, (
        "JavaScript should use strict mode"
    )


@pytest.mark.slow
def test_sidebar_js_queries_toggle_button(built_site: Path) -> None:
    """sidebar.js should query the toggle button by ID."""
    # Arrange & Act
    js_content = load_js(built_site, "sidebar.js")

    # Assert - check for querySelector with sidebar-toggle ID
    assert "querySelector" in js_content, (
        "JavaScript should use querySelector to find elements"
    )
    assert "sidebar-toggle" in js_content, (
        "JavaScript should query element with ID 'sidebar-toggle'"
    )


@pytest.mark.slow
def test_sidebar_js_handles_localstorage(built_site: Path) -> None:
    """sidebar.js should implement localStorage for state persistence."""
    # Arrange & Act
    js_content = load_js(built_site, "sidebar.js")

    # Assert - check for localStorage operations
    assert "localStorage" in js_content, (
        "JavaScript should use localStorage for state persistence"
    )
    assert "storyville.sidebar.collapsed" in js_content, (
        "JavaScript should use correct localStorage key"
    )


@pytest.mark.slow
def test_sidebar_js_toggles_body_class(built_site: Path) -> None:
    """sidebar.js should toggle .sidebar-collapsed class on body."""
    # Arrange & Act
    js_content = load_js(built_site, "sidebar.js")

    # Assert - check for classList operations
    assert "classList" in js_content, (
        "JavaScript should use classList to manipulate classes"
    )
    assert "sidebar-collapsed" in js_content, (
        "JavaScript should toggle 'sidebar-collapsed' class"
    )


@pytest.mark.slow
def test_sidebar_js_updates_aria_expanded(built_site: Path) -> None:
    """sidebar.js should update aria-expanded attribute on toggle."""
    # Arrange & Act
    js_content = load_js(built_site, "sidebar.js")

    # Assert - check for aria-expanded attribute updates
    assert "aria-expanded" in js_content, (
        "JavaScript should update aria-expanded attribute"
    )
