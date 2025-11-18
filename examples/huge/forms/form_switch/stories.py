"""The subject for the FormSwitch component."""

from examples.huge.forms.form_switch.form_switch import FormSwitch
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for FormSwitch component."""
    return Subject(
        title="Form Switch",
        description="Switch toggle for forms",
        target=FormSwitch,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
