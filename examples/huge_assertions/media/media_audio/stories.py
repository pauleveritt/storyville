"""The subject for the MediaAudio component."""

from examples.huge_assertions.media.media_audio.media_audio import MediaAudio
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for MediaAudio component."""
    return Subject(
        title="Media Audio",
        description="Audio player",
        target=MediaAudio,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if (el is not None and str(el)) else (_ for _ in ()).throw(AssertionError("Invalid element"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
