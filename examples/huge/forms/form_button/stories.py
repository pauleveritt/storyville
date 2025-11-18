"""The subject for the FormButton component."""

from examples.huge.forms.form_button.form_button import FormButton
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for FormButton component."""
    return Subject(
        title="Form Button",
        description="Button for forms",
        target=FormButton,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
