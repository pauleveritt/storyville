"""Tests for Layout component."""

from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name
from tdom import Element, Fragment, Node
from typing import cast

from storytime.section import Section
from storytime.site.models import Site
from storytime.components.layout.layout import Layout
from tdom import html


def _get_element(result: Node) -> Element:
    """Extract Element from result (handles Fragment wrapper)."""
    if isinstance(result, Fragment):
        # Fragment contains the html element as first child
        for child in result.children:
            if isinstance(child, Element):
                return child
        raise ValueError("No Element found in Fragment")
    return cast(Element, result)


def test_layout_renders_complete_html_structure() -> None:
    """Test Layout renders complete HTML structure with html, head, body tags."""
    site = Site(title="My Site")
    layout = Layout(view_title="Test Page", site=site, children=None)
    result = layout()

    # Extract Element from Fragment if needed
    element = _get_element(result)

    # Verify html tag is the root
    assert element.tag == "html"

    # Verify head exists
    get_by_tag_name(element, "head")

    # Verify body exists
    get_by_tag_name(element, "body")


def test_layout_includes_meta_tags() -> None:
    """Test Layout includes meta charset and viewport tags in head."""
    site = Site(title="My Site")
    layout = Layout(view_title="Test Page", site=site, children=None)
    result = layout()

    # Extract Element from Fragment if needed
    element = _get_element(result)

    # Get all meta tags
    head = get_by_tag_name(element, "head")
    meta_tags = query_all_by_tag_name(head, "meta")

    # Verify we have at least 2 meta tags (charset and viewport)
    assert len(meta_tags) >= 2

    # Check for charset meta
    charset_metas = [m for m in meta_tags if m.attrs.get("charset") == "utf-8"]
    assert len(charset_metas) == 1

    # Check for viewport meta
    viewport_metas = [m for m in meta_tags if m.attrs.get("name") == "viewport"]
    assert len(viewport_metas) == 1


def test_layout_title_concatenates_view_title_and_site_title() -> None:
    """Test Layout title concatenates view_title and site.title correctly."""
    site = Site(title="My Site")
    layout = Layout(view_title="Home", site=site, children=None)
    result = layout()

    # Extract Element from Fragment if needed
    element = _get_element(result)

    # Get title element
    title = get_by_tag_name(element, "title")
    title_text = get_text_content(title)

    # Verify concatenation with hyphen
    assert title_text == "Home - My Site"


def test_layout_title_uses_only_site_title_when_view_title_is_none() -> None:
    """Test Layout title uses only site.title when view_title is None."""
    site = Site(title="My Site")
    layout = Layout(view_title=None, site=site, children=None)
    result = layout()

    # Extract Element from Fragment if needed
    element = _get_element(result)

    # Get title element
    title = get_by_tag_name(element, "title")
    title_text = get_text_content(title)

    # Verify no hyphen when view_title is None
    assert title_text == "My Site"
    assert " - " not in title_text


def test_layout_inserts_children_content_into_main() -> None:
    """Test Layout inserts children content into main element."""
    site = Site(title="My Site")

    # Create some children content
    children = html(t"<div><p>Test Content</p></div>")

    layout = Layout(view_title="Test", site=site, children=children)
    result = layout()

    # Extract Element from Fragment if needed
    element = _get_element(result)

    # Get main element
    main = get_by_tag_name(element, "main")

    # Verify children content is in main or its descendants
    main_text = get_text_content(main)
    assert "Test Content" in main_text


def test_layout_includes_navigation_bar() -> None:
    """Test Layout includes navigation bar with site branding."""
    site = Site(title="My Site")
    layout = Layout(view_title="Test", site=site, children=None)
    result = layout()

    # Extract Element from Fragment if needed
    element = _get_element(result)

    # Get nav element
    nav = get_by_tag_name(element, "nav")

    # Verify nav has correct role and aria-label
    assert nav.attrs.get("role") == "navigation"

    # Verify "Storytime" branding is present
    nav_text = get_text_content(nav)
    assert "Storytime" in nav_text


def test_layout_includes_sidebar_with_sections() -> None:
    """Test Layout includes sidebar with SectionsListing component."""
    site = Site(title="My Site")

    # Add sections to site
    section1 = Section(title="Components")
    section2 = Section(title="Utilities")
    site.items = {"components": section1, "utilities": section2}

    layout = Layout(view_title="Test", site=site, children=None)
    result = layout()

    # Extract Element from Fragment if needed
    element = _get_element(result)

    # Get aside element (sidebar)
    aside = get_by_tag_name(element, "aside")

    # Verify aside has menu class
    class_attr = aside.attrs.get("class", "")
    assert class_attr is not None
    assert "menu" in class_attr


def test_layout_satisfies_view_protocol() -> None:
    """Test Layout satisfies View Protocol (__call__() -> Node)."""
    site = Site(title="My Site")
    layout = Layout(view_title="Test", site=site, children=None)

    # Verify __call__ returns Node (verified by type checker)
    result = layout()

    # Runtime verification that result is a Node (Element or Fragment)
    assert isinstance(result, (Element, Fragment))
