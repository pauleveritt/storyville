"""The subject for the LayoutGrid component."""

from examples.huge.layout.layout_grid.layout_grid import LayoutGrid
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for LayoutGrid component."""
    return Subject(
        title="Layout Grid",
        description="Grid layout",
        target=LayoutGrid,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
