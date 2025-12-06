"""Form component with sample stories and assertions."""

from dataclasses import dataclass, field

import tdom
from tdom import Element, Fragment


@dataclass
class FormField:
    """A form field definition.

    Args:
        name: The field name.
        label: The field label text.
        type: The input type (text, email, password, etc.).
        required: Whether the field is required.
    """

    name: str
    label: str
    type: str = "text"
    required: bool = False


@dataclass
class Form:
    """A form component with configurable fields.

    Args:
        fields: List of form fields to render.
        submit_text: The submit button text.
    """

    fields: list[FormField] = field(default_factory=list)
    submit_text: str = "Submit"

    def __call__(self) -> tdom.html.form:
        """Render the form using tdom.

        Returns:
            tdom.html.form: The rendered form element.
        """
        form_style = "max-width: 400px; padding: 24px; border: 1px solid #ddd; border-radius: 8px;"
        field_style = "margin-bottom: 16px;"
        label_style = (
            "display: block; margin-bottom: 4px; font-weight: 600; color: #333;"
        )
        input_style = (
            "width: 100%; padding: 10px; border: 1px solid #ccc; "
            "border-radius: 4px; font-size: 14px; box-sizing: border-box;"
        )
        button_style = (
            "background: #667eea; color: white; padding: 12px 24px; "
            "border: none; border-radius: 6px; cursor: pointer; font-weight: 600;"
        )

        field_nodes = [
            tdom.html.div(
                tdom.html.label(
                    f"{field.label}{'*' if field.required else ''}",
                    for_=field.name,
                    style=label_style,
                ),
                tdom.html.input(
                    type=field.type,
                    name=field.name,
                    id=field.name,
                    required=field.required,
                    style=input_style,
                ),
                style=field_style,
            )
            for field in self.fields
        ]

        return tdom.html.form(
            *field_nodes,
            tdom.html.button(self.submit_text, type="submit", style=button_style),
            style=form_style,
        )


# Sample assertion functions


def check_is_form_element(el: Element | Fragment) -> None:
    """Assert that the component renders as a form element.

    Args:
        el: The rendered element to check.

    Raises:
        AssertionError: If the element is not a form.
    """
    rendered = str(el)
    assert "<form" in rendered, "Should render as a form element"


def check_has_input_fields(el: Element | Fragment) -> None:
    """Assert that the form contains input elements.

    Args:
        el: The rendered element to check.

    Raises:
        AssertionError: If no inputs are found.
    """
    rendered = str(el)
    assert "<input" in rendered, "Form should contain input fields"


def check_has_submit_button(el: Element | Fragment) -> None:
    """Assert that the form has a submit button.

    Args:
        el: The rendered element to check.

    Raises:
        AssertionError: If no submit button is found.
    """
    rendered = str(el)
    assert 'type="submit"' in rendered or "type='submit'" in rendered, (
        "Form should have a submit button"
    )
