"""The subject for the MediaPlayer component."""

from examples.huge.media.media_player.media_player import MediaPlayer
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for MediaPlayer component."""
    return Subject(
        title="Media Player",
        description="Media player",
        target=MediaPlayer,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
