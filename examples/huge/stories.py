"""The Catalog for the huge example package."""

from storyville import Catalog


def this_catalog() -> Catalog:
    """The top of this package's story catalog."""
    return Catalog(
        title="Huge Scale Example",
    )
