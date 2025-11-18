"""The subject for the InputTime component."""

from examples.huge.inputs.input_time.input_time import InputTime
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for InputTime component."""
    return Subject(
        title="Input Time",
        description="Time input",
        target=InputTime,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
