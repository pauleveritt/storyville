"""Test the SectionView rendering."""

from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name

from storyville.section.models import Section
from storyville.section.views import SectionView
from storyville.subject import Subject
from storyville.catalog.models import Catalog


def test_section_view_renders_title_in_h1() -> None:
    """Test SectionView renders section title in h1 element."""
    catalog = Catalog(title="My Catalog")
    section = Section(title="Components")
    view = SectionView(section=section, site=catalog)
    result = view()

    # Extract  from  (Layout wraps the result)
    element = result

    # Verify title is in h1
    h1 = get_by_tag_name(element, "h1")
    assert get_text_content(h1) == "Components"


def test_section_view_renders_description() -> None:
    """Test SectionView renders description when present."""
    catalog = Catalog(title="My Catalog")
    section = Section(title="Components", description="UI component library")
    view = SectionView(section=section, site=catalog)
    result = view()

    # Extract  from  (Layout wraps the result)
    element = result

    # Verify description is rendered in a p element
    all_p_tags = query_all_by_tag_name(element, "p")
    description_found = any(
        "UI component library" in get_text_content(p) for p in all_p_tags
    )
    assert description_found


def test_section_view_renders_subject_cards() -> None:
    """Test SectionView renders subject cards as list with title and link."""
    catalog = Catalog(title="My Catalog")
    section = Section(title="Components")
    section.package_path = ".components"

    # Add subjects to section
    subject1 = Subject(title="Button")
    subject2 = Subject(title="Input")
    section.items = {"button": subject1, "input": subject2}

    view = SectionView(section=section, site=catalog)
    result = view()

    # Extract  from  (Layout wraps the result)
    element = result

    # Get the main element (content area) to avoid sidebar sections listing
    main = get_by_tag_name(element, "main")

    # Verify subject cards are rendered as links (no parent link anymore)
    all_links = query_all_by_tag_name(main, "a")

    # Should have 2 subject links (parent link has been removed and replaced by breadcrumbs)
    assert len(all_links) == 2
    # Links can be in any order since dict iteration order may vary
    link_texts = {get_text_content(link) for link in all_links}
    assert link_texts == {"Button", "Input"}


def test_section_view_shows_empty_state() -> None:
    """Test SectionView shows empty state message when no subjects."""
    catalog = Catalog(title="My Catalog")
    section = Section(title="Empty Section")
    view = SectionView(section=section, site=catalog)
    result = view()

    # Extract  from  (Layout wraps the result)
    element = result

    # Verify empty state message
    all_p_tags = query_all_by_tag_name(element, "p")
    empty_state_found = any(
        "No subjects defined for this section" in get_text_content(p)
        for p in all_p_tags
    )
    assert empty_state_found


def test_section_view_has_breadcrumbs() -> None:
    """Test SectionView includes breadcrumbs navigation (replaces parent link)."""
    catalog = Catalog(title="My Catalog")
    section = Section(title="Components")
    section.resource_path = "components"
    view = SectionView(section=section, site=catalog, resource_path="components")
    result = view()

    # Extract  from  (Layout wraps the result)
    element = result

    # Get the main element (content area)
    main = get_by_tag_name(element, "main")

    # Verify breadcrumbs navigation exists (replaces parent link)
    nav = get_by_tag_name(main, "nav")
    assert nav is not None
    assert nav.attrs.get("aria-label") == "Breadcrumb"
