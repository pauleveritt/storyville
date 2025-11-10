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
    output_dir = tmpdir_factory.getbasetemp()
    build_site(package_location="storytime", output_dir=output_dir)
    return Path(output_dir)


def get_page(page_path: Path) -> Node:
    with open(page_path) as f:
        html_string = f.read()
        return parse_html(html_string)


def test_index(output_dir: Path) -> None:
    """Render the index page."""

    page = get_page(output_dir / "index.html")
    expected = "Welcome to Storytime. Choose a component on the left."
    p = get_by_tag_name(page, "p")
    assert get_text_content(p) == expected


def test_static_css(output_dir: Path) -> None:
    """Confirm that the chosen CSS file made it to the build dir."""

    assert (output_dir / "static").exists()
    bulma_file = output_dir / "static" / "bulma.css"
    assert bulma_file.exists()
    bulma_text = bulma_file.read_text()
    assert "bulma.io" in bulma_text
