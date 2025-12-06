"""The subject for the FormSlider component."""

from examples.huge_assertions.forms.form_slider.form_slider import FormSlider
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for FormSlider component."""
    return Subject(
        title="Form Slider",
        description="Slider for forms",
        target=FormSlider,
        items=[
            Story(
                props=dict(text="Default", variant="primary", state="default"),
                assertions=[
                    lambda el: None
                    if "class" in str(el).lower() or "div" in str(el).lower()
                    else (_ for _ in ()).throw(AssertionError("No class or div found"))
                ],
            ),
            Story(
                props=dict(text="Disabled", variant="secondary", state="disabled"),
                assertions=[
                    lambda el: None
                    if len(str(el)) > 10
                    else (_ for _ in ()).throw(AssertionError("Element too short")),
                    lambda el: None
                    if hasattr(el, "__html__")
                    else (_ for _ in ()).throw(
                        AssertionError("Missing __html__ attribute")
                    ),
                ],
            ),
            Story(
                props=dict(text="Loading", variant="primary", state="loading"),
                assertions=[
                    lambda el: None
                    if hasattr(el, "__html__")
                    else (_ for _ in ()).throw(
                        AssertionError("Missing __html__ attribute")
                    )
                ],
            ),
        ],
    )
