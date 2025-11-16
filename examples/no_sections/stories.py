"""The Site for the no_sections example."""

from storytime import Site


def this_site() -> Site:
    """A site with no sections to demonstrate Sections are optional."""
    return Site(
        title="No Sections Site",
    )
