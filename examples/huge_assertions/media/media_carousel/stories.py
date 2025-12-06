"""The subject for the MediaCarousel component."""

from examples.huge_assertions.media.media_carousel.media_carousel import MediaCarousel
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for MediaCarousel component."""
    return Subject(
        title="Media Carousel",
        description="Image carousel",
        target=MediaCarousel,
        items=[
            Story(
                props=dict(text="Default", variant="primary", state="default"),
                assertions=[
                    lambda el: None
                    if hasattr(el, "__html__")
                    else (_ for _ in ()).throw(
                        AssertionError("Missing __html__ attribute")
                    )
                ],
            ),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(
                props=dict(text="Loading", variant="primary", state="loading"),
                assertions=[
                    lambda el: None
                    if (el is not None and str(el))
                    else (_ for _ in ()).throw(AssertionError("Invalid element"))
                ],
            ),
        ],
    )
