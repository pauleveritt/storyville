"""The subject for the DataStat component."""

from examples.huge.data_display.data_stat.data_stat import DataStat
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for DataStat component."""
    return Subject(
        title="Data Stat",
        description="Statistic display",
        target=DataStat,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
