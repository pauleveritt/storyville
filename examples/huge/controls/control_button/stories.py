"""The subject for the ControlButton component."""

from examples.huge.controls.control_button.control_button import ControlButton
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for ControlButton component."""
    return Subject(
        title="Control Button",
        description="Button control",
        target=ControlButton,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
