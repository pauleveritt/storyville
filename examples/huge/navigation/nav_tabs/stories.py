"""The subject for the NavTabs component."""

from examples.huge.navigation.nav_tabs.nav_tabs import NavTabs
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for NavTabs component."""
    return Subject(
        title="Nav Tabs",
        description="Tab navigation",
        target=NavTabs,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
