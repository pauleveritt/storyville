"""The subject for the ControlRating component."""

from examples.huge_assertions.controls.control_rating.control_rating import ControlRating
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for ControlRating component."""
    return Subject(
        title="Control Rating",
        description="Rating control",
        target=ControlRating,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if hasattr(el, "__html__") else (_ for _ in ()).throw(AssertionError("Missing __html__ attribute")), lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found")), lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if len(str(el)) > 10 else (_ for _ in ()).throw(AssertionError("Element too short")), lambda el: None if hasattr(el, "__html__") else (_ for _ in ()).throw(AssertionError("Missing __html__ attribute")), lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None"))]),
        ],
    )
