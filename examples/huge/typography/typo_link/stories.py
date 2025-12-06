"""The subject for the TypoLink component."""

from examples.huge.typography.typo_link.typo_link import TypoLink
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for TypoLink component."""
    return Subject(
        title="Typo Link",
        description="Link text",
        target=TypoLink,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
