"""The subject for the LayoutSection component."""

from examples.huge_assertions.layout.layout_section.layout_section import LayoutSection
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for LayoutSection component."""
    return Subject(
        title="Layout Section",
        description="Section container",
        target=LayoutSection,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found")), lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags"))]),
        ],
    )
