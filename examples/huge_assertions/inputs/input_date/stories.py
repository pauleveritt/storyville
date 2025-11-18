"""The subject for the InputDate component."""

from examples.huge_assertions.inputs.input_date.input_date import InputDate
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for InputDate component."""
    return Subject(
        title="Input Date",
        description="Date input",
        target=InputDate,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None")), lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags"))]),
        ],
    )
