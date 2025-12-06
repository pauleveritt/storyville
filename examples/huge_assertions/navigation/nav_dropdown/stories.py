"""The subject for the NavDropdown component."""

from examples.huge_assertions.navigation.nav_dropdown.nav_dropdown import NavDropdown
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for NavDropdown component."""
    return Subject(
        title="Nav Dropdown",
        description="Dropdown menu",
        target=NavDropdown,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if "class" in str(el).lower() or "div" in str(el).lower() else (_ for _ in ()).throw(AssertionError("No class or div found")), lambda el: None if len(str(el)) > 10 else (_ for _ in ()).throw(AssertionError("Element too short")), lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if len(str(el)) > 10 else (_ for _ in ()).throw(AssertionError("Element too short"))]),
        ],
    )
