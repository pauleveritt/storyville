"""The subject for the FormDatePicker component."""

from examples.huge_assertions.forms.form_date_picker.form_date_picker import FormDatePicker
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for FormDatePicker component."""
    return Subject(
        title="Form Date Picker",
        description="Date picker for forms",
        target=FormDatePicker,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if hasattr(el, "__html__") else (_ for _ in ()).throw(AssertionError("Missing __html__ attribute"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if (el is not None and str(el)) else (_ for _ in ()).throw(AssertionError("Invalid element"))]),
        ],
    )
