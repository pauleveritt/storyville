"""Command-line interface."""
from pathlib import Path

import click

from storytime.build import build_site


def rebuild_site() -> None:
    """Called by livereload whenever anything changes."""


@click.command()
@click.version_option()
def main() -> None:
    """Storytime main entry point."""
    package_location = "storytime"
    output_dir = Path("var")
    build_site(package_location=package_location, output_dir=output_dir)


if __name__ == "__main__":
    main(prog_name="storytime")  # pragma: no cover
