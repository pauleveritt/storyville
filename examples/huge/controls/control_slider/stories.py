"""The subject for the ControlSlider component."""

from examples.huge.controls.control_slider.control_slider import ControlSlider
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for ControlSlider component."""
    return Subject(
        title="Control Slider",
        description="Slider control",
        target=ControlSlider,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
