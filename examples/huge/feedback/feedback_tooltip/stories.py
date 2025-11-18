"""The subject for the FeedbackTooltip component."""

from examples.huge.feedback.feedback_tooltip.feedback_tooltip import FeedbackTooltip
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for FeedbackTooltip component."""
    return Subject(
        title="Feedback Tooltip",
        description="Tooltip message",
        target=FeedbackTooltip,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
