"""The subject for the TypoText component."""

from examples.huge.typography.typo_text.typo_text import TypoText
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for TypoText component."""
    return Subject(
        title="Typo Text",
        description="Body text",
        target=TypoText,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
