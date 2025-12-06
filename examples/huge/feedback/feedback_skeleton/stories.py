"""The subject for the FeedbackSkeleton component."""

from examples.huge.feedback.feedback_skeleton.feedback_skeleton import FeedbackSkeleton
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for FeedbackSkeleton component."""
    return Subject(
        title="Feedback Skeleton",
        description="Skeleton loader",
        target=FeedbackSkeleton,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
