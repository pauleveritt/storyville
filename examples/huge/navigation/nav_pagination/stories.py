"""The subject for the NavPagination component."""

from examples.huge.navigation.nav_pagination.nav_pagination import NavPagination
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for NavPagination component."""
    return Subject(
        title="Nav Pagination",
        description="Pagination control",
        target=NavPagination,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
