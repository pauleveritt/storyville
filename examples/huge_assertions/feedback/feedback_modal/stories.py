"""The subject for the FeedbackModal component."""

from examples.huge_assertions.feedback.feedback_modal.feedback_modal import FeedbackModal
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for FeedbackModal component."""
    return Subject(
        title="Feedback Modal",
        description="Modal dialog",
        target=FeedbackModal,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None")), lambda el: None if len(str(el)) > 10 else (_ for _ in ()).throw(AssertionError("Element too short")), lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if hasattr(el, "__html__") else (_ for _ in ()).throw(AssertionError("Missing __html__ attribute")), lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags"))]),
        ],
    )
