"""Test the SiteView rendering."""

from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name
from tdom import Element

from storytime.section import Section
from storytime.site.models import Site
from storytime.site.views import SiteView
from storytime.subject import Subject


def test_site_view_renders_title_in_h1() -> None:
    """Test SiteView renders site title in h1 element."""
    site = Site(title="My Catalog")
    view = SiteView(site=site)
    result = view()

    # Type guard in test to verify Element
    assert isinstance(result, Element)

    # Verify title is in h1
    h1 = get_by_tag_name(result, "h1")
    assert get_text_content(h1) == "My Catalog"


def test_site_view_renders_section_links() -> None:
    """Test SiteView renders section links when sections exist."""
    site = Site(title="My Catalog")
    site.package_path = "."

    # Add sections to site
    section1 = Section(title="Components")
    section2 = Section(title="Utilities")
    site.items = {"components": section1, "utilities": section2}

    view = SiteView(site=site)
    result = view()

    # Type guard in test to verify Element
    assert isinstance(result, Element)

    # Verify ul element exists
    get_by_tag_name(result, "ul")

    # Verify section cards are rendered as links
    all_links = query_all_by_tag_name(result, "a")

    assert len(all_links) == 2
    # Links can be in any order since dict iteration order may vary
    link_texts = {get_text_content(link) for link in all_links}
    assert link_texts == {"Components", "Utilities"}


def test_site_view_shows_empty_state() -> None:
    """Test SiteView shows empty state message when no sections."""
    site = Site(title="Empty Catalog")
    view = SiteView(site=site)
    result = view()

    # Type guard in test to verify Element
    assert isinstance(result, Element)

    # Verify empty state message
    all_p_tags = query_all_by_tag_name(result, "p")
    empty_state_found = any(
        "No sections defined for this site" in get_text_content(p)
        for p in all_p_tags
    )
    assert empty_state_found


def test_site_view_does_not_include_parent_link() -> None:
    """Test SiteView does NOT include parent link (Site is root)."""
    site = Site(title="My Catalog")
    view = SiteView(site=site)
    result = view()

    # Type guard in test to verify Element
    assert isinstance(result, Element)

    # Verify NO parent link exists (Site has no parent)
    all_links = query_all_by_tag_name(result, "a")
    parent_links = [link for link in all_links if link.attrs.get("href") == ".."]
    assert len(parent_links) == 0


def test_site_view_satisfies_view_protocol() -> None:
    """Test SiteView satisfies View Protocol (__call__() -> Node)."""
    site = Site(title="My Catalog")
    view = SiteView(site=site)

    # Verify __call__ returns Node (verified by type checker)
    result = view()

    # Runtime verification that result is an Element (which is a Node)
    assert isinstance(result, Element)


def test_site_view_shows_section_descriptions() -> None:
    """Test SiteView shows section descriptions when present."""
    site = Site(title="My Catalog")
    section1 = Section(title="Components", description="UI building blocks")
    section2 = Section(title="Utilities", description="Helper functions")
    site.items = {"components": section1, "utilities": section2}

    view = SiteView(site=site)
    result = view()

    # Type guard
    assert isinstance(result, Element)

    # Get all text content and verify descriptions are present
    text_content = get_text_content(result)
    assert "UI building blocks" in text_content
    assert "Helper functions" in text_content


def test_site_view_omits_none_descriptions() -> None:
    """Test SiteView omits descriptions when None."""
    site = Site(title="My Catalog")
    section1 = Section(title="Components", description=None)
    section2 = Section(title="Utilities", description="Helper functions")
    site.items = {"components": section1, "utilities": section2}

    view = SiteView(site=site)
    result = view()

    # Type guard
    assert isinstance(result, Element)

    # Get all text content
    text_content = get_text_content(result)
    # Section with description shows it
    assert "Helper functions" in text_content
    # No placeholder text for None description
    assert "None" not in text_content


def test_site_view_shows_subject_counts() -> None:
    """Test SiteView shows correct subject counts for each section."""
    site = Site(title="My Catalog")

    # Section 1 with 3 subjects
    section1 = Section(title="Components")
    section1.items = {
        "button": Subject(title="Button"),
        "input": Subject(title="Input"),
        "card": Subject(title="Card"),
    }

    # Section 2 with 1 subject
    section2 = Section(title="Utilities")
    section2.items = {
        "helpers": Subject(title="Helpers"),
    }

    site.items = {"components": section1, "utilities": section2}

    view = SiteView(site=site)
    result = view()

    # Type guard
    assert isinstance(result, Element)

    # Get all text content and verify subject counts
    text_content = get_text_content(result)
    assert "3 subjects" in text_content
    assert "1 subject" in text_content


def test_site_view_url_pattern() -> None:
    """Test SiteView uses /section/{section_name} URL pattern."""
    site = Site(title="My Catalog")
    section1 = Section(title="Components")
    section2 = Section(title="Utilities")
    site.items = {"components": section1, "utilities": section2}

    view = SiteView(site=site)
    result = view()

    # Type guard
    assert isinstance(result, Element)

    # Verify section links follow /section/{section_name} pattern
    all_links = query_all_by_tag_name(result, "a")
    hrefs = {link.attrs.get("href") for link in all_links}
    assert "/section/components" in hrefs
    assert "/section/utilities" in hrefs
