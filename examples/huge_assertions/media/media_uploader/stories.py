"""The subject for the MediaUploader component."""

from examples.huge_assertions.media.media_uploader.media_uploader import MediaUploader
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for MediaUploader component."""
    return Subject(
        title="Media Uploader",
        description="Media uploader",
        target=MediaUploader,
        items=[
            Story(
                props=dict(text="Default", variant="primary", state="default"),
                assertions=[
                    lambda el: None
                    if el is not None
                    else (_ for _ in ()).throw(AssertionError("Element is None"))
                ],
            ),
            Story(
                props=dict(text="Disabled", variant="secondary", state="disabled"),
                assertions=[
                    lambda el: None
                    if el is not None
                    else (_ for _ in ()).throw(AssertionError("Element is None"))
                ],
            ),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
