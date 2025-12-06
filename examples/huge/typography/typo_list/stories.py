"""The subject for the TypoList component."""

from examples.huge.typography.typo_list.typo_list import TypoList
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for TypoList component."""
    return Subject(
        title="Typo List",
        description="List display",
        target=TypoList,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
