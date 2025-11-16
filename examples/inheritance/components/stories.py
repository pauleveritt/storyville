"""Section for the inheritance example."""

from __future__ import annotations

from storytime import Section


def this_section() -> Section:
    """Section containing card components."""
    return Section(
        title="Card Components",
        description="Components demonstrating field inheritance patterns",
    )
