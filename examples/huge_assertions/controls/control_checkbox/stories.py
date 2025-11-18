"""The subject for the ControlCheckbox component."""

from examples.huge_assertions.controls.control_checkbox.control_checkbox import ControlCheckbox
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for ControlCheckbox component."""
    return Subject(
        title="Control Checkbox",
        description="Checkbox control",
        target=ControlCheckbox,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
