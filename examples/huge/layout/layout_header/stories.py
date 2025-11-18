"""The subject for the LayoutHeader component."""

from examples.huge.layout.layout_header.layout_header import LayoutHeader
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for LayoutHeader component."""
    return Subject(
        title="Layout Header",
        description="Header container",
        target=LayoutHeader,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
