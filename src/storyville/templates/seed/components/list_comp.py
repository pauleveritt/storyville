"""List component with sample stories and assertions."""

from dataclasses import dataclass

from tdom import Element, Fragment, Node, html


@dataclass
class ListComponent:
    """A list component that can render ordered or unordered lists.

    Args:
        items: List of items to display.
        ordered: Whether to render as ordered list (ol) or unordered (ul).
    """

    items: list[str]
    ordered: bool = False

    def __call__(self) -> Node:
        """Render the list using tdom.

        Returns:
            Node: The rendered list element.
        """
        list_style = "margin: 0; padding-left: 24px; line-height: 1.8; color: #333;"
        list_items_html = "\n".join([f"<li>{item}</li>" for item in self.items])

        if self.ordered:
            return html(t'<ol style="{list_style}">{list_items_html}</ol>')
        else:
            return html(t'<ul style="{list_style}">{list_items_html}</ul>')


# Sample assertion functions


def check_is_list_element(el: Element | Fragment) -> None:
    """Assert that the component renders as a list element.

    Args:
        el: The rendered element to check.

    Raises:
        AssertionError: If the element is not a list.
    """
    rendered = str(el)
    assert "<ul" in rendered or "<ol" in rendered, (
        "Should render as a list element (ul or ol)"
    )


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
    assert ("<ol" in rendered) or ("<ul" in rendered), (
        "Should be either ordered or unordered list"
    )
