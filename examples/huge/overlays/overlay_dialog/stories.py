"""The subject for the OverlayDialog component."""

from examples.huge.overlays.overlay_dialog.overlay_dialog import OverlayDialog
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for OverlayDialog component."""
    return Subject(
        title="Overlay Dialog",
        description="Dialog overlay",
        target=OverlayDialog,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
