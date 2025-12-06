"""The subject for the FeedbackProgress component."""

from examples.huge_assertions.feedback.feedback_progress.feedback_progress import (
    FeedbackProgress,
)
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for FeedbackProgress component."""
    return Subject(
        title="Feedback Progress",
        description="Progress indicator",
        target=FeedbackProgress,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(
                props=dict(text="Disabled", variant="secondary", state="disabled"),
                assertions=[
                    lambda el: None
                    if hasattr(el, "__html__")
                    else (_ for _ in ()).throw(
                        AssertionError("Missing __html__ attribute")
                    ),
                    lambda el: None
                    if el is not None
                    else (_ for _ in ()).throw(AssertionError("Element is None")),
                ],
            ),
            Story(
                props=dict(text="Loading", variant="primary", state="loading"),
                assertions=[
                    lambda el: None
                    if hasattr(el, "__html__")
                    else (_ for _ in ()).throw(
                        AssertionError("Missing __html__ attribute")
                    ),
                    lambda el: None
                    if (el is not None and str(el))
                    else (_ for _ in ()).throw(AssertionError("Invalid element")),
                ],
            ),
        ],
    )
