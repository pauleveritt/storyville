"""The subject for the LayoutStack component."""

from examples.huge.layout.layout_stack.layout_stack import LayoutStack
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for LayoutStack component."""
    return Subject(
        title="Layout Stack",
        description="Stack layout",
        target=LayoutStack,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
