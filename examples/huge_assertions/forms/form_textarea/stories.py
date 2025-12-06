"""The subject for the FormTextarea component."""

from examples.huge_assertions.forms.form_textarea.form_textarea import FormTextarea
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for FormTextarea component."""
    return Subject(
        title="Form Textarea",
        description="Textarea for forms",
        target=FormTextarea,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(
                props=dict(text="Disabled", variant="secondary", state="disabled"),
                assertions=[
                    lambda el: None
                    if len(str(el)) > 10
                    else (_ for _ in ()).throw(AssertionError("Element too short"))
                ],
            ),
            Story(
                props=dict(text="Loading", variant="primary", state="loading"),
                assertions=[
                    lambda el: None
                    if (el is not None and str(el))
                    else (_ for _ in ()).throw(AssertionError("Invalid element")),
                    lambda el: None
                    if any(tag in str(el) for tag in ["div", "span", "button", "input"])
                    else (_ for _ in ()).throw(AssertionError("No common tags")),
                ],
            ),
        ],
    )
