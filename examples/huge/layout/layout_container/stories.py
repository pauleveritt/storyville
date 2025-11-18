"""The subject for the LayoutContainer component."""

from examples.huge.layout.layout_container.layout_container import LayoutContainer
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for LayoutContainer component."""
    return Subject(
        title="Layout Container",
        description="Container for layout",
        target=LayoutContainer,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
