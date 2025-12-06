"""The subject for the MediaVideo component."""

from examples.huge.media.media_video.media_video import MediaVideo
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for MediaVideo component."""
    return Subject(
        title="Media Video",
        description="Video player",
        target=MediaVideo,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
