"""The subject for the TypoHeading component."""

from examples.huge_assertions.typography.typo_heading.typo_heading import TypoHeading
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for TypoHeading component."""
    return Subject(
        title="Typo Heading",
        description="Heading text",
        target=TypoHeading,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if "class" in str(el).lower() or "div" in str(el).lower() else (_ for _ in ()).throw(AssertionError("No class or div found"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found")), lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
