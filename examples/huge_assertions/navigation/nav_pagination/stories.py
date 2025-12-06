"""The subject for the NavPagination component."""

from examples.huge_assertions.navigation.nav_pagination.nav_pagination import (
    NavPagination,
)
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for NavPagination component."""
    return Subject(
        title="Nav Pagination",
        description="Pagination control",
        target=NavPagination,
        items=[
            Story(
                props=dict(text="Default", variant="primary", state="default"),
                assertions=[
                    lambda el: None
                    if (el is not None and str(el))
                    else (_ for _ in ()).throw(AssertionError("Invalid element")),
                    lambda el: None
                    if "class" in str(el).lower() or "div" in str(el).lower()
                    else (_ for _ in ()).throw(AssertionError("No class or div found")),
                ],
            ),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(
                props=dict(text="Loading", variant="primary", state="loading"),
                assertions=[
                    lambda el: None
                    if "class" in str(el).lower() or "div" in str(el).lower()
                    else (_ for _ in ()).throw(AssertionError("No class or div found")),
                    lambda el: None
                    if (el is not None and str(el))
                    else (_ for _ in ()).throw(AssertionError("Invalid element")),
                ],
            ),
        ],
    )
