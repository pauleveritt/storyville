"""The subject for the NavDropdown component."""

from examples.huge.navigation.nav_dropdown.nav_dropdown import NavDropdown
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for NavDropdown component."""
    return Subject(
        title="Nav Dropdown",
        description="Dropdown menu",
        target=NavDropdown,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
