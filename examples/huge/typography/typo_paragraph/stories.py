"""The subject for the TypoParagraph component."""

from examples.huge.typography.typo_paragraph.typo_paragraph import TypoParagraph
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for TypoParagraph component."""
    return Subject(
        title="Typo Paragraph",
        description="Paragraph text",
        target=TypoParagraph,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
