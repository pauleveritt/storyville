"""Temporary site until getting the cmd args right."""

from livereload import Server
from livereload import shell


def main() -> None:
    """Start the server and watch for reloads."""
    server = Server()
    server.watch(
        "src/storytime/**/*.py",
        shell(".venv/bin/python -m storytime")
    )
    server.serve(root="var")


if __name__ == "__main__":
    main()  # pragma: no cover
