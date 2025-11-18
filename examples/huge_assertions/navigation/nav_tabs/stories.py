"""The subject for the NavTabs component."""

from examples.huge_assertions.navigation.nav_tabs.nav_tabs import NavTabs
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for NavTabs component."""
    return Subject(
        title="Nav Tabs",
        description="Tab navigation",
        target=NavTabs,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if len(str(el)) > 10 else (_ for _ in ()).throw(AssertionError("Element too short")), lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
