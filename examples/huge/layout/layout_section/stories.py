"""The subject for the LayoutSection component."""

from examples.huge.layout.layout_section.layout_section import LayoutSection
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for LayoutSection component."""
    return Subject(
        title="Layout Section",
        description="Section container",
        target=LayoutSection,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
