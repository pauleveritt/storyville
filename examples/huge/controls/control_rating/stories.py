"""The subject for the ControlRating component."""

from examples.huge.controls.control_rating.control_rating import ControlRating
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for ControlRating component."""
    return Subject(
        title="Control Rating",
        description="Rating control",
        target=ControlRating,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
