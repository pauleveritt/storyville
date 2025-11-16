"""Command-line interface."""


from pathlib import Path

import typer
import uvicorn

from storytime import make_site
from storytime.app import create_app
from storytime.build import build_site

app = typer.Typer()


@app.command()
def serve(
    input_path: str = typer.Argument(
        "storytime",
        help="Path to the package to serve (default: 'storytime')",
    ),
) -> None:
    """Start a development server for the Storytime site."""
    site = make_site(package_location=input_path)
    starlette_app = create_app(site)
    try:
        uvicorn.run(starlette_app, port=8080, log_level="info")
    except KeyboardInterrupt:
        print("Server ceasing operations. Cheerio!")


@app.command()
def build(
    input_path: str = typer.Argument(
        ...,
        help="Package location to build (e.g., 'storytime' or a dotted package path)",
    ),
    output_dir: str = typer.Argument(
        ...,
        help="Output directory for the built site",
    ),
) -> None:
    """Build the Storytime site to static files."""
    # Convert output_dir to Path object
    output_p = Path(output_dir).resolve()

    # Build the site
    typer.echo(f"Building site from '{input_path}' to '{output_p}'...")
    build_site(package_location=input_path, output_dir=output_p)
    typer.echo("Build complete!")


def main() -> None:
    """Storytime main entry point."""
    app()


if __name__ == "__main__":
    main()  # pragma: no cover
