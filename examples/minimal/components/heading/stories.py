"""The subject for this Heading component."""

from __future__ import annotations

from storytime import Story, Subject


def this_subject() -> Subject:
    """Let's make a Storytime subject for this Heading component."""
    return Subject(
        title="Heading",
        items=[
            Story(),
        ],
    )
