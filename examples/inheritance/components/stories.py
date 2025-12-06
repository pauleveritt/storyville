"""Section for the inheritance example."""


from storyville import Section


def this_section() -> Section:
    """Section containing card components."""
    return Section(
        title="Card Components",
        description="Components demonstrating field inheritance patterns",
    )
