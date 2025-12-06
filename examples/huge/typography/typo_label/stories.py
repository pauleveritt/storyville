"""The subject for the TypoLabel component."""

from examples.huge.typography.typo_label.typo_label import TypoLabel
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for TypoLabel component."""
    return Subject(
        title="Typo Label",
        description="Label text",
        target=TypoLabel,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
