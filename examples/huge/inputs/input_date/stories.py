"""The subject for the InputDate component."""

from examples.huge.inputs.input_date.input_date import InputDate
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for InputDate component."""
    return Subject(
        title="Input Date",
        description="Date input",
        target=InputDate,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
