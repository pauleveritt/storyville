"""The subject for the MediaAudio component."""

from examples.huge.media.media_audio.media_audio import MediaAudio
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for MediaAudio component."""
    return Subject(
        title="Media Audio",
        description="Audio player",
        target=MediaAudio,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
