"""The Components section for the complete example."""

from __future__ import annotations

from storytime import Section


def this_section() -> Section:
    """Let's make a Storytime section for Components."""
    return Section(
        title="Components Collection",
        description="A collection of component examples with all optional fields populated",
    )
