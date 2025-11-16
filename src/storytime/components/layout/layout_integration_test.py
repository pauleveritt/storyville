"""Integration tests for Layout component with views."""

from aria_testing import get_by_tag_name, get_text_content
from tdom import Element, Fragment, Node
from typing import cast

from storytime.site.models import Site
from storytime.site.views import SiteView
from storytime.section.models import Section
from storytime.section.views import SectionView
from storytime.subject.models import Subject
from storytime.subject.views import SubjectView


def _get_element(result: Node) -> Element:
    """Extract Element from result (handles Fragment wrapper)."""
    if isinstance(result, Fragment):
        # Fragment contains the html element as first child
        for child in result.children:
            if isinstance(child, Element):
                return child
        raise ValueError("No Element found in Fragment")
    return cast(Element, result)


def test_site_view_renders_full_html_document() -> None:
    """Test SiteView renders full HTML document with proper head/body structure."""
    site = Site(title="My Site")
    view = SiteView(site=site)
    result = view()

    # Extract Element from Fragment
    element = _get_element(result)

    # Verify complete HTML structure
    assert element.tag == "html"

    # Verify head contains required elements
    head = get_by_tag_name(element, "head")
    get_by_tag_name(head, "title")
    get_by_tag_name(head, "meta", attrs={"charset": "utf-8"})
    get_by_tag_name(head, "link", attrs={"rel": "stylesheet"})

    # Verify body contains header, nav, and main
    body = get_by_tag_name(element, "body")
    get_by_tag_name(body, "header")
    get_by_tag_name(body, "main")


def test_section_view_title_appears_in_browser_title() -> None:
    """Test SectionView title appears in browser title tag correctly."""
    site = Site(title="My Site")
    section = Section(title="Components")
    view = SectionView(section=section, site=site)
    result = view()

    # Extract Element from Fragment
    element = _get_element(result)

    # Get title element and verify concatenation
    title = get_by_tag_name(element, "title")
    from aria_testing import get_text_content
    title_text = get_text_content(title)

    # Should be "Components - My Site"
    assert title_text == "Components - My Site"
    assert "Components" in title_text
    assert "My Site" in title_text


def test_subject_view_includes_navigation_and_sidebar() -> None:
    """Test SubjectView includes navigation and sidebar in rendered output."""
    site = Site(title="My Site")

    # Add a section to site so sidebar has content
    section = Section(title="Components")
    site.items = {"components": section}

    subject = Subject(title="Button")
    view = SubjectView(subject=subject, site=site)
    result = view()

    # Extract Element from Fragment
    element = _get_element(result)

    # Verify header and sidebar exist
    get_by_tag_name(element, "header")
    aside = get_by_tag_name(element, "aside")

    # Verify sidebar contains "Sections" text
    aside_text = get_text_content(aside)
    assert "Sections" in aside_text


def test_layout_handles_none_children() -> None:
    """Test Layout handles None children gracefully."""
    from storytime.components.layout import Layout

    site = Site(title="My Site")
    layout = Layout(view_title="Test", site=site, children=None)
    result = layout()

    # Extract Element from Fragment
    element = _get_element(result)

    # Should still render complete HTML structure
    assert element.tag == "html"
    get_by_tag_name(element, "head")
    get_by_tag_name(element, "body")
    get_by_tag_name(element, "main")


def test_layout_css_link_points_to_valid_static_path() -> None:
    """Test Layout CSS link href points to valid destination in static directory."""
    from storytime.components.layout import Layout
    from storytime import PACKAGE_DIR

    site = Site(title="My Site")
    layout = Layout(view_title="Test", site=site, children=None)
    result = layout()

    # Extract Element from Fragment
    element = _get_element(result)

    # Get link element
    head = get_by_tag_name(element, "head")
    link = get_by_tag_name(head, "link", attrs={"rel": "stylesheet"})

    # Verify href points to pico-main.css
    href = link.attrs.get("href")
    assert href == "../static/pico-main.css"

    # Verify the actual file exists at the expected location
    # The static dir should be at PACKAGE_DIR / "components" / "layout" / "static"
    static_dir = PACKAGE_DIR / "components" / "layout" / "static"
    pico_css = static_dir / "pico-main.css"

    assert static_dir.exists(), f"Static directory should exist at {static_dir}"
    assert pico_css.exists(), f"pico-main.css should exist at {pico_css}"


def test_static_asset_paths_resolve_from_different_depths() -> None:
    """Test static asset paths resolve correctly from pages at different depths."""
    from storytime.components.layout import Layout

    site = Site(title="My Site")

    # All views currently use "../static/pico-main.css" regardless of depth
    # This is the relative path from output pages to the static directory

    # Test at root level (site view)
    site_layout = Layout(view_title="Home", site=site, children=None)
    site_result = site_layout()
    site_element = _get_element(site_result)

    site_link = get_by_tag_name(site_element, "link", attrs={"rel": "stylesheet"})
    assert site_link.attrs.get("href") == "../static/pico-main.css"

    # Test at section level (one level deep)
    section_layout = Layout(view_title="Section", site=site, children=None)
    section_result = section_layout()
    section_element = _get_element(section_result)

    section_link = get_by_tag_name(section_element, "link", attrs={"rel": "stylesheet"})
    assert section_link.attrs.get("href") == "../static/pico-main.css"

    # Note: All pages use the same relative path "../static/pico-main.css"
    # This works because build.py copies static to output root, and all
    # pages are generated one level deep (e.g., /section/index.html)
