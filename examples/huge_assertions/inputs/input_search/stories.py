"""The subject for the InputSearch component."""

from examples.huge_assertions.inputs.input_search.input_search import InputSearch
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for InputSearch component."""
    return Subject(
        title="Input Search",
        description="Search input",
        target=InputSearch,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(
                props=dict(text="Disabled", variant="secondary", state="disabled"),
                assertions=[
                    lambda el: None
                    if len(str(el)) > 10
                    else (_ for _ in ()).throw(AssertionError("Element too short"))
                ],
            ),
            Story(
                props=dict(text="Loading", variant="primary", state="loading"),
                assertions=[
                    lambda el: None
                    if (el is not None and str(el))
                    else (_ for _ in ()).throw(AssertionError("Invalid element"))
                ],
            ),
        ],
    )
