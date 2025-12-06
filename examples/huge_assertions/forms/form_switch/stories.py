"""The subject for the FormSwitch component."""

from examples.huge_assertions.forms.form_switch.form_switch import FormSwitch
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for FormSwitch component."""
    return Subject(
        title="Form Switch",
        description="Switch toggle for forms",
        target=FormSwitch,
        items=[
            Story(
                props=dict(text="Default", variant="primary", state="default"),
                assertions=[
                    lambda el: None
                    if (el is not None and str(el))
                    else (_ for _ in ()).throw(AssertionError("Invalid element")),
                    lambda el: None
                    if len(str(el)) > 10
                    else (_ for _ in ()).throw(AssertionError("Element too short")),
                    lambda el: None
                    if any(tag in str(el) for tag in ["div", "span", "button", "input"])
                    else (_ for _ in ()).throw(AssertionError("No common tags")),
                ],
            ),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(
                props=dict(text="Loading", variant="primary", state="loading"),
                assertions=[
                    lambda el: None
                    if len(str(el)) > 10
                    else (_ for _ in ()).throw(AssertionError("Element too short"))
                ],
            ),
        ],
    )
