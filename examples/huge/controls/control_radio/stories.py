"""The subject for the ControlRadio component."""

from examples.huge.controls.control_radio.control_radio import ControlRadio
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for ControlRadio component."""
    return Subject(
        title="Control Radio",
        description="Radio control",
        target=ControlRadio,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
