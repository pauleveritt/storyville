"""The subject for the DataTag component."""

from examples.huge_assertions.data_display.data_tag.data_tag import DataTag
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for DataTag component."""
    return Subject(
        title="Data Tag",
        description="Tag for data",
        target=DataTag,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
