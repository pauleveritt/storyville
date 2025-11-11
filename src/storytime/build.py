"""Called by the CLI main to build the site to disk."""

from pathlib import Path
from shutil import copytree

from storytime.views.index_view import IndexView
from storytime.stories import make_site


def build_site(package_location: str, output_dir: Path) -> None:
    """Write the static files and story info to the output directory."""

    # Make a site and put it in the registry
    site = make_site(package_location=package_location)

    # Handle the index page
    index_view = IndexView()
    index_html = index_view()
    with open(output_dir / "index.html", "w") as f:
        index_output = str(index_html)
        f.write(index_output)

    # Write the static_dir
    if site.static_dir:
        copytree(site.static_dir, output_dir / "static", dirs_exist_ok=True)
