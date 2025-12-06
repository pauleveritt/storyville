"""The subject for the MediaVideo component."""

from examples.huge_assertions.media.media_video.media_video import MediaVideo
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for MediaVideo component."""
    return Subject(
        title="Media Video",
        description="Video player",
        target=MediaVideo,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None")), lambda el: None if "class" in str(el).lower() or "div" in str(el).lower() else (_ for _ in ()).throw(AssertionError("No class or div found"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if "class" in str(el).lower() or "div" in str(el).lower() else (_ for _ in ()).throw(AssertionError("No class or div found")), lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None"))]),
        ],
    )
