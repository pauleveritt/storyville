"""The Layout section for the huge example."""


from storyville import Section


def this_section() -> Section:
    """Layout section with layout components."""
    return Section(
        title="Layout",
        description="Layout components",
    )
