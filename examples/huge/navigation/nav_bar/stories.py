"""The subject for the NavBar component."""

from examples.huge.navigation.nav_bar.nav_bar import NavBar
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for NavBar component."""
    return Subject(
        title="Nav Bar",
        description="Navigation bar",
        target=NavBar,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
