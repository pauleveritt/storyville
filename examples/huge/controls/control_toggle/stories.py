"""The subject for the ControlToggle component."""

from examples.huge.controls.control_toggle.control_toggle import ControlToggle
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for ControlToggle component."""
    return Subject(
        title="Control Toggle",
        description="Toggle control",
        target=ControlToggle,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
