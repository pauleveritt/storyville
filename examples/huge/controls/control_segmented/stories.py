"""The subject for the ControlSegmented component."""

from examples.huge.controls.control_segmented.control_segmented import ControlSegmented
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
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
