"""The subject for the InputEmail component."""

from examples.huge.inputs.input_email.input_email import InputEmail
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for InputEmail component."""
    return Subject(
        title="Input Email",
        description="Email input",
        target=InputEmail,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
