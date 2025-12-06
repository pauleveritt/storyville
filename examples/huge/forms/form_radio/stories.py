"""The subject for the FormRadio component."""

from examples.huge.forms.form_radio.form_radio import FormRadio
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for FormRadio component."""
    return Subject(
        title="Form Radio",
        description="Radio button for forms",
        target=FormRadio,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
