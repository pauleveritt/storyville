"""The subject for the FeedbackToast component."""

from examples.huge.feedback.feedback_toast.feedback_toast import FeedbackToast
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for FeedbackToast component."""
    return Subject(
        title="Feedback Toast",
        description="Toast notification",
        target=FeedbackToast,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
