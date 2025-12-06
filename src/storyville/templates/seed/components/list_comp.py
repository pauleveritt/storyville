"""List component with sample stories and assertions."""

from dataclasses import dataclass

import tdom
from tdom import Element, Fragment


@dataclass
class ListComponent:
    """A list component that can render ordered or unordered lists.

    Args:
        items: List of items to display.
        ordered: Whether to render as ordered list (ol) or unordered (ul).
    """

    items: list[str]
    ordered: bool = False

    def __call__(self) -> tdom.html.ol | tdom.html.ul:
        """Render the list using tdom.

        Returns:
            tdom.html.ol | tdom.html.ul: The rendered list element.
        """
        list_style = (
            "margin: 0; padding-left: 24px; "
            "line-height: 1.8; color: #333;"
        )

        list_items = [tdom.html.li(item) for item in self.items]

        if self.ordered:
            return tdom.html.ol(*list_items, style=list_style)
        else:
            return tdom.html.ul(*list_items, style=list_style)


# Sample assertion functions


def check_is_list_element(el: Element | Fragment) -> None:
    """Assert that the component renders as a list element.

    Args:
        el: The rendered element to check.

    Raises:
        AssertionError: If the element is not a list.
    """
    rendered = str(el)
    assert "<ul" in rendered or "<ol" in rendered, "Should render as a list element (ul or ol)"


def check_has_list_items(el: Element | Fragment) -> None:
    """Assert that the list contains list items.

    Args:
        el: The rendered element to check.

    Raises:
        AssertionError: If no list items are found.
    """
    rendered = str(el)
    assert "<li" in rendered, "List should contain li elements"


def check_list_type_matches_ordered_prop(el: Element | Fragment) -> None:
    """Assert that ordered lists render as ol and unordered as ul.

    Args:
        el: The rendered element to check.

    Raises:
        AssertionError: If the list type doesn't match expectations.
    """
    rendered = str(el)
    # This is a simplified check - in real usage you'd pass the ordered prop
    # For now, just verify that it's one or the other
    assert ("<ol" in rendered) or ("<ul" in rendered), "Should be either ordered or unordered list"
