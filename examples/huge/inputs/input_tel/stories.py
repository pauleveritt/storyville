"""The subject for the InputTel component."""

from examples.huge.inputs.input_tel.input_tel import InputTel
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for InputTel component."""
    return Subject(
        title="Input Tel",
        description="Telephone input",
        target=InputTel,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
