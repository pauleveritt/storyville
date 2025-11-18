"""The subject for the OverlaySidebar component."""

from examples.huge.overlays.overlay_sidebar.overlay_sidebar import OverlaySidebar
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for OverlaySidebar component."""
    return Subject(
        title="Overlay Sidebar",
        description="Sidebar overlay",
        target=OverlaySidebar,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
