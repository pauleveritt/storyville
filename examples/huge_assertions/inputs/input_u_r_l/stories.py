"""The subject for the InputURL component."""

from examples.huge_assertions.inputs.input_u_r_l.input_u_r_l import InputURL
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for InputURL component."""
    return Subject(
        title="Input URL",
        description="URL input",
        target=InputURL,
        items=[
            Story(
                props=dict(text="Default", variant="primary", state="default"),
                assertions=[
                    lambda el: None
                    if (el is not None and str(el))
                    else (_ for _ in ()).throw(AssertionError("Invalid element"))
                ],
            ),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
