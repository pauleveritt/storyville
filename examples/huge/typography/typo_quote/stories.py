"""The subject for the TypoQuote component."""

from examples.huge.typography.typo_quote.typo_quote import TypoQuote
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for TypoQuote component."""
    return Subject(
        title="Typo Quote",
        description="Quote text",
        target=TypoQuote,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
