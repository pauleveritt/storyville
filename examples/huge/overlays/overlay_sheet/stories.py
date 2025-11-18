"""The subject for the OverlaySheet component."""

from examples.huge.overlays.overlay_sheet.overlay_sheet import OverlaySheet
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for OverlaySheet component."""
    return Subject(
        title="Overlay Sheet",
        description="Sheet overlay",
        target=OverlaySheet,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
