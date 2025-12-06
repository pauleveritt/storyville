"""The subject for the FeedbackNotification component."""

from examples.huge.feedback.feedback_notification.feedback_notification import (
    FeedbackNotification,
)
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for FeedbackNotification component."""
    return Subject(
        title="Feedback Notification",
        description="Notification message",
        target=FeedbackNotification,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
