"""The subject for the FormSelect component."""

from examples.huge.forms.form_select.form_select import FormSelect
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for FormSelect component."""
    return Subject(
        title="Form Select",
        description="Select for forms",
        target=FormSelect,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
