"""The subject for the OverlayModal component."""

from examples.huge_assertions.overlays.overlay_modal.overlay_modal import OverlayModal
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for OverlayModal component."""
    return Subject(
        title="Overlay Modal",
        description="Modal overlay",
        target=OverlayModal,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if (el is not None and str(el)) else (_ for _ in ()).throw(AssertionError("Invalid element")), lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None")), lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
