"""The subject for the LayoutCard component."""

from examples.huge.layout.layout_card.layout_card import LayoutCard
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for LayoutCard component."""
    return Subject(
        title="Layout Card",
        description="Card container",
        target=LayoutCard,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
