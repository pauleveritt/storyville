"""The subject for the TypoList component."""

from examples.huge_assertions.typography.typo_list.typo_list import TypoList
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for TypoList component."""
    return Subject(
        title="Typo List",
        description="List display",
        target=TypoList,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None")), lambda el: None if (el is not None and str(el)) else (_ for _ in ()).throw(AssertionError("Invalid element"))]),
        ],
    )
