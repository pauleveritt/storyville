"""The Catalog for the no_sections example."""

from storyville import Catalog


def this_catalog() -> Catalog:
    """A catalog with no sections to demonstrate Sections are optional."""
    return Catalog(
        title="No Sections Catalog",
    )
