"""The subject for the FormTextarea component."""

from examples.huge.forms.form_textarea.form_textarea import FormTextarea
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for FormTextarea component."""
    return Subject(
        title="Form Textarea",
        description="Textarea for forms",
        target=FormTextarea,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
