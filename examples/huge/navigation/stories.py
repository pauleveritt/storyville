"""The Navigation section for the huge example."""


from storyville import Section


def this_section() -> Section:
    """Navigation section with navigation components."""
    return Section(
        title="Navigation",
        description="Navigation components",
    )
