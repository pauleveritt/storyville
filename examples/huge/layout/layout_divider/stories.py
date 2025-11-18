"""The subject for the LayoutDivider component."""

from examples.huge.layout.layout_divider.layout_divider import LayoutDivider
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for LayoutDivider component."""
    return Subject(
        title="Layout Divider",
        description="Divider element",
        target=LayoutDivider,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
