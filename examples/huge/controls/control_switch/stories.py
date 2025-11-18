"""The subject for the ControlSwitch component."""

from examples.huge.controls.control_switch.control_switch import ControlSwitch
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for ControlSwitch component."""
    return Subject(
        title="Control Switch",
        description="Switch control",
        target=ControlSwitch,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
