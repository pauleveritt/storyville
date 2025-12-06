"""The subject for the FeedbackAlert component."""

from examples.huge.feedback.feedback_alert.feedback_alert import FeedbackAlert
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for FeedbackAlert component."""
    return Subject(
        title="Feedback Alert",
        description="Alert message",
        target=FeedbackAlert,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
