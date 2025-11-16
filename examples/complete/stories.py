"""The Site for the complete example package."""

from __future__ import annotations

from storytime import Site


def this_site() -> Site:
    """The top of this package's story catalog."""
    return Site(
        title="Complete Example",
    )
