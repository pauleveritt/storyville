"""The Site for the templates example."""

from storytime import Site


def this_site() -> Site:
    """The top of this package's story catalog."""
    return Site(
        title="Templates Example",
    )
