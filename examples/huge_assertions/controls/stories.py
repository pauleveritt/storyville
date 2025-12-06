"""The Controls section for the huge example."""


from storyville import Section


def this_section() -> Section:
    """Controls section with control components."""
    return Section(
        title="Controls",
        description="Control components",
    )
