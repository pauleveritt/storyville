"""The subject for the OverlayDropdown component."""

from examples.huge.overlays.overlay_dropdown.overlay_dropdown import OverlayDropdown
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for OverlayDropdown component."""
    return Subject(
        title="Overlay Dropdown",
        description="Dropdown overlay",
        target=OverlayDropdown,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
