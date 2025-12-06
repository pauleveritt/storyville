"""Card component with sample stories and assertions."""

from dataclasses import dataclass

from tdom import Element, Fragment, Node, html


@dataclass
class Card:
    """A card component for displaying content with title and optional image.

    Args:
        title: The card title.
        content: The card body content.
        image_url: Optional URL for card image.
    """

    title: str
    content: str
    image_url: str | None = None

    def __call__(self) -> Node:
        """Render the card using tdom.

        Returns:
            Node: The rendered card element.
        """
        card_style = (
            "border: 1px solid #ddd; border-radius: 8px; padding: 20px; "
            "background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1);"
        )

        img_style = "width: 100%; border-radius: 6px; margin-bottom: 16px;"
        image_html = (
            f'<img src="{self.image_url}" alt="{self.title}" style="{img_style}">'
            if self.image_url
            else ""
        )

        return html(t'''
<div class="card" style="{card_style}">
  {image_html}
  <h3 style="margin: 0 0 12px 0; color: #333;">{self.title}</h3>
  <p style="margin: 0; color: #666; line-height: 1.6;">{self.content}</p>
</div>
        ''')


# Sample assertion functions


def check_is_card_div(el: Element | Fragment) -> None:
    """Assert that the card renders as a div element.

    Args:
        el: The rendered element to check.

    Raises:
        AssertionError: If the element is not a div.
    """
    rendered = str(el)
    assert "<div" in rendered, "Card should render as a div element"


def check_has_title_heading(el: Element | Fragment) -> None:
    """Assert that the card contains a heading element.

    Args:
        el: The rendered element to check.

    Raises:
        AssertionError: If no heading is found.
    """
    rendered = str(el)
    assert "<h3" in rendered, "Card should contain an h3 heading for title"


def check_has_content_paragraph(el: Element | Fragment) -> None:
    """Assert that the card contains paragraph content.

    Args:
        el: The rendered element to check.

    Raises:
        AssertionError: If no paragraph is found.
    """
    rendered = str(el)
    assert "<p" in rendered, "Card should contain a paragraph for content"
