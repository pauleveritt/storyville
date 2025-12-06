"""The subject for the MediaIcon component."""

from examples.huge.media.media_icon.media_icon import MediaIcon
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for MediaIcon component."""
    return Subject(
        title="Media Icon",
        description="Icon display",
        target=MediaIcon,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
