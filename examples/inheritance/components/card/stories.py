"""Stories for the Card component demonstrating field inheritance."""

from __future__ import annotations

from examples.inheritance.components.card.badge import Badge
from examples.inheritance.components.card.card import Card
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for Card component demonstrating field inheritance patterns."""
    return Subject(
        target=Card,
        items=[
            # Story 1: No title (inherits auto-generated from Subject), props for Card
            Story(props={"title": "First Card", "text": "This story inherits its title from the Subject"}),
            # Story 2: Explicit title, props for Card
            Story(
                title="Custom Card Title",
                props={"title": "Second Card", "text": "This story has an explicit title"},
            ),
            # Story 3: target override - different component (Badge instead of Card)
            Story(
                target=Badge,
                props={"count": 42},
            ),
            # Story 4: No title (inherits), different Card props
            Story(props={"title": "Third Card", "text": "Another story with inherited title"}),
        ],
    )
