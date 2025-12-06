"""The subject for the OverlayDrawer component."""

from examples.huge_assertions.overlays.overlay_drawer.overlay_drawer import OverlayDrawer
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for OverlayDrawer component."""
    return Subject(
        title="Overlay Drawer",
        description="Drawer overlay",
        target=OverlayDrawer,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None")), lambda el: None if len(str(el)) > 10 else (_ for _ in ()).throw(AssertionError("Element too short"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if (el is not None and str(el)) else (_ for _ in ()).throw(AssertionError("Invalid element")), lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found"))]),
        ],
    )
