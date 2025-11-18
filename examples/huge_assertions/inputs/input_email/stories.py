"""The subject for the InputEmail component."""

from examples.huge_assertions.inputs.input_email.input_email import InputEmail
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for InputEmail component."""
    return Subject(
        title="Input Email",
        description="Email input",
        target=InputEmail,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if len(str(el)) > 10 else (_ for _ in ()).throw(AssertionError("Element too short")), lambda el: None if "class" in str(el).lower() or "div" in str(el).lower() else (_ for _ in ()).throw(AssertionError("No class or div found"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags")), lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None"))]),
        ],
    )
