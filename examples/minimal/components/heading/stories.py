"""The subject for this Heading component."""

from examples.minimal.components.heading.heading import Heading
from storytime import Story, Subject


def this_subject() -> Subject:
    """Let's make a Storytime subject for this Heading component."""
    return Subject(
        title="Heading",
        description="A Heading component that says hello to a name",
        target=Heading,
        items=[
            Story(props=dict(name="88World")),
        ],
    )
