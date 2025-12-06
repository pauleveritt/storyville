"""The subject for the MediaEmbed component."""

from examples.huge.media.media_embed.media_embed import MediaEmbed
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for MediaEmbed component."""
    return Subject(
        title="Media Embed",
        description="Embedded media",
        target=MediaEmbed,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
