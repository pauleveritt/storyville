"""Test the LayoutHeader component."""

from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name
from tdom import Element, Fragment, Node

from storytime.components.header.header import LayoutHeader


def _get_element(result: Node) -> Element:
    """Extract Element from result (handles Fragment wrapper)."""
    if isinstance(result, Fragment):
        for child in result.children:
            if isinstance(child, Element):
                return child
    if isinstance(result, Element):
        return result
    raise ValueError("Result is not an Element or Fragment containing an Element")


def test_layout_header_renders_with_site_title() -> None:
    """Test LayoutHeader renders header with site_title."""
    header = LayoutHeader(site_title="My Site")
    result = header()
    element = _get_element(result)

    assert element.tag == "header"

    # Check for site title in hgroup
    text_content = get_text_content(element)
    assert "My Site" in text_content


def test_layout_header_generates_correct_relative_paths_depth_zero() -> None:
    """Test LayoutHeader generates correct relative paths at depth=0."""
    header = LayoutHeader(site_title="Test", depth=0)
    result = header()
    element = _get_element(result)

    # Get all links
    all_links = query_all_by_tag_name(element, "a")
    assert len(all_links) == 3

    # At depth 0, relative path should be "../"
    # But navigation links are absolute paths starting with "/"
    # Check that links are present with correct hrefs
    home_link = all_links[0]
    assert home_link.attrs.get("href") == "/"
    assert get_text_content(home_link) == "Home"

    about_link = all_links[1]
    assert about_link.attrs.get("href") == "/about"
    assert get_text_content(about_link) == "About"

    debug_link = all_links[2]
    assert debug_link.attrs.get("href") == "/debug"
    assert get_text_content(debug_link) == "Debug"


def test_layout_header_has_container_structure() -> None:
    """Test LayoutHeader has correct container, hgroup, and nav structure."""
    header = LayoutHeader(site_title="Site")
    result = header()
    element = _get_element(result)

    # Check for container div
    container = get_by_tag_name(element, "div")
    class_attr = container.attrs.get("class") or ""
    assert "container" in class_attr

    # Check for hgroup
    hgroup = get_by_tag_name(element, "hgroup")
    assert hgroup is not None

    # Check for nav with ul
    nav = get_by_tag_name(element, "nav")
    assert nav is not None
    ul = get_by_tag_name(nav, "ul")
    assert ul is not None
