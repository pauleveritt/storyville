"""The subject for the OverlayDrawer component."""

from examples.huge.overlays.overlay_drawer.overlay_drawer import OverlayDrawer
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for OverlayDrawer component."""
    return Subject(
        title="Overlay Drawer",
        description="Drawer overlay",
        target=OverlayDrawer,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
