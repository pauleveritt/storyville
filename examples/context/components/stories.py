"""A section in the example.context site."""
from storytime import Section

context = dict(title="Context Section")


def this_section() -> Section:
    """Let's make a Storytime section for Components."""
    return Section(
        context=context,
        title="Components",
    )
