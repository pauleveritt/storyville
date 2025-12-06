"""The Feedback section for the huge example."""

from storyville import Section


def this_section() -> Section:
    """Feedback section with feedback components."""
    return Section(
        title="Feedback",
        description="Feedback components",
    )
