"""The subject for the InputSearch component."""

from examples.huge.inputs.input_search.input_search import InputSearch
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for InputSearch component."""
    return Subject(
        title="Input Search",
        description="Search input",
        target=InputSearch,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
