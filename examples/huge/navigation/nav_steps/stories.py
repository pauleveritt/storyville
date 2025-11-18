"""The subject for the NavSteps component."""

from examples.huge.navigation.nav_steps.nav_steps import NavSteps
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for NavSteps component."""
    return Subject(
        title="Nav Steps",
        description="Step indicator",
        target=NavSteps,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
