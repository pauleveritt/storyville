"""The subject for the DataCode component."""

from examples.huge.data_display.data_code.data_code import DataCode
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for DataCode component."""
    return Subject(
        title="Data Code",
        description="Code display",
        target=DataCode,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
