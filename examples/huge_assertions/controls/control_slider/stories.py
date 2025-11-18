"""The subject for the ControlSlider component."""

from examples.huge_assertions.controls.control_slider.control_slider import ControlSlider
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for ControlSlider component."""
    return Subject(
        title="Control Slider",
        description="Slider control",
        target=ControlSlider,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None")), lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if hasattr(el, "__html__") else (_ for _ in ()).throw(AssertionError("Missing __html__ attribute")), lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
