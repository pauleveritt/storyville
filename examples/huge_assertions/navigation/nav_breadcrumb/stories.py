"""The subject for the NavBreadcrumb component."""

from examples.huge_assertions.navigation.nav_breadcrumb.nav_breadcrumb import NavBreadcrumb
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for NavBreadcrumb component."""
    return Subject(
        title="Nav Breadcrumb",
        description="Breadcrumb navigation",
        target=NavBreadcrumb,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if len(str(el)) > 10 else (_ for _ in ()).throw(AssertionError("Element too short"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if hasattr(el, "__html__") else (_ for _ in ()).throw(AssertionError("Missing __html__ attribute"))]),
        ],
    )
