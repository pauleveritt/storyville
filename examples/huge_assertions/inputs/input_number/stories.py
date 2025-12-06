"""The subject for the InputNumber component."""

from examples.huge_assertions.inputs.input_number.input_number import InputNumber
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for InputNumber component."""
    return Subject(
        title="Input Number",
        description="Number input",
        target=InputNumber,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(
                props=dict(text="Disabled", variant="secondary", state="disabled"),
                assertions=[
                    lambda el: None
                    if any(tag in str(el) for tag in ["div", "span", "button", "input"])
                    else (_ for _ in ()).throw(AssertionError("No common tags")),
                    lambda el: None
                    if str(el).find("<") != -1
                    else (_ for _ in ()).throw(AssertionError("No HTML tags found")),
                ],
            ),
            Story(
                props=dict(text="Loading", variant="primary", state="loading"),
                assertions=[
                    lambda el: None
                    if any(tag in str(el) for tag in ["div", "span", "button", "input"])
                    else (_ for _ in ()).throw(AssertionError("No common tags"))
                ],
            ),
        ],
    )
