"""Assertion helpers for Story.assertions.

This package provides frozen dataclass-based assertion helpers that wrap
aria-testing queries for declarative, type-safe component assertions.

Example:
    from storyville.assertions import GetByRole, GetByText, GetAllByRole

    Story(
        props=dict(label="Submit"),
        assertions=[
            GetByRole(role="button"),
            GetByText(text="Submit").exact(),
            GetByRole(role="button").text_content("Submit"),
            GetAllByRole(role="button").count(3),
            GetAllByRole(role="button").nth(0).text_content("First"),
        ]
    )
"""

from storyville.assertions.helpers import (
    GetAllByClass,
    GetAllByLabelText,
    GetAllByRole,
    GetAllByTagName,
    GetAllByTestId,
    GetAllByText,
    GetByClass,
    GetById,
    GetByLabelText,
    GetByRole,
    GetByTagName,
    GetByTestId,
    GetByText,
)

__all__ = [
    # Single element helpers
    "GetByRole",
    "GetByText",
    "GetByLabelText",
    "GetByTestId",
    "GetByClass",
    "GetById",
    "GetByTagName",
    # List-oriented helpers
    "GetAllByRole",
    "GetAllByText",
    "GetAllByLabelText",
    "GetAllByTestId",
    "GetAllByClass",
    "GetAllByTagName",
]
