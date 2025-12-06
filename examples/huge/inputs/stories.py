"""The Inputs section for the huge example."""

from storyville import Section


def this_section() -> Section:
    """Inputs section with input components."""
    return Section(
        title="Inputs",
        description="Input components",
    )
