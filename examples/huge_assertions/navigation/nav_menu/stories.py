"""The subject for the NavMenu component."""

from examples.huge_assertions.navigation.nav_menu.nav_menu import NavMenu
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for NavMenu component."""
    return Subject(
        title="Nav Menu",
        description="Navigation menu",
        target=NavMenu,
        items=[
            Story(
                props=dict(text="Default", variant="primary", state="default"),
                assertions=[
                    lambda el: None
                    if "class" in str(el).lower() or "div" in str(el).lower()
                    else (_ for _ in ()).throw(AssertionError("No class or div found"))
                ],
            ),
            Story(
                props=dict(text="Disabled", variant="secondary", state="disabled"),
                assertions=[
                    lambda el: None
                    if hasattr(el, "__html__")
                    else (_ for _ in ()).throw(
                        AssertionError("Missing __html__ attribute")
                    ),
                    lambda el: None
                    if el is not None
                    else (_ for _ in ()).throw(AssertionError("Element is None")),
                ],
            ),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
