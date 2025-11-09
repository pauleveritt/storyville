"""Called by the CLI main to build the site to disk."""

from pathlib import Path
from shutil import copytree

from storytime.components.index import IndexView
from storytime.stories import make_site


def build_site(package_location: str, output_dir: Path) -> None:
    """Write the static files and story info to the output directory."""

    # Make a site and put it in the registry
    site = make_site(package_location=package_location)
    site.registry.register(site)

    # Handle the index page
    index_view = site.registry.get(IndexView)
    index_html = index_view()
    index_output = render(index_html, registry=site.registry)
    with open(output_dir / "index.html", "w") as f:
        f.write(index_output)

    # Write the static_dir
    if site.static_dir:
        copytree(site.static_dir, output_dir / "static", dirs_exist_ok=True)
