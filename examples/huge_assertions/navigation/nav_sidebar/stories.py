"""The subject for the NavSidebar component."""

from examples.huge_assertions.navigation.nav_sidebar.nav_sidebar import NavSidebar
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for NavSidebar component."""
    return Subject(
        title="Nav Sidebar",
        description="Sidebar navigation",
        target=NavSidebar,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
