"""The subject for this Heading component."""
from examples.scannables import components
from examples.scannables.components.heading import Heading

from storytime import Story
from storytime import Subject


def this_subject() -> Subject:
    """Let's make a Storytime subject for this Heading component."""
    assert Heading
    return Subject(
        title="Heading",
        scannables=[
            components,
        ],
        stories=[
            Story(
                title="Default Heading",
                component=Heading,
            ),
        ],
    )
