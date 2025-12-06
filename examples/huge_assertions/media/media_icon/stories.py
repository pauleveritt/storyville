"""The subject for the MediaIcon component."""

from examples.huge_assertions.media.media_icon.media_icon import MediaIcon
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for MediaIcon component."""
    return Subject(
        title="Media Icon",
        description="Icon display",
        target=MediaIcon,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if (el is not None and str(el)) else (_ for _ in ()).throw(AssertionError("Invalid element"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None"))]),
        ],
    )
