"""The subject for the MediaImage component."""

from examples.huge.media.media_image.media_image import MediaImage
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for MediaImage component."""
    return Subject(
        title="Media Image",
        description="Image display",
        target=MediaImage,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
