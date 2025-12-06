"""The subject for the FormInput component."""

from examples.huge.forms.form_input.form_input import FormInput
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for FormInput component."""
    return Subject(
        title="Form Input",
        description="Input for forms",
        target=FormInput,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
