"""The subject for the FormButton component."""

from examples.huge_assertions.forms.form_button.form_button import FormButton
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for FormButton component."""
    return Subject(
        title="Form Button",
        description="Button for forms",
        target=FormButton,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if len(str(el)) > 10 else (_ for _ in ()).throw(AssertionError("Element too short")), lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags")), lambda el: None if "class" in str(el).lower() or "div" in str(el).lower() else (_ for _ in ()).throw(AssertionError("No class or div found"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
