"""The subject for the LayoutCard component."""

from examples.huge_assertions.layout.layout_card.layout_card import LayoutCard
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for LayoutCard component."""
    return Subject(
        title="Layout Card",
        description="Card container",
        target=LayoutCard,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(
                props=dict(text="Disabled", variant="secondary", state="disabled"),
                assertions=[
                    lambda el: None
                    if hasattr(el, "__html__")
                    else (_ for _ in ()).throw(
                        AssertionError("Missing __html__ attribute")
                    )
                ],
            ),
            Story(
                props=dict(text="Loading", variant="primary", state="loading"),
                assertions=[
                    lambda el: None
                    if any(tag in str(el) for tag in ["div", "span", "button", "input"])
                    else (_ for _ in ()).throw(AssertionError("No common tags")),
                    lambda el: None
                    if len(str(el)) > 10
                    else (_ for _ in ()).throw(AssertionError("Element too short")),
                ],
            ),
        ],
    )
