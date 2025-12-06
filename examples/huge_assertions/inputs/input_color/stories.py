"""The subject for the InputColor component."""

from examples.huge_assertions.inputs.input_color.input_color import InputColor
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for InputColor component."""
    return Subject(
        title="Input Color",
        description="Color picker",
        target=InputColor,
        items=[
            Story(
                props=dict(text="Default", variant="primary", state="default"),
                assertions=[
                    lambda el: None
                    if "class" in str(el).lower() or "div" in str(el).lower()
                    else (_ for _ in ()).throw(AssertionError("No class or div found")),
                    lambda el: None
                    if any(tag in str(el) for tag in ["div", "span", "button", "input"])
                    else (_ for _ in ()).throw(AssertionError("No common tags")),
                    lambda el: None
                    if str(el).find("<") != -1
                    else (_ for _ in ()).throw(AssertionError("No HTML tags found")),
                ],
            ),
            Story(
                props=dict(text="Disabled", variant="secondary", state="disabled"),
                assertions=[
                    lambda el: None
                    if "class" in str(el).lower() or "div" in str(el).lower()
                    else (_ for _ in ()).throw(AssertionError("No class or div found"))
                ],
            ),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
