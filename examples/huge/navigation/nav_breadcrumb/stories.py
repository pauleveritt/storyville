"""The subject for the NavBreadcrumb component."""

from examples.huge.navigation.nav_breadcrumb.nav_breadcrumb import NavBreadcrumb
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for NavBreadcrumb component."""
    return Subject(
        title="Nav Breadcrumb",
        description="Breadcrumb navigation",
        target=NavBreadcrumb,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
