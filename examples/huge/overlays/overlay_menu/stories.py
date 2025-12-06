"""The subject for the OverlayMenu component."""

from examples.huge.overlays.overlay_menu.overlay_menu import OverlayMenu
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for OverlayMenu component."""
    return Subject(
        title="Overlay Menu",
        description="Menu overlay",
        target=OverlayMenu,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
