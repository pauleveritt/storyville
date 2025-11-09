"""Command-line interface."""


import click
import uvicorn

from storytime import make_site
from storytime.app import create_app


@click.command()
@click.version_option()
def main() -> None:
    """Storytime main entry point."""
    package_location = "storytime"
    site = make_site(package_location=package_location)

    app = create_app(site)
    try:
        uvicorn.run(app, port=8080, log_level="info")
    except KeyboardInterrupt:
        print("Server ceasing operations. Cheerio!")

    # Later we'll have commands which let you serve vs. build, for now, comment this out
    # build_site(package_location=package_location, output_dir=output_dir)


if __name__ == "__main__":
    main(prog_name="storytime")  # pragma: no cover
