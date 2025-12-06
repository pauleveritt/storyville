"""The subject for the FeedbackProgress component."""

from examples.huge.feedback.feedback_progress.feedback_progress import FeedbackProgress
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for FeedbackProgress component."""
    return Subject(
        title="Feedback Progress",
        description="Progress indicator",
        target=FeedbackProgress,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
