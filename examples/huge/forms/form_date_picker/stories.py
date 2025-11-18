"""The subject for the FormDatePicker component."""

from examples.huge.forms.form_date_picker.form_date_picker import FormDatePicker
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for FormDatePicker component."""
    return Subject(
        title="Form Date Picker",
        description="Date picker for forms",
        target=FormDatePicker,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
