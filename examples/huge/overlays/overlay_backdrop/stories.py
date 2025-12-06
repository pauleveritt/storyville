"""The subject for the OverlayBackdrop component."""

from examples.huge.overlays.overlay_backdrop.overlay_backdrop import OverlayBackdrop
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for OverlayBackdrop component."""
    return Subject(
        title="Overlay Backdrop",
        description="Backdrop overlay",
        target=OverlayBackdrop,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
