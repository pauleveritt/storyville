"""The subject for the LayoutDivider component."""

from examples.huge_assertions.layout.layout_divider.layout_divider import LayoutDivider
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for LayoutDivider component."""
    return Subject(
        title="Layout Divider",
        description="Divider element",
        target=LayoutDivider,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if (el is not None and str(el)) else (_ for _ in ()).throw(AssertionError("Invalid element")), lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
