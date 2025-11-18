"""The subject for the TypoMark component."""

from examples.huge_assertions.typography.typo_mark.typo_mark import TypoMark
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for TypoMark component."""
    return Subject(
        title="Typo Mark",
        description="Marked text",
        target=TypoMark,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if "class" in str(el).lower() or "div" in str(el).lower() else (_ for _ in ()).throw(AssertionError("No class or div found"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found")), lambda el: None if hasattr(el, "__html__") else (_ for _ in ()).throw(AssertionError("Missing __html__ attribute"))]),
        ],
    )
