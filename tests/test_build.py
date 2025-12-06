"""Build a Storyville catalog to a tmpdir and test.

These tests will be testing the Storyville UI itself using
the stories written for that UI.
"""

from pathlib import Path

import pytest
from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name
from storyville.build import build_catalog
from tdom import Node
from tdom.parser import parse_html


# Do this at the session scope. We want just one build of all the stories,
# with small tests for each part.
@pytest.fixture(scope="session")
def output_dir(tmpdir_factory) -> Path:
    output_dir = Path(tmpdir_factory.getbasetemp())
    build_catalog(package_location="examples.minimal", output_dir=output_dir)
    return output_dir


def get_page(page_path: Path) -> Node:
    with open(page_path) as f:
        html_string = f.read()
        return parse_html(html_string)


def test_index(output_dir: Path) -> None:
    """Render the index page with catalog title."""

    page = get_page(output_dir / "index.html")
    # CatalogView renders the catalog title in h1
    h1 = get_by_tag_name(page, "h1")
    assert get_text_content(h1) == "Minimal Catalog"


def test_static_css(output_dir: Path) -> None:
    """Confirm that the chosen CSS file made it to the build dir."""

    # Static assets from storyville core should be in single static/ directory with paths preserved
    assert (output_dir / "static").exists()
    pico_file = (
        output_dir / "static" / "components" / "layout" / "static" / "pico-main.css"
    )
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
    assert get_text_content(h1) == "About Storyville"


def test_debug_page_created(output_dir: Path) -> None:
    """Test that debug.html is created in the output directory."""
    debug_page = output_dir / "debug.html"
    assert debug_page.exists()


def test_debug_page_content(output_dir: Path) -> None:
    """Test that debug page has correct content."""
    page = get_page(output_dir / "debug.html")
    h1 = get_by_tag_name(page, "h1")
    assert get_text_content(h1) == "Debug Information"


def test_stylesheet_path_at_catalog_root(output_dir: Path) -> None:
    """Test stylesheet path is correct at catalog root (depth=0)."""
    page = get_page(output_dir / "index.html")

    # Get link elements
    head = get_by_tag_name(page, "head")
    links = query_all_by_tag_name(head, "link", attrs={"rel": "stylesheet"})

    # Verify hrefs are correct for depth=0 (root level) with nested path structure
    hrefs = [link.attrs.get("href") for link in links]
    assert (
        "static/components/layout/static/pico-main.css" in hrefs
    )  # No ../ prefix for root pages
    assert "static/components/layout/static/storyville.css" in hrefs


def test_stylesheet_path_at_section_depth(output_dir: Path) -> None:
    """Test stylesheet path is correct at section depth (depth=1)."""
    section_page = output_dir / "components" / "index.html"
    page = get_page(section_page)

    # Get link elements
    head = get_by_tag_name(page, "head")
    links = query_all_by_tag_name(head, "link", attrs={"rel": "stylesheet"})

    # Verify hrefs are correct for depth=1 (one directory deep)
    hrefs = [link.attrs.get("href") for link in links]
    assert "../static/components/layout/static/pico-main.css" in hrefs
    assert "../static/components/layout/static/storyville.css" in hrefs


def test_stylesheet_path_at_subject_depth(output_dir: Path) -> None:
    """Test stylesheet path is correct at subject depth (depth=2)."""
    subject_page = output_dir / "components" / "heading" / "index.html"
    page = get_page(subject_page)

    # Get link elements
    head = get_by_tag_name(page, "head")
    links = query_all_by_tag_name(head, "link", attrs={"rel": "stylesheet"})

    # Verify hrefs are correct for depth=2 (two directories deep)
    hrefs = [link.attrs.get("href") for link in links]
    assert "../../static/components/layout/static/pico-main.css" in hrefs
    assert "../../static/components/layout/static/storyville.css" in hrefs


def test_output_dir_cleared_before_build(tmp_path: Path) -> None:
    """Test that output directory is cleared before building."""
    # Create a file in the output directory
    (tmp_path / "old_file.txt").write_text("old content")

    # Build the catalog
    build_catalog(package_location="examples.minimal", output_dir=tmp_path)

    # Verify old file is gone
    assert not (tmp_path / "old_file.txt").exists()

    # Verify new files exist
    assert (tmp_path / "index.html").exists()
    assert (tmp_path / "static").exists()


def test_storyville_static_directory_structure(output_dir: Path) -> None:
    """Test that storyville static assets are in single static/ directory with path preservation."""
    # Check that static/ directory exists
    static_dir = output_dir / "static"
    assert static_dir.exists()

    # Verify specific assets exist with preserved path structure
    assert (static_dir / "components" / "layout" / "static" / "pico-main.css").exists()
    assert (static_dir / "components" / "layout" / "static" / "storyville.css").exists()


def test_static_directory_contains_layout_assets(output_dir: Path) -> None:
    """Test that static/ directory contains layout assets."""
    # The static/ directory should exist and contain layout assets with path preservation
    static_dir = output_dir / "static"
    assert static_dir.exists()

    # Verify it contains layout assets with preserved paths
    assert (static_dir / "components" / "layout" / "static" / "pico-main.css").exists()
    assert (static_dir / "components" / "layout" / "static" / "storyville.css").exists()


def test_static_assets_phase_logs(output_dir: Path, caplog) -> None:
    """Test that static assets discovery and copying is logged."""
    # Build again to capture logs
    import logging

    caplog.set_level(logging.INFO)

    tmp_output = output_dir.parent / "test_logging"
    tmp_output.mkdir(exist_ok=True)

    build_catalog(package_location="examples.minimal", output_dir=tmp_output)

    # Check that static assets phase is logged
    assert any("Phase Static Assets" in record.message for record in caplog.records)
