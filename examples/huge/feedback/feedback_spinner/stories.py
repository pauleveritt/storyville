"""The subject for the FeedbackSpinner component."""

from examples.huge.feedback.feedback_spinner.feedback_spinner import FeedbackSpinner
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for FeedbackSpinner component."""
    return Subject(
        title="Feedback Spinner",
        description="Loading spinner",
        target=FeedbackSpinner,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
