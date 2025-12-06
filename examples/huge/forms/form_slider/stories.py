"""The subject for the FormSlider component."""

from examples.huge.forms.form_slider.form_slider import FormSlider
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for FormSlider component."""
    return Subject(
        title="Form Slider",
        description="Slider for forms",
        target=FormSlider,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
