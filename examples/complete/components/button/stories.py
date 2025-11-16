"""The subject for the Button component."""


from examples.complete.components.button.button import Button
from storytime import Story, Subject


def this_subject() -> Subject:
    """Let's make a Storytime subject for this Button component."""
    return Subject(
        title="Button Component",
        description="A button component demonstrating all optional Story field variations",
        target=Button,
        items=[
            # Story 1: Minimal props-only pattern (inherits target from Subject)
            Story(props=dict(text="Click Me", variant="primary")),
            # Story 2: Story with custom title and description
            Story(
                title="Secondary Action Button",
                description="A button with secondary styling and custom metadata",
                props=dict(text="Learn More", variant="secondary"),
            ),
            # Story 3: Different props for same component
            Story(props=dict(text="Cancel", variant="danger")),
        ],
    )
