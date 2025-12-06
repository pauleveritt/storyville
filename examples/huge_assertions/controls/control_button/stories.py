"""The subject for the ControlButton component."""

from examples.huge_assertions.controls.control_button.control_button import ControlButton
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for ControlButton component."""
    return Subject(
        title="Control Button",
        description="Button control",
        target=ControlButton,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if len(str(el)) > 10 else (_ for _ in ()).throw(AssertionError("Element too short"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if hasattr(el, "__html__") else (_ for _ in ()).throw(AssertionError("Missing __html__ attribute"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
