"""The subject for the LayoutSpacer component."""

from examples.huge.layout.layout_spacer.layout_spacer import LayoutSpacer
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for LayoutSpacer component."""
    return Subject(
        title="Layout Spacer",
        description="Spacer element",
        target=LayoutSpacer,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
