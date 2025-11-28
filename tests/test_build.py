"""Build a Storytime site to a tmpdir and test.

These tests will be testing the Storytime UI itself using
the stories written for that UI.
"""

from pathlib import Path

import pytest
from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name
from storytime.build import build_site
from tdom import Node
from tdom.parser import parse_html


# Do this at the session scope. We want just one build of all the stories,
# with small tests for each part.
@pytest.fixture(scope="session")
def output_dir(tmpdir_factory) -> Path:
    output_dir = Path(tmpdir_factory.getbasetemp())
    build_site(package_location="examples.minimal", output_dir=output_dir)
    return output_dir


def get_page(page_path: Path) -> Node:
    with open(page_path) as f:
        html_string = f.read()
        return parse_html(html_string)


def test_index(output_dir: Path) -> None:
    """Render the index page with site title."""

    page = get_page(output_dir / "index.html")
    # SiteView renders the site title in h1
    h1 = get_by_tag_name(page, "h1")
    assert get_text_content(h1) == "Minimal Site"


def test_static_css(output_dir: Path) -> None:
    """Confirm that the chosen CSS file made it to the build dir."""

    # Static assets from storytime core should be in storytime_static/
    assert (output_dir / "storytime_static").exists()
    pico_file = output_dir / "storytime_static" / "components" / "layout" / "static" / "pico-main.css"
    assert pico_file.exists()
    pico_text = pico_file.read_text()
    assert "pico" in pico_text


def test_section_page(output_dir: Path) -> None:
    """Test that section pages are rendered correctly."""
    # Check that components section exists
    section_page = output_dir / "components" / "index.html"
    assert section_page.exists()

    # Parse and verify content
    page = get_page(section_page)
    h1 = get_by_tag_name(page, "h1")
    assert get_text_content(h1) == "Components"


def test_subject_page(output_dir: Path) -> None:
    """Test that subject pages are rendered correctly."""
    # Check that a subject page exists (e.g., components/heading)
    subject_page = output_dir / "components" / "heading" / "index.html"
    assert subject_page.exists()

    # Parse and verify content
    page = get_page(subject_page)
    h1 = get_by_tag_name(page, "h1")
    # Subject title should be in the h1
    assert get_text_content(h1) == "Heading"


def test_about_page_created(output_dir: Path) -> None:
    """Test that about.html is created in the output directory."""
    about_page = output_dir / "about.html"
    assert about_page.exists()


def test_about_page_content(output_dir: Path) -> None:
    """Test that about page has correct content."""
    page = get_page(output_dir / "about.html")
    h1 = get_by_tag_name(page, "h1")
    assert get_text_content(h1) == "About Storytime"


def test_debug_page_created(output_dir: Path) -> None:
    """Test that debug.html is created in the output directory."""
    debug_page = output_dir / "debug.html"
    assert debug_page.exists()


def test_debug_page_content(output_dir: Path) -> None:
    """Test that debug page has correct content."""
    page = get_page(output_dir / "debug.html")
    h1 = get_by_tag_name(page, "h1")
    assert get_text_content(h1) == "Debug Information"


def test_stylesheet_path_at_site_root(output_dir: Path) -> None:
    """Test stylesheet path is correct at site root (depth=0)."""
    page = get_page(output_dir / "index.html")

    # Get link elements
    head = get_by_tag_name(page, "head")
    links = query_all_by_tag_name(head, "link", attrs={"rel": "stylesheet"})

    # Verify hrefs are correct for depth=0 with new storytime_static/ structure
    hrefs = [link.attrs.get("href") for link in links]
    assert "../storytime_static/components/layout/static/pico-main.css" in hrefs
    assert "../storytime_static/components/layout/static/storytime.css" in hrefs


def test_stylesheet_path_at_section_depth(output_dir: Path) -> None:
    """Test stylesheet path is correct at section depth (depth=1)."""
    section_page = output_dir / "components" / "index.html"
    page = get_page(section_page)

    # Get link elements
    head = get_by_tag_name(page, "head")
    links = query_all_by_tag_name(head, "link", attrs={"rel": "stylesheet"})

    # Verify hrefs are correct for depth=0 (sections now at root level)
    hrefs = [link.attrs.get("href") for link in links]
    assert "../storytime_static/components/layout/static/pico-main.css" in hrefs
    assert "../storytime_static/components/layout/static/storytime.css" in hrefs


def test_stylesheet_path_at_subject_depth(output_dir: Path) -> None:
    """Test stylesheet path is correct at subject depth (depth=1)."""
    subject_page = output_dir / "components" / "heading" / "index.html"
    page = get_page(subject_page)

    # Get link elements
    head = get_by_tag_name(page, "head")
    links = query_all_by_tag_name(head, "link", attrs={"rel": "stylesheet"})

    # Verify hrefs are correct for depth=1 (subject pages)
    hrefs = [link.attrs.get("href") for link in links]
    assert "../../storytime_static/components/layout/static/pico-main.css" in hrefs
    assert "../../storytime_static/components/layout/static/storytime.css" in hrefs


def test_output_dir_cleared_before_build(tmp_path: Path) -> None:
    """Test that output directory is cleared before building."""
    # Create a file in the output directory
    (tmp_path / "old_file.txt").write_text("old content")

    # Build the site
    build_site(package_location="examples.minimal", output_dir=tmp_path)

    # Verify old file is gone
    assert not (tmp_path / "old_file.txt").exists()

    # Verify new files exist
    assert (tmp_path / "index.html").exists()
    assert (tmp_path / "storytime_static").exists()


def test_storytime_static_directory_structure(output_dir: Path) -> None:
    """Test that storytime static assets are in storytime_static/ with full path preservation."""
    # Check that storytime_static/ directory exists
    storytime_static = output_dir / "storytime_static"
    assert storytime_static.exists()

    # Check that layout component static assets are in the correct location
    layout_static = storytime_static / "components" / "layout" / "static"
    assert layout_static.exists()

    # Verify specific assets exist
    assert (layout_static / "pico-main.css").exists()
    assert (layout_static / "storytime.css").exists()


def test_no_old_static_directory(output_dir: Path) -> None:
    """Test that old site-level static/ directory no longer exists."""
    # The old static/ directory at root should not exist anymore
    # (unless it's from input_dir, but examples.minimal doesn't have one)
    old_static = output_dir / "static"

    # It might exist if input_dir has static assets, but it should not contain
    # the layout's assets (those should be in storytime_static/)
    if old_static.exists():
        # If it exists, ensure it doesn't have layout assets
        assert not (old_static / "pico-main.css").exists()
        assert not (old_static / "storytime.css").exists()


def test_static_assets_phase_logs(output_dir: Path, caplog) -> None:
    """Test that static assets discovery and copying is logged."""
    # Build again to capture logs
    import logging
    caplog.set_level(logging.INFO)

    tmp_output = output_dir.parent / "test_logging"
    tmp_output.mkdir(exist_ok=True)

    build_site(package_location="examples.minimal", output_dir=tmp_output)

    # Check that static assets phase is logged
    assert any("Phase Static Assets" in record.message for record in caplog.records)
