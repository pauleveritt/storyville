"""The subject for the TypoEmphasis component."""

from examples.huge_assertions.typography.typo_emphasis.typo_emphasis import TypoEmphasis
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for TypoEmphasis component."""
    return Subject(
        title="Typo Emphasis",
        description="Emphasized text",
        target=TypoEmphasis,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if "class" in str(el).lower() or "div" in str(el).lower() else (_ for _ in ()).throw(AssertionError("No class or div found")), lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None")), lambda el: None if (el is not None and str(el)) else (_ for _ in ()).throw(AssertionError("Invalid element"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
