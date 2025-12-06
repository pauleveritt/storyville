"""The subject for the FeedbackBanner component."""

from examples.huge.feedback.feedback_banner.feedback_banner import FeedbackBanner
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for FeedbackBanner component."""
    return Subject(
        title="Feedback Banner",
        description="Banner message",
        target=FeedbackBanner,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
