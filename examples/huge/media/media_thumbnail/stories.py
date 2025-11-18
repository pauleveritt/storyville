"""The subject for the MediaThumbnail component."""

from examples.huge.media.media_thumbnail.media_thumbnail import MediaThumbnail
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for MediaThumbnail component."""
    return Subject(
        title="Media Thumbnail",
        description="Thumbnail display",
        target=MediaThumbnail,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
