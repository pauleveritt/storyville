"""The subject for the FeedbackTooltip component."""

from examples.huge_assertions.feedback.feedback_tooltip.feedback_tooltip import (
    FeedbackTooltip,
)
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for FeedbackTooltip component."""
    return Subject(
        title="Feedback Tooltip",
        description="Tooltip message",
        target=FeedbackTooltip,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(
                props=dict(text="Loading", variant="primary", state="loading"),
                assertions=[
                    lambda el: None
                    if str(el).find("<") != -1
                    else (_ for _ in ()).throw(AssertionError("No HTML tags found")),
                    lambda el: None
                    if len(str(el)) > 10
                    else (_ for _ in ()).throw(AssertionError("Element too short")),
                    lambda el: None
                    if hasattr(el, "__html__")
                    else (_ for _ in ()).throw(
                        AssertionError("Missing __html__ attribute")
                    ),
                ],
            ),
        ],
    )
