"""Section for template components."""

from storytime import Section


def this_section() -> Section:
    """Section containing template demonstration components."""
    return Section(
        title="Template Components",
        description="Components demonstrating custom template usage",
    )
