"""The subject for the InputText component."""

from examples.huge_assertions.inputs.input_text.input_text import InputText
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for InputText component."""
    return Subject(
        title="Input Text",
        description="Text input",
        target=InputText,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if "class" in str(el).lower() or "div" in str(el).lower() else (_ for _ in ()).throw(AssertionError("No class or div found"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found")), lambda el: None if (el is not None and str(el)) else (_ for _ in ()).throw(AssertionError("Invalid element")), lambda el: None if len(str(el)) > 10 else (_ for _ in ()).throw(AssertionError("Element too short"))]),
        ],
    )
