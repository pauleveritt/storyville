"""The subject for the DataTable component."""

from examples.huge.data_display.data_table.data_table import DataTable
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for DataTable component."""
    return Subject(
        title="Data Table",
        description="Table for data",
        target=DataTable,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
