"""The subject for the NavLink component."""

from examples.huge_assertions.navigation.nav_link.nav_link import NavLink
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for NavLink component."""
    return Subject(
        title="Nav Link",
        description="Navigation link",
        target=NavLink,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(
                props=dict(text="Disabled", variant="secondary", state="disabled"),
                assertions=[
                    lambda el: None
                    if any(tag in str(el) for tag in ["div", "span", "button", "input"])
                    else (_ for _ in ()).throw(AssertionError("No common tags"))
                ],
            ),
            Story(
                props=dict(text="Loading", variant="primary", state="loading"),
                assertions=[
                    lambda el: None
                    if el is not None
                    else (_ for _ in ()).throw(AssertionError("Element is None"))
                ],
            ),
        ],
    )
