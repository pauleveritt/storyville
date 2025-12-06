"""The subject for the LayoutPanel component."""

from examples.huge.layout.layout_panel.layout_panel import LayoutPanel
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for LayoutPanel component."""
    return Subject(
        title="Layout Panel",
        description="Panel container",
        target=LayoutPanel,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
