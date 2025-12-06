"""The subject for the OverlayTooltip component."""

from examples.huge.overlays.overlay_tooltip.overlay_tooltip import OverlayTooltip
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for OverlayTooltip component."""
    return Subject(
        title="Overlay Tooltip",
        description="Tooltip overlay",
        target=OverlayTooltip,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
