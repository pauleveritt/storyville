"""The subject for this Heading component."""
from ... import components
from . import Heading

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
