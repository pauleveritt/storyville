"""The subject for the DataTimeline component."""

from examples.huge_assertions.data_display.data_timeline.data_timeline import DataTimeline
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for DataTimeline component."""
    return Subject(
        title="Data Timeline",
        description="Timeline display",
        target=DataTimeline,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags")), lambda el: None if len(str(el)) > 10 else (_ for _ in ()).throw(AssertionError("Element too short"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if (el is not None and str(el)) else (_ for _ in ()).throw(AssertionError("Invalid element"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if len(str(el)) > 10 else (_ for _ in ()).throw(AssertionError("Element too short")), lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags"))]),
        ],
    )
