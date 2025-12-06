"""The Forms section for the huge example."""

from storyville import Section


def this_section() -> Section:
    """Forms section with form components."""
    return Section(
        title="Forms",
        description="Form components",
    )
