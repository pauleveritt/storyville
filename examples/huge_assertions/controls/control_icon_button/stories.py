"""The subject for the ControlIconButton component."""

from examples.huge_assertions.controls.control_icon_button.control_icon_button import (
    ControlIconButton,
)
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for ControlIconButton component."""
    return Subject(
        title="Control Icon Button",
        description="Icon button",
        target=ControlIconButton,
        items=[
            Story(
                props=dict(text="Default", variant="primary", state="default"),
                assertions=[
                    lambda el: None
                    if (el is not None and str(el))
                    else (_ for _ in ()).throw(AssertionError("Invalid element"))
                ],
            ),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(
                props=dict(text="Loading", variant="primary", state="loading"),
                assertions=[
                    lambda el: None
                    if "class" in str(el).lower() or "div" in str(el).lower()
                    else (_ for _ in ()).throw(AssertionError("No class or div found")),
                    lambda el: None
                    if (el is not None and str(el))
                    else (_ for _ in ()).throw(AssertionError("Invalid element")),
                ],
            ),
        ],
    )
