"""The subject for the ControlChip component."""

from examples.huge_assertions.controls.control_chip.control_chip import ControlChip
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for ControlChip component."""
    return Subject(
        title="Control Chip",
        description="Chip control",
        target=ControlChip,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None")), lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found")), lambda el: None if hasattr(el, "__html__") else (_ for _ in ()).throw(AssertionError("Missing __html__ attribute"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if (el is not None and str(el)) else (_ for _ in ()).throw(AssertionError("Invalid element"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if hasattr(el, "__html__") else (_ for _ in ()).throw(AssertionError("Missing __html__ attribute"))]),
        ],
    )
