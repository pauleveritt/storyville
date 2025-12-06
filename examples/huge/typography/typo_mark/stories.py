"""The subject for the TypoMark component."""

from examples.huge.typography.typo_mark.typo_mark import TypoMark
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for TypoMark component."""
    return Subject(
        title="Typo Mark",
        description="Marked text",
        target=TypoMark,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
