"""The subject for the FormCheckbox component."""

from examples.huge_assertions.forms.form_checkbox.form_checkbox import FormCheckbox
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for FormCheckbox component."""
    return Subject(
        title="Form Checkbox",
        description="Checkbox for forms",
        target=FormCheckbox,
        items=[
            Story(
                props=dict(text="Default", variant="primary", state="default"),
                assertions=[
                    lambda el: None
                    if "class" in str(el).lower() or "div" in str(el).lower()
                    else (_ for _ in ()).throw(AssertionError("No class or div found"))
                ],
            ),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(
                props=dict(text="Loading", variant="primary", state="loading"),
                assertions=[
                    lambda el: None
                    if "class" in str(el).lower() or "div" in str(el).lower()
                    else (_ for _ in ()).throw(AssertionError("No class or div found"))
                ],
            ),
        ],
    )
