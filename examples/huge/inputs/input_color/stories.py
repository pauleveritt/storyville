"""The subject for the InputColor component."""

from examples.huge.inputs.input_color.input_color import InputColor
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for InputColor component."""
    return Subject(
        title="Input Color",
        description="Color picker",
        target=InputColor,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
