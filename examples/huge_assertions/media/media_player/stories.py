"""The subject for the MediaPlayer component."""

from examples.huge_assertions.media.media_player.media_player import MediaPlayer
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for MediaPlayer component."""
    return Subject(
        title="Media Player",
        description="Media player",
        target=MediaPlayer,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if (el is not None and str(el)) else (_ for _ in ()).throw(AssertionError("Invalid element")), lambda el: None if hasattr(el, "__html__") else (_ for _ in ()).throw(AssertionError("Missing __html__ attribute"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found"))]),
        ],
    )
