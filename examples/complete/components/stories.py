"""The Components section for the complete example."""


from storyville import Section


def this_section() -> Section:
    """Let's make a Storyville section for Components."""
    return Section(
        title="Components Collection",
        description="A collection of component examples with all optional fields populated",
    )
