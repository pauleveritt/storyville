"""The Catalog for the templates example."""

from storyville import Catalog


def this_catalog() -> Catalog:
    """The top of this package's story catalog."""
    return Catalog(
        title="Templates Example",
    )
