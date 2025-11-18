"""The subject for the DataTimeline component."""

from examples.huge.data_display.data_timeline.data_timeline import DataTimeline
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for DataTimeline component."""
    return Subject(
        title="Data Timeline",
        description="Timeline display",
        target=DataTimeline,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
