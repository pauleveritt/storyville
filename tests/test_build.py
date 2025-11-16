"""Build a Storytime site to a tmpdir and test.

These tests will be testing the Storytime UI itself using
the stories written for that UI.
"""

from pathlib import Path

import pytest
from aria_testing import get_by_tag_name, get_text_content
from storytime.build import build_site
from tdom import Node
from tdom.parser import parse_html


# Do this at the session scope. We want just one build of all the stories,
# with small tests for each part.
@pytest.fixture(scope="session")
def output_dir(tmpdir_factory) -> Path:
    output_dir = Path(tmpdir_factory.getbasetemp())
    build_site(package_location="storytime", output_dir=output_dir)
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
    assert get_text_content(h1) == "Storytime UI"


def test_static_css(output_dir: Path) -> None:
    """Confirm that the chosen CSS file made it to the build dir."""

    assert (output_dir / "static").exists()
    bulma_file = output_dir / "static" / "bulma.css"
    assert bulma_file.exists()
    bulma_text = bulma_file.read_text()
    assert "bulma.io" in bulma_text


def test_section_page(output_dir: Path) -> None:
    """Test that section pages are rendered correctly."""
    # Check that components section exists
    section_page = output_dir / "section" / "components" / "index.html"
    assert section_page.exists()

    # Parse and verify content
    page = get_page(section_page)
    h1 = get_by_tag_name(page, "h1")
    assert get_text_content(h1) == "Components"


def test_subject_page(output_dir: Path) -> None:
    """Test that subject pages are rendered correctly."""
    # Check that a subject page exists (e.g., components/component_view)
    subject_page = output_dir / "section" / "components" / "component_view" / "index.html"
    assert subject_page.exists()

    # Parse and verify content
    page = get_page(subject_page)
    h1 = get_by_tag_name(page, "h1")
    # Subject title should be in the h1
    assert get_text_content(h1) == "Component View"


def test_stylesheet_path_at_site_root(output_dir: Path) -> None:
    """Test stylesheet path is correct at site root (depth=0)."""
    page = get_page(output_dir / "index.html")

    # Get link element
    head = get_by_tag_name(page, "head")
    link = get_by_tag_name(head, "link", attrs={"rel": "stylesheet"})

    # Verify href is correct for depth=0 (../static/bulma.css)
    href = link.attrs.get("href")
    assert href == "../static/bulma.css"


def test_stylesheet_path_at_section_depth(output_dir: Path) -> None:
    """Test stylesheet path is correct at section depth (depth=1)."""
    section_page = output_dir / "section" / "components" / "index.html"
    page = get_page(section_page)

    # Get link element
    head = get_by_tag_name(page, "head")
    link = get_by_tag_name(head, "link", attrs={"rel": "stylesheet"})

    # Verify href is correct for depth=1 (../../static/bulma.css)
    href = link.attrs.get("href")
    assert href == "../../static/bulma.css"


def test_stylesheet_path_at_subject_depth(output_dir: Path) -> None:
    """Test stylesheet path is correct at subject depth (depth=2)."""
    subject_page = output_dir / "section" / "components" / "component_view" / "index.html"
    page = get_page(subject_page)

    # Get link element
    head = get_by_tag_name(page, "head")
    link = get_by_tag_name(head, "link", attrs={"rel": "stylesheet"})

    # Verify href is correct for depth=2 (../../../static/bulma.css)
    href = link.attrs.get("href")
    assert href == "../../../static/bulma.css"


def test_output_dir_cleared_before_build(tmp_path: Path) -> None:
    """Test that output directory is cleared before building."""
    # Create a file in the output directory
    (tmp_path / "old_file.txt").write_text("old content")

    # Build the site
    build_site(package_location="storytime", output_dir=tmp_path)

    # Verify old file is gone
    assert not (tmp_path / "old_file.txt").exists()

    # Verify new files exist
    assert (tmp_path / "index.html").exists()
    assert (tmp_path / "static").exists()
