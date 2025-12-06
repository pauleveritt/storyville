"""The subject for the OverlayDialog component."""

from examples.huge_assertions.overlays.overlay_dialog.overlay_dialog import OverlayDialog
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for OverlayDialog component."""
    return Subject(
        title="Overlay Dialog",
        description="Dialog overlay",
        target=OverlayDialog,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found"))]),
        ],
    )
