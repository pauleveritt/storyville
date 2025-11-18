"""The subject for the TypoEmphasis component."""

from examples.huge.typography.typo_emphasis.typo_emphasis import TypoEmphasis
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for TypoEmphasis component."""
    return Subject(
        title="Typo Emphasis",
        description="Emphasized text",
        target=TypoEmphasis,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
