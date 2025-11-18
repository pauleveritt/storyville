"""The subject for the LayoutHeader component."""

from examples.huge_assertions.layout.layout_header.layout_header import LayoutHeader
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for LayoutHeader component."""
    return Subject(
        title="Layout Header",
        description="Header container",
        target=LayoutHeader,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if (el is not None and str(el)) else (_ for _ in ()).throw(AssertionError("Invalid element")), lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
