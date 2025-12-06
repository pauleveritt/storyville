"""The subject for the FeedbackModal component."""

from examples.huge.feedback.feedback_modal.feedback_modal import FeedbackModal
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for FeedbackModal component."""
    return Subject(
        title="Feedback Modal",
        description="Modal dialog",
        target=FeedbackModal,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
