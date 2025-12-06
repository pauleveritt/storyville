"""Badge component with sample stories and assertions."""

from dataclasses import dataclass

from tdom import Element, Fragment, Node, html


@dataclass
class Badge:
    """A badge component for displaying labels or status indicators.

    Args:
        text: The badge text content.
        variant: The badge variant (success, warning, error, info).
    """

    text: str
    variant: str = "info"

    def __call__(self) -> Node:
        """Render the badge using tdom.

        Returns:
            Node: The rendered badge element.
        """
        styles = self._get_styles()
        return html(
            t'<span class="badge badge-{self.variant}" style="{styles}">{self.text}</span>'
        )

    def _get_styles(self) -> str:
        """Generate inline styles based on variant."""
        # Variant color map
        variant_map = {
            "success": "background: #28a745; color: white;",
            "warning": "background: #ffc107; color: #212529;",
            "error": "background: #dc3545; color: white;",
            "info": "background: #17a2b8; color: white;",
        }

        base_style = (
            "display: inline-block; padding: 6px 12px; font-size: 12px; "
            "font-weight: 600; border-radius: 12px; text-transform: uppercase; "
            "letter-spacing: 0.5px;"
        )

        return f"{base_style} {variant_map.get(self.variant, variant_map['info'])}"


# Sample assertion functions


def check_is_span_element(el: Element | Fragment) -> None:
    """Assert that the badge renders as a span element.

    Args:
        el: The rendered element to check.

    Raises:
        AssertionError: If the element is not a span.
    """
    rendered = str(el)
    assert "<span" in rendered, "Badge should render as a span element"


def check_has_badge_text(el: Element | Fragment) -> None:
    """Assert that the badge contains text content.

    Args:
        el: The rendered element to check.

    Raises:
        AssertionError: If no text is found.
    """
    rendered = str(el)
    # Simple check that there's content between tags
    assert ">" in rendered and "</" in rendered, "Badge should contain text content"


def check_has_variant_class(el: Element | Fragment) -> None:
    """Assert that the badge has a variant class.

    Args:
        el: The rendered element to check.

    Raises:
        AssertionError: If no variant class is found.
    """
    rendered = str(el)
    assert (
        "badge-success" in rendered
        or "badge-warning" in rendered
        or "badge-error" in rendered
        or "badge-info" in rendered
    ), "Badge should have a variant class"
