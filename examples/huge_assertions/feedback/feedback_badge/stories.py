"""The subject for the FeedbackBadge component."""

from examples.huge_assertions.feedback.feedback_badge.feedback_badge import FeedbackBadge
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for FeedbackBadge component."""
    return Subject(
        title="Feedback Badge",
        description="Badge indicator",
        target=FeedbackBadge,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags"))]),
        ],
    )
