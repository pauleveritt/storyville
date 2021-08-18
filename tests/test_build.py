"""Build a Storytime site to a tmpdir and test."""
from pathlib import Path

from bs4 import BeautifulSoup

from storytime.build import build_site


def test_index(tmpdir: Path) -> None:
    """Render the index page."""

    build_site(package_location="storytime", output_dir=tmpdir)

    with open(tmpdir / "index.html") as f:
        rendered = f.read()
        soup = BeautifulSoup(rendered, "html.parser")
        expected = "Welcome to Storytime. Choose a component on the left."
        assert soup.select_one("main p").text == expected
