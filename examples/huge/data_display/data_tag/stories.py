"""The subject for the DataTag component."""

from examples.huge.data_display.data_tag.data_tag import DataTag
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for DataTag component."""
    return Subject(
        title="Data Tag",
        description="Tag for data",
        target=DataTag,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
