"""The subject for the LayoutFooter component."""

from examples.huge.layout.layout_footer.layout_footer import LayoutFooter
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for LayoutFooter component."""
    return Subject(
        title="Layout Footer",
        description="Footer container",
        target=LayoutFooter,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
