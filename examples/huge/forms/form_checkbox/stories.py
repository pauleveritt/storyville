"""The subject for the FormCheckbox component."""

from examples.huge.forms.form_checkbox.form_checkbox import FormCheckbox
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for FormCheckbox component."""
    return Subject(
        title="Form Checkbox",
        description="Checkbox for forms",
        target=FormCheckbox,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
