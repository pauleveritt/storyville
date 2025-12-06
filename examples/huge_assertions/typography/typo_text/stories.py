"""The subject for the TypoText component."""

from examples.huge_assertions.typography.typo_text.typo_text import TypoText
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for TypoText component."""
    return Subject(
        title="Typo Text",
        description="Body text",
        target=TypoText,
        items=[
            Story(
                props=dict(text="Default", variant="primary", state="default"),
                assertions=[
                    lambda el: None
                    if len(str(el)) > 10
                    else (_ for _ in ()).throw(AssertionError("Element too short")),
                    lambda el: None
                    if str(el).find("<") != -1
                    else (_ for _ in ()).throw(AssertionError("No HTML tags found")),
                ],
            ),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
