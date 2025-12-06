"""The subject for this Heading component."""

from examples.minimal.components.heading.heading import Heading
from storyville import Story, Subject


def this_subject() -> Subject:
    """Let's make a Storyville subject for this Heading component."""

    def failing_assertion(el):
        """This assertion will fail."""
        assert 1 == 12, "1 should equal 12 (it doesn't)"

    return Subject(
        title="Heading",
        description="A Heading component that says hello to a name",
        target=Heading,
        items=[
            Story(props=dict(name="World"), assertions=[failing_assertion]),
        ],
    )
