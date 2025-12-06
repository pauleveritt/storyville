"""The subject for the OverlayModal component."""

from examples.huge.overlays.overlay_modal.overlay_modal import OverlayModal
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for OverlayModal component."""
    return Subject(
        title="Overlay Modal",
        description="Modal overlay",
        target=OverlayModal,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
