"""The subject for the InputPassword component."""

from examples.huge_assertions.inputs.input_password.input_password import InputPassword
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for InputPassword component."""
    return Subject(
        title="Input Password",
        description="Password input",
        target=InputPassword,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found"))]),
        ],
    )
