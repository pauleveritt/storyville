"""The subject for the DataCard component."""

from examples.huge.data_display.data_card.data_card import DataCard
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for DataCard component."""
    return Subject(
        title="Data Card",
        description="Card for data",
        target=DataCard,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
