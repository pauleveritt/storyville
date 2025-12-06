"""The subject for the NavMenu component."""

from examples.huge.navigation.nav_menu.nav_menu import NavMenu
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for NavMenu component."""
    return Subject(
        title="Nav Menu",
        description="Navigation menu",
        target=NavMenu,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
