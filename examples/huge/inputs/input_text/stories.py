"""The subject for the InputText component."""

from examples.huge.inputs.input_text.input_text import InputText
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for InputText component."""
    return Subject(
        title="Input Text",
        description="Text input",
        target=InputText,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
