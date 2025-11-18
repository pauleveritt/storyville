"""The subject for the InputNumber component."""

from examples.huge.inputs.input_number.input_number import InputNumber
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for InputNumber component."""
    return Subject(
        title="Input Number",
        description="Number input",
        target=InputNumber,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
