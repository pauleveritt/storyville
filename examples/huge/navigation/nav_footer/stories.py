"""The subject for the NavFooter component."""

from examples.huge.navigation.nav_footer.nav_footer import NavFooter
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for NavFooter component."""
    return Subject(
        title="Nav Footer",
        description="Navigation footer",
        target=NavFooter,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
