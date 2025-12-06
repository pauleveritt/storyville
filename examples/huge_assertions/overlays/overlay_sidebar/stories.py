"""The subject for the OverlaySidebar component."""

from examples.huge_assertions.overlays.overlay_sidebar.overlay_sidebar import OverlaySidebar
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for OverlaySidebar component."""
    return Subject(
        title="Overlay Sidebar",
        description="Sidebar overlay",
        target=OverlaySidebar,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if hasattr(el, "__html__") else (_ for _ in ()).throw(AssertionError("Missing __html__ attribute"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if len(str(el)) > 10 else (_ for _ in ()).throw(AssertionError("Element too short")), lambda el: None if (el is not None and str(el)) else (_ for _ in ()).throw(AssertionError("Invalid element"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if (el is not None and str(el)) else (_ for _ in ()).throw(AssertionError("Invalid element")), lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags"))]),
        ],
    )
