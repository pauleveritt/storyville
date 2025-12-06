"""The subject for the TypoCode component."""

from examples.huge_assertions.typography.typo_code.typo_code import TypoCode
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for TypoCode component."""
    return Subject(
        title="Typo Code",
        description="Code text",
        target=TypoCode,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if len(str(el)) > 10 else (_ for _ in ()).throw(AssertionError("Element too short"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
