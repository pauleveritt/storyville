"""The subject for the InputTel component."""

from examples.huge_assertions.inputs.input_tel.input_tel import InputTel
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for InputTel component."""
    return Subject(
        title="Input Tel",
        description="Telephone input",
        target=InputTel,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if "class" in str(el).lower() or "div" in str(el).lower() else (_ for _ in ()).throw(AssertionError("No class or div found")), lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags")), lambda el: None if hasattr(el, "__html__") else (_ for _ in ()).throw(AssertionError("Missing __html__ attribute"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if len(str(el)) > 10 else (_ for _ in ()).throw(AssertionError("Element too short")), lambda el: None if hasattr(el, "__html__") else (_ for _ in ()).throw(AssertionError("Missing __html__ attribute"))]),
        ],
    )
