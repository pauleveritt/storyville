"""The subject for the LayoutContainer component."""

from examples.huge_assertions.layout.layout_container.layout_container import (
    LayoutContainer,
)
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for LayoutContainer component."""
    return Subject(
        title="Layout Container",
        description="Container for layout",
        target=LayoutContainer,
        items=[
            Story(
                props=dict(text="Default", variant="primary", state="default"),
                assertions=[
                    lambda el: None
                    if "class" in str(el).lower() or "div" in str(el).lower()
                    else (_ for _ in ()).throw(AssertionError("No class or div found")),
                    lambda el: None
                    if any(tag in str(el) for tag in ["div", "span", "button", "input"])
                    else (_ for _ in ()).throw(AssertionError("No common tags")),
                    lambda el: None
                    if str(el).find("<") != -1
                    else (_ for _ in ()).throw(AssertionError("No HTML tags found")),
                ],
            ),
            Story(
                props=dict(text="Disabled", variant="secondary", state="disabled"),
                assertions=[
                    lambda el: None
                    if len(str(el)) > 10
                    else (_ for _ in ()).throw(AssertionError("Element too short"))
                ],
            ),
            Story(
                props=dict(text="Loading", variant="primary", state="loading"),
                assertions=[
                    lambda el: None
                    if hasattr(el, "__html__")
                    else (_ for _ in ()).throw(
                        AssertionError("Missing __html__ attribute")
                    ),
                    lambda el: None
                    if (el is not None and str(el))
                    else (_ for _ in ()).throw(AssertionError("Invalid element")),
                ],
            ),
        ],
    )
