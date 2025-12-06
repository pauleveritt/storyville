"""The subject for the LayoutPanel component."""

from examples.huge_assertions.layout.layout_panel.layout_panel import LayoutPanel
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for LayoutPanel component."""
    return Subject(
        title="Layout Panel",
        description="Panel container",
        target=LayoutPanel,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if hasattr(el, "__html__") else (_ for _ in ()).throw(AssertionError("Missing __html__ attribute")), lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if "class" in str(el).lower() or "div" in str(el).lower() else (_ for _ in ()).throw(AssertionError("No class or div found")), lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None")), lambda el: None if hasattr(el, "__html__") else (_ for _ in ()).throw(AssertionError("Missing __html__ attribute"))]),
        ],
    )
