"""The subject for the LayoutSpacer component."""

from examples.huge_assertions.layout.layout_spacer.layout_spacer import LayoutSpacer
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for LayoutSpacer component."""
    return Subject(
        title="Layout Spacer",
        description="Spacer element",
        target=LayoutSpacer,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if "class" in str(el).lower() or "div" in str(el).lower() else (_ for _ in ()).throw(AssertionError("No class or div found"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found"))]),
        ],
    )
