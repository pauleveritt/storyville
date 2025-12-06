"""The subject for the MediaImage component."""

from examples.huge_assertions.media.media_image.media_image import MediaImage
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for MediaImage component."""
    return Subject(
        title="Media Image",
        description="Image display",
        target=MediaImage,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if (el is not None and str(el)) else (_ for _ in ()).throw(AssertionError("Invalid element")), lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags")), lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if "class" in str(el).lower() or "div" in str(el).lower() else (_ for _ in ()).throw(AssertionError("No class or div found"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
