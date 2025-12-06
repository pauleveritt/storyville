"""The subject for the MediaCarousel component."""

from examples.huge.media.media_carousel.media_carousel import MediaCarousel
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for MediaCarousel component."""
    return Subject(
        title="Media Carousel",
        description="Image carousel",
        target=MediaCarousel,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
