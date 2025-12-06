"""The subject for the DataTree component."""

from examples.huge.data_display.data_tree.data_tree import DataTree
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for DataTree component."""
    return Subject(
        title="Data Tree",
        description="Tree structure",
        target=DataTree,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
