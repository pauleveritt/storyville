"""The subject for the TypoLink component."""

from examples.huge_assertions.typography.typo_link.typo_link import TypoLink
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for TypoLink component."""
    return Subject(
        title="Typo Link",
        description="Link text",
        target=TypoLink,
        items=[
            Story(
                props=dict(text="Default", variant="primary", state="default"),
                assertions=[
                    lambda el: None
                    if el is not None
                    else (_ for _ in ()).throw(AssertionError("Element is None"))
                ],
            ),
            Story(
                props=dict(text="Disabled", variant="secondary", state="disabled"),
                assertions=[
                    lambda el: None
                    if any(tag in str(el) for tag in ["div", "span", "button", "input"])
                    else (_ for _ in ()).throw(AssertionError("No common tags")),
                    lambda el: None
                    if str(el).find("<") != -1
                    else (_ for _ in ()).throw(AssertionError("No HTML tags found")),
                    lambda el: None
                    if len(str(el)) > 10
                    else (_ for _ in ()).throw(AssertionError("Element too short")),
                ],
            ),
            Story(
                props=dict(text="Loading", variant="primary", state="loading"),
                assertions=[
                    lambda el: None
                    if str(el).find("<") != -1
                    else (_ for _ in ()).throw(AssertionError("No HTML tags found")),
                    lambda el: None
                    if "class" in str(el).lower() or "div" in str(el).lower()
                    else (_ for _ in ()).throw(AssertionError("No class or div found")),
                ],
            ),
        ],
    )
