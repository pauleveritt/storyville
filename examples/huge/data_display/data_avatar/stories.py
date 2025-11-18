"""The subject for the DataAvatar component."""

from examples.huge.data_display.data_avatar.data_avatar import DataAvatar
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for DataAvatar component."""
    return Subject(
        title="Data Avatar",
        description="Avatar display",
        target=DataAvatar,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
