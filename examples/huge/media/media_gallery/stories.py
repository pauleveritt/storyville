"""The subject for the MediaGallery component."""

from examples.huge.media.media_gallery.media_gallery import MediaGallery
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for MediaGallery component."""
    return Subject(
        title="Media Gallery",
        description="Image gallery",
        target=MediaGallery,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
