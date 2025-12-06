"""The subject for the TypoHeading component."""

from examples.huge.typography.typo_heading.typo_heading import TypoHeading
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for TypoHeading component."""
    return Subject(
        title="Typo Heading",
        description="Heading text",
        target=TypoHeading,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
