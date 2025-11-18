"""The subject for the MediaGallery component."""

from examples.huge_assertions.media.media_gallery.media_gallery import MediaGallery
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for MediaGallery component."""
    return Subject(
        title="Media Gallery",
        description="Image gallery",
        target=MediaGallery,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if hasattr(el, "__html__") else (_ for _ in ()).throw(AssertionError("Missing __html__ attribute")), lambda el: None if (el is not None and str(el)) else (_ for _ in ()).throw(AssertionError("Invalid element"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if (el is not None and str(el)) else (_ for _ in ()).throw(AssertionError("Invalid element"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found"))]),
        ],
    )
