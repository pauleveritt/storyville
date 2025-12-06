"""The subject for the FormInput component."""

from examples.huge_assertions.forms.form_input.form_input import FormInput
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for FormInput component."""
    return Subject(
        title="Form Input",
        description="Input for forms",
        target=FormInput,
        items=[
            Story(
                props=dict(text="Default", variant="primary", state="default"),
                assertions=[
                    lambda el: None
                    if el is not None
                    else (_ for _ in ()).throw(AssertionError("Element is None"))
                ],
            ),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(
                props=dict(text="Loading", variant="primary", state="loading"),
                assertions=[
                    lambda el: None
                    if str(el).find("<") != -1
                    else (_ for _ in ()).throw(AssertionError("No HTML tags found")),
                    lambda el: None
                    if (el is not None and str(el))
                    else (_ for _ in ()).throw(AssertionError("Invalid element")),
                    lambda el: None
                    if len(str(el)) > 10
                    else (_ for _ in ()).throw(AssertionError("Element too short")),
                ],
            ),
        ],
    )
