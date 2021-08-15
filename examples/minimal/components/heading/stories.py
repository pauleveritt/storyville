"""The subject for this Heading component."""
from storytime import Story
from storytime import Subject


def this_subject() -> Subject:
    """Let's make a Storytime subject for this Heading component."""
    return Subject(
        title="Heading",
        stories=[
            Story(),
        ],
    )
