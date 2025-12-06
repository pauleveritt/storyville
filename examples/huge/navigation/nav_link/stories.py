"""The subject for the NavLink component."""

from examples.huge.navigation.nav_link.nav_link import NavLink
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for NavLink component."""
    return Subject(
        title="Nav Link",
        description="Navigation link",
        target=NavLink,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
