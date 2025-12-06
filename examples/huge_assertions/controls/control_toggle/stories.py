"""The subject for the ControlToggle component."""

from examples.huge_assertions.controls.control_toggle.control_toggle import (
    ControlToggle,
)
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for ControlToggle component."""
    return Subject(
        title="Control Toggle",
        description="Toggle control",
        target=ControlToggle,
        items=[
            Story(
                props=dict(text="Default", variant="primary", state="default"),
                assertions=[
                    lambda el: None
                    if el is not None
                    else (_ for _ in ()).throw(AssertionError("Element is None"))
                ],
            ),
            Story(
                props=dict(text="Disabled", variant="secondary", state="disabled"),
                assertions=[
                    lambda el: None
                    if str(el).find("<") != -1
                    else (_ for _ in ()).throw(AssertionError("No HTML tags found")),
                    lambda el: None
                    if "class" in str(el).lower() or "div" in str(el).lower()
                    else (_ for _ in ()).throw(AssertionError("No class or div found")),
                    lambda el: None
                    if el is not None
                    else (_ for _ in ()).throw(AssertionError("Element is None")),
                ],
            ),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
