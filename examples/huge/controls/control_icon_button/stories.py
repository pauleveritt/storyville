"""The subject for the ControlIconButton component."""

from examples.huge.controls.control_icon_button.control_icon_button import ControlIconButton
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for ControlIconButton component."""
    return Subject(
        title="Control Icon Button",
        description="Icon button",
        target=ControlIconButton,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
