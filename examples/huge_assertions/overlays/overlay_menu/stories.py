"""The subject for the OverlayMenu component."""

from examples.huge_assertions.overlays.overlay_menu.overlay_menu import OverlayMenu
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for OverlayMenu component."""
    return Subject(
        title="Overlay Menu",
        description="Menu overlay",
        target=OverlayMenu,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags")), lambda el: None if hasattr(el, "__html__") else (_ for _ in ()).throw(AssertionError("Missing __html__ attribute")), lambda el: None if "class" in str(el).lower() or "div" in str(el).lower() else (_ for _ in ()).throw(AssertionError("No class or div found"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
