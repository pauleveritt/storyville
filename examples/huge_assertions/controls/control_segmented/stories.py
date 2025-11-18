"""The subject for the ControlSegmented component."""

from examples.huge_assertions.controls.control_segmented.control_segmented import ControlSegmented
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for ControlSegmented component."""
    return Subject(
        title="Control Segmented",
        description="Segmented control",
        target=ControlSegmented,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if "class" in str(el).lower() or "div" in str(el).lower() else (_ for _ in ()).throw(AssertionError("No class or div found")), lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None")), lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags"))]),
        ],
    )
