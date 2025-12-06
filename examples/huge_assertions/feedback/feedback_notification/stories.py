"""The subject for the FeedbackNotification component."""

from examples.huge_assertions.feedback.feedback_notification.feedback_notification import FeedbackNotification
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for FeedbackNotification component."""
    return Subject(
        title="Feedback Notification",
        description="Notification message",
        target=FeedbackNotification,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if (el is not None and str(el)) else (_ for _ in ()).throw(AssertionError("Invalid element"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags")), lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None")), lambda el: None if hasattr(el, "__html__") else (_ for _ in ()).throw(AssertionError("Missing __html__ attribute"))]),
        ],
    )
