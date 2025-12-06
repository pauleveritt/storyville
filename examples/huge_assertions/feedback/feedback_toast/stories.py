"""The subject for the FeedbackToast component."""

from examples.huge_assertions.feedback.feedback_toast.feedback_toast import (
    FeedbackToast,
)
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for FeedbackToast component."""
    return Subject(
        title="Feedback Toast",
        description="Toast notification",
        target=FeedbackToast,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(
                props=dict(text="Disabled", variant="secondary", state="disabled"),
                assertions=[
                    lambda el: None
                    if el is not None
                    else (_ for _ in ()).throw(AssertionError("Element is None")),
                    lambda el: None
                    if len(str(el)) > 10
                    else (_ for _ in ()).throw(AssertionError("Element too short")),
                ],
            ),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
