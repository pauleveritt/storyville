"""The subject for the DataChart component."""

from examples.huge.data_display.data_chart.data_chart import DataChart
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for DataChart component."""
    return Subject(
        title="Data Chart",
        description="Chart display",
        target=DataChart,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
