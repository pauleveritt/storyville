"""The subject for the DataList component."""

from examples.huge.data_display.data_list.data_list import DataList
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for DataList component."""
    return Subject(
        title="Data List",
        description="List for data",
        target=DataList,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
