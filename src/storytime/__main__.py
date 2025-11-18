"""Command-line interface."""

import logging
from pathlib import Path
from tempfile import TemporaryDirectory

import typer
import uvicorn

from storytime.app import create_app
from storytime.build import build_site

app = typer.Typer()


@app.command()
def serve(
    input_path: str = typer.Argument(
        "storytime",
        help="Path to the package to serve (default: 'storytime')",
    ),
    output_dir_arg: str | None = typer.Argument(
        None,
        help="Output directory for the built site (default: temporary directory)",
    ),
    use_subinterpreters: bool = typer.Option(
        True,
        "--use-subinterpreters/--no-use-subinterpreters",
        help=(
            "Enable subinterpreters for hot reload builds. "
            "When enabled, each rebuild runs in a fresh isolated subinterpreter, "
            "allowing module changes (e.g., to stories.py) to take effect immediately. "
            "Default: True (use subinterpreters for proper hot reload)."
        ),
    ),
) -> None:
    """Start a development server for the Storytime site.

    The server provides hot reload functionality - when source files change,
    the site is automatically rebuilt and the browser is refreshed.

    By default, rebuilds run directly in the main interpreter. Use the
    --use-subinterpreters flag to enable isolated subinterpreters for each
    rebuild, which allows module changes to take effect without restarting
    the server.
    """
    # Configure logging for storytime modules to show watcher events
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s:     %(name)s - %(message)s",
    )

    def run_server(output_dir: Path) -> None:
        """Run the server with the given output directory."""
        typer.echo(f"Building site from '{input_path}' to '{output_dir}'...")
        build_site(package_location=input_path, output_dir=output_dir)
        typer.echo("Build complete! Starting server on http://localhost:8080")
        typer.echo(f"Serving from: {output_dir}")

        if use_subinterpreters:
            typer.echo("Hot reload using subinterpreters: enabled")
        else:
            typer.echo("Hot reload using direct builds: enabled")

        # Create and run the app with hot reload support
        # Pass input_path, package_location, and output_dir to enable watchers
        starlette_app = create_app(
            path=output_dir,
            input_path=input_path,
            package_location=input_path,
            output_dir=output_dir,
            use_subinterpreters=use_subinterpreters,
        )
        try:
            # Note: Do NOT use reload=True - we have custom file watching
            uvicorn.run(starlette_app, port=8080, log_level="info")
        except KeyboardInterrupt:
            print("Server ceasing operations. Cheerio!")

    # Use provided output directory or temporary directory
    if output_dir_arg:
        output_dir = Path(output_dir_arg).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        run_server(output_dir)
    else:
        # Use temporary directory (will be cleaned up automatically)
        with TemporaryDirectory() as tmpdir:
            run_server(Path(tmpdir))


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
    """Build the Storytime site to static files.

    The build command performs a one-time build without starting a server.
    It always uses direct builds (no subinterpreters) for maximum simplicity
    and performance.

    For development with hot reload, use the 'serve' command instead.
    """
    # Configure logging to show build phase timing
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s:     %(name)s - %(message)s",
    )

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
