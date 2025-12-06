"""The subject for the ControlChip component."""

from examples.huge.controls.control_chip.control_chip import ControlChip
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for ControlChip component."""
    return Subject(
        title="Control Chip",
        description="Chip control",
        target=ControlChip,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
