"""The Catalog for the complete example package."""

from storyville import Catalog


def this_catalog() -> Catalog:
    """The top of this package's story catalog."""
    return Catalog(
        title="Complete Example",
    )
