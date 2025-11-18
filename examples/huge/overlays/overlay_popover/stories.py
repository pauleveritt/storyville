"""The subject for the OverlayPopover component."""

from examples.huge.overlays.overlay_popover.overlay_popover import OverlayPopover
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for OverlayPopover component."""
    return Subject(
        title="Overlay Popover",
        description="Popover overlay",
        target=OverlayPopover,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
