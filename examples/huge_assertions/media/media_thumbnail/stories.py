"""The subject for the MediaThumbnail component."""

from examples.huge_assertions.media.media_thumbnail.media_thumbnail import MediaThumbnail
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for MediaThumbnail component."""
    return Subject(
        title="Media Thumbnail",
        description="Thumbnail display",
        target=MediaThumbnail,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if len(str(el)) > 10 else (_ for _ in ()).throw(AssertionError("Element too short"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if "class" in str(el).lower() or "div" in str(el).lower() else (_ for _ in ()).throw(AssertionError("No class or div found"))]),
        ],
    )
