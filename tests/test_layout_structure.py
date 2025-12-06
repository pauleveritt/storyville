"""Layout structure tests using tdom + aria-testing.

These tests verify DOM structure without requiring a browser.
They're faster alternatives to Playwright tests for checking static HTML structure.
"""

import re
import pytest
from pathlib import Path
from tdom.parser import parse_html
from aria_testing import (
    get_by_role,
    get_by_tag_name,
    query_all_by_tag_name,
    get_text_content,
)
from storyville.build import build_site


@pytest.fixture
def built_site(tmp_path: Path) -> Path:
    """Build a test site with hierarchical structure.

    Creates a minimal site structure with:
    - One section with one subject containing one story
    - About and Debug pages

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
def test_header_navigation_links_present(built_site: Path) -> None:
    """Header should contain Home, About, and Debug navigation links."""
    # Arrange & Act
    doc = load_html(built_site)

    # Assert - check header nav contains expected links
    assert get_by_role(doc, "link", name="Home") is not None
    assert get_by_role(doc, "link", name="About") is not None
    assert get_by_role(doc, "link", name="Debug") is not None


@pytest.mark.slow
def test_header_links_have_correct_hrefs(built_site: Path) -> None:
    """Header navigation links should have correct href attributes."""
    # Arrange & Act
    doc = load_html(built_site)

    # Assert - verify href attributes
    home_link = get_by_role(doc, "link", name="Home")
    about_link = get_by_role(doc, "link", name="About")
    debug_link = get_by_role(doc, "link", name="Debug")

    assert home_link.attrs["href"] == "/"
    assert about_link.attrs["href"] == "/about"
    assert debug_link.attrs["href"] == "/debug"


@pytest.mark.slow
def test_sidebar_navigation_sections_collapsed_by_default(built_site: Path) -> None:
    """Sidebar sections should be collapsed by default (no open attribute)."""
    # Arrange & Act
    doc = load_html(built_site)

    # Assert - details elements in aside should not have open attribute
    aside = get_by_tag_name(doc, "aside")
    assert aside is not None

    details_elements = query_all_by_tag_name(aside, "details")
    assert len(details_elements) > 0, "Should have at least one section"

    # Check that at least one section is collapsed (doesn't have open attribute)
    collapsed = [d for d in details_elements if "open" not in d.attrs]
    assert len(collapsed) > 0, "At least one section should be collapsed by default"


@pytest.mark.slow
def test_footer_displays_copyright(built_site: Path) -> None:
    """Footer should display copyright text."""
    # Arrange & Act
    doc = load_html(built_site)

    # Assert - footer should contain copyright text
    footer = get_by_tag_name(doc, "footer")
    assert footer is not None
    footer_text = get_text_content(footer)
    assert "2025 Storyville" in footer_text


@pytest.mark.slow
def test_sidebar_shows_hierarchical_structure(built_site: Path) -> None:
    """Sidebar should display three-level hierarchy (sections > subjects > stories)."""
    # Arrange & Act
    doc = load_html(built_site)

    # Assert - check structure exists
    aside = get_by_tag_name(doc, "aside")
    assert aside is not None

    # Should have section-level details (get all details in aside)
    all_details = query_all_by_tag_name(aside, "details")
    assert len(all_details) > 0, "Should have details elements"

    # First should be a section-level details
    first_section = all_details[0]

    # Should have nested details inside the first section (for subjects)
    nested_details = query_all_by_tag_name(first_section, "details")
    assert len(nested_details) > 0, "Should have nested subject-level details"

    # Should have story links inside (find all anchors)
    all_links = query_all_by_tag_name(first_section, "a")
    assert len(all_links) > 0, "Should have story links"


@pytest.mark.slow
def test_story_links_in_sidebar_have_correct_structure(built_site: Path) -> None:
    """Story links in sidebar should follow /{section}/{subject}/story-{idx}/index.html pattern."""
    # Arrange & Act
    doc = load_html(built_site)

    # Find first story link in sidebar
    aside = get_by_tag_name(doc, "aside")
    assert aside is not None

    # Get all links in sidebar
    all_links = query_all_by_tag_name(aside, "a")
    assert len(all_links) > 0

    # Find a story link (should have story- in the href)
    story_link = None
    for link in all_links:
        href = link.attrs.get("href", "") or ""
        if "story-" in href:
            story_link = link
            break

    assert story_link is not None, "Should have at least one story link"

    # Assert - href should match expected pattern
    href = story_link.attrs.get("href")
    assert href is not None
    # Pattern: /{section}/{subject}/story-{idx}/index.html
    assert re.match(r"^/[\w-]+/[\w-]+/story-\d+/index\.html$", href), (
        f"Expected story link pattern, got: {href}"
    )


@pytest.mark.slow
def test_two_column_grid_layout_structure(built_site: Path) -> None:
    """Page should have a two-column layout with aside and main elements."""
    # Arrange & Act
    doc = load_html(built_site)

    # Assert - body should exist and have expected structure
    body = get_by_tag_name(doc, "body")
    assert body is not None

    # Header should exist
    header = get_by_tag_name(doc, "header")
    assert header is not None

    # Should have aside and main elements (they might be in a grid div or directly in body)
    aside = get_by_tag_name(doc, "aside")
    assert aside is not None

    main = get_by_tag_name(doc, "main")
    assert main is not None

    # Main should contain content (h1 should be present on home page)
    h1 = get_by_tag_name(main, "h1")
    assert h1 is not None

    # Footer should exist
    footer = get_by_tag_name(doc, "footer")
    assert footer is not None


@pytest.mark.slow
def test_story_page_layout_elements_visible(built_site: Path) -> None:
    """Story page should have visible aside and main elements."""
    # Arrange - find a story page (look for components/*/story-* structure)
    story_path = None
    for section_dir in built_site.iterdir():
        if section_dir.is_dir() and section_dir.name != "static":
            for subject_dir in section_dir.iterdir():
                if subject_dir.is_dir():
                    for story_dir in subject_dir.iterdir():
                        if story_dir.is_dir() and "story-" in story_dir.name:
                            index_file = story_dir / "index.html"
                            if index_file.exists():
                                story_path = index_file.relative_to(built_site)
                                break
                    if story_path:
                        break
            if story_path:
                break

    if not story_path:
        pytest.skip("No story page found in built site")

    doc = load_html(built_site, str(story_path))

    # Assert - both aside and main should exist
    aside = get_by_tag_name(doc, "aside")
    assert aside is not None

    main = get_by_tag_name(doc, "main")
    assert aside is not None

    # Verify aside contains navigation
    nav = get_by_tag_name(aside, "nav")
    assert nav is not None

    # Main should exist and have content - that's sufficient
    assert main is not None


@pytest.mark.slow
def test_static_assets_load_correctly_at_root(built_site: Path) -> None:
    """Static assets should load correctly from root-level pages."""
    # Arrange & Act
    doc = load_html(built_site)

    # Assert - CSS should be loaded (check for link elements with correct paths)
    all_links = query_all_by_tag_name(doc, "link")
    stylesheet_link = None
    for link in all_links:
        href = link.attrs.get("href", "") or ""
        if link.attrs.get("rel") == "stylesheet" and "static" in href:
            stylesheet_link = link
            break

    assert stylesheet_link is not None, (
        "Should have a stylesheet link with static in href"
    )

    # Verify the href doesn't start with ../ (which would go outside output_dir)
    href = stylesheet_link.attrs.get("href")
    assert href is not None
    assert not href.startswith("../"), (
        f"Root page should not use ../ prefix, got: {href}"
    )

    # Should start with static/ or ./static/
    assert href.startswith("static/") or href.startswith("./static/"), (
        f"Expected static/ or ./static/ prefix, got: {href}"
    )


@pytest.mark.slow
def test_static_assets_load_correctly_at_depth_1(built_site: Path) -> None:
    """Static assets should load correctly from depth-1 pages."""
    # Arrange - load a depth-1 page (section page) - find any section
    section_path = None
    for item in built_site.iterdir():
        if item.is_dir() and item.name != "static":
            index_file = item / "index.html"
            if index_file.exists():
                section_path = index_file.relative_to(built_site)
                break

    if not section_path:
        pytest.skip("No section page found in built site")

    doc = load_html(built_site, str(section_path))

    # Assert - CSS should be loaded with correct relative path
    all_links = query_all_by_tag_name(doc, "link")
    stylesheet_link = None
    for link in all_links:
        href = link.attrs.get("href", "") or ""
        if link.attrs.get("rel") == "stylesheet" and "static" in href:
            stylesheet_link = link
            break

    assert stylesheet_link is not None

    # For depth-1 page (sections at root), should use ../static/
    href = stylesheet_link.attrs.get("href")
    assert href is not None
    assert href.startswith("../static/"), (
        f"Section page should use ../static/ prefix, got: {href}"
    )


@pytest.mark.slow
def test_static_assets_load_correctly_at_depth_2(built_site: Path) -> None:
    """Static assets should load correctly from depth-2 pages (subject level)."""
    # Arrange - load a depth-2 page (subject page) - find any subject
    subject_path = None
    for section_dir in built_site.iterdir():
        if section_dir.is_dir() and section_dir.name != "static":
            for subject_dir in section_dir.iterdir():
                if subject_dir.is_dir():
                    index_file = subject_dir / "index.html"
                    if index_file.exists():
                        subject_path = index_file.relative_to(built_site)
                        break
            if subject_path:
                break

    if not subject_path:
        pytest.skip("No subject page found in built site")

    doc = load_html(built_site, str(subject_path))

    # Assert - CSS should be loaded with correct relative path
    all_links = query_all_by_tag_name(doc, "link")
    stylesheet_link = None
    for link in all_links:
        href = link.attrs.get("href", "") or ""
        if link.attrs.get("rel") == "stylesheet" and "static" in href:
            stylesheet_link = link
            break

    assert stylesheet_link is not None

    # For depth-2 page, should use ../../static/
    href = stylesheet_link.attrs.get("href")
    assert href is not None
    assert href.startswith("../../static/"), (
        f"Subject page should use ../../static/ prefix, got: {href}"
    )
