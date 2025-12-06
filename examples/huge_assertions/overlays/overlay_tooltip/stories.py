"""The subject for the OverlayTooltip component."""

from examples.huge_assertions.overlays.overlay_tooltip.overlay_tooltip import OverlayTooltip
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for OverlayTooltip component."""
    return Subject(
        title="Overlay Tooltip",
        description="Tooltip overlay",
        target=OverlayTooltip,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if hasattr(el, "__html__") else (_ for _ in ()).throw(AssertionError("Missing __html__ attribute"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if hasattr(el, "__html__") else (_ for _ in ()).throw(AssertionError("Missing __html__ attribute")), lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None")), lambda el: None if "class" in str(el).lower() or "div" in str(el).lower() else (_ for _ in ()).throw(AssertionError("No class or div found"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags"))]),
        ],
    )
