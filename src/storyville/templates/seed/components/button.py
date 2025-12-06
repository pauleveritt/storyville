"""Button component with sample stories and assertions."""

from dataclasses import dataclass

import tdom
from tdom import Element, Fragment


@dataclass
class Button:
    """A simple button component demonstrating prop variations.

    Args:
        text: The button text content.
        color: The button color variant (primary, secondary, danger).
        size: The button size (small, medium, large).
    """

    text: str
    color: str = "primary"
    size: str = "medium"

    def __call__(self) -> tdom.html.button:
        """Render the button using tdom.

        Returns:
            tdom.html.button: The rendered button element.
        """
        return tdom.html.button(
            self.text,
            class_=f"btn btn-{self.color} btn-{self.size}",
            style=self._get_styles(),
        )

    def _get_styles(self) -> str:
        """Generate inline styles based on props."""
        # Color styles
        color_map = {
            "primary": "background: #667eea; color: white;",
            "secondary": "background: #6c757d; color: white;",
            "danger": "background: #dc3545; color: white;",
        }

        # Size styles
        size_map = {
            "small": "padding: 8px 16px; font-size: 14px;",
            "medium": "padding: 12px 24px; font-size: 16px;",
            "large": "padding: 16px 32px; font-size: 18px;",
        }

        base_style = "border: none; border-radius: 6px; cursor: pointer; font-weight: 600;"
        return f"{base_style} {color_map.get(self.color, color_map['primary'])} {size_map.get(self.size, size_map['medium'])}"


# Sample assertion functions demonstrating testing patterns


def check_is_button_element(el: Element | Fragment) -> None:
    """Assert that the rendered element is a button tag.

    Args:
        el: The rendered element to check.

    Raises:
        AssertionError: If the element is not a button tag.
    """
    rendered = str(el)
    assert "<button" in rendered, "Should render as a button element"


def check_has_button_text(el: Element | Fragment) -> None:
    """Assert that the button contains expected text content.

    Args:
        el: The rendered element to check.

    Raises:
        AssertionError: If the button text is not found.
    """
    rendered = str(el)
    assert "Click" in rendered or "Submit" in rendered or "Button" in rendered, (
        "Button should contain text content"
    )


def check_has_color_class(el: Element | Fragment) -> None:
    """Assert that the button has a color variant class.

    Args:
        el: The rendered element to check.

    Raises:
        AssertionError: If no color class is found.
    """
    rendered = str(el)
    assert (
        "btn-primary" in rendered or "btn-secondary" in rendered or "btn-danger" in rendered
    ), "Button should have a color variant class"
