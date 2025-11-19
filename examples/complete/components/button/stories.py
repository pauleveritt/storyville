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
            # Story 1: Minimal props-only pattern with assertions
            Story(
                props=dict(text="Click Me", variant="primary"),
                assertions=[
                    # Simple assertion: verify element exists
                    lambda el: None
                    if el is not None
                    else (_ for _ in ()).throw(
                        AssertionError("Element should not be None")
                    ),
                    # Check for button tag
                    lambda el: None
                    if "button" in str(el).lower()
                    else (_ for _ in ()).throw(
                        AssertionError("Should contain button tag")
                    ),
                    # Verify variant class is present
                    lambda el: None
                    if "primary" in str(el)
                    else (_ for _ in ()).throw(
                        AssertionError("Should have primary variant class")
                    ),
                ],
            ),
            # Story 2: Story with custom title and description
            Story(
                title="Secondary Action Button",
                description="A button with secondary styling and custom metadata",
                props=dict(text="Learn More", variant="secondary"),
                assertions=[
                    # Verify button text appears in rendered output
                    lambda el: None
                    if "Learn More" in str(el)
                    else (_ for _ in ()).throw(
                        AssertionError("Button text should be in output")
                    ),
                    # Check for secondary variant
                    lambda el: None
                    if "secondary" in str(el)
                    else (_ for _ in ()).throw(
                        AssertionError("Should have secondary variant")
                    ),
                ],
            ),
            # Story 3: Different props for same component
            Story(
                props=dict(text="Cancel", variant="danger"),
                assertions=[
                    # Verify danger variant styling
                    lambda el: None
                    if "danger" in str(el)
                    else (_ for _ in ()).throw(
                        AssertionError("Should have danger variant")
                    ),
                ],
            ),
        ],
    )
