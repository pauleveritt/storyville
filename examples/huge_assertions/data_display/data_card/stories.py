"""The subject for the DataCard component."""

from examples.huge_assertions.data_display.data_card.data_card import DataCard
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for DataCard component."""
    return Subject(
        title="Data Card",
        description="Card for data",
        target=DataCard,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
