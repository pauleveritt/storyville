"""The subject for the MediaUploader component."""

from examples.huge.media.media_uploader.media_uploader import MediaUploader
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for MediaUploader component."""
    return Subject(
        title="Media Uploader",
        description="Media uploader",
        target=MediaUploader,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
