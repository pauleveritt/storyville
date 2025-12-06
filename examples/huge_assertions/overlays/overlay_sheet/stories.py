"""The subject for the OverlaySheet component."""

from examples.huge_assertions.overlays.overlay_sheet.overlay_sheet import OverlaySheet
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for OverlaySheet component."""
    return Subject(
        title="Overlay Sheet",
        description="Sheet overlay",
        target=OverlaySheet,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if "class" in str(el).lower() or "div" in str(el).lower() else (_ for _ in ()).throw(AssertionError("No class or div found"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if len(str(el)) > 10 else (_ for _ in ()).throw(AssertionError("Element too short"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found")), lambda el: None if len(str(el)) > 10 else (_ for _ in ()).throw(AssertionError("Element too short"))]),
        ],
    )
