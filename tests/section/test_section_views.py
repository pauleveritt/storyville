"""Test the SectionView rendering."""

from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name
from tdom import Element, Fragment, Node
from typing import cast

from storytime.section.models import Section
from storytime.section.views import SectionView
from storytime.subject import Subject
from storytime.site.models import Site


def _get_element(result: Node) -> Element:
    """Extract Element from result (handles Fragment wrapper)."""
    if isinstance(result, Fragment):
        # Fragment contains the html element as first child
        for child in result.children:
            if isinstance(child, Element):
                return child
        raise ValueError("No Element found in Fragment")
    return cast(Element, result)


def test_section_view_renders_title_in_h1() -> None:
    """Test SectionView renders section title in h1 element."""
    site = Site(title="My Site")
    section = Section(title="Components")
    view = SectionView(section=section, site=site)
    result = view()

    # Extract Element from Fragment (Layout wraps the result)
    element = _get_element(result)

    # Verify title is in h1
    h1 = get_by_tag_name(element, "h1")
    assert get_text_content(h1) == "Components"


def test_section_view_renders_description() -> None:
    """Test SectionView renders description when present."""
    site = Site(title="My Site")
    section = Section(title="Components", description="UI component library")
    view = SectionView(section=section, site=site)
    result = view()

    # Extract Element from Fragment (Layout wraps the result)
    element = _get_element(result)

    # Verify description is rendered in a p element
    all_p_tags = query_all_by_tag_name(element, "p")
    description_found = any(
        "UI component library" in get_text_content(p)
        for p in all_p_tags
    )
    assert description_found


def test_section_view_renders_subject_cards() -> None:
    """Test SectionView renders subject cards as list with title and link."""
    site = Site(title="My Site")
    section = Section(title="Components")
    section.package_path = ".components"

    # Add subjects to section
    subject1 = Subject(title="Button")
    subject2 = Subject(title="Input")
    section.items = {"button": subject1, "input": subject2}

    view = SectionView(section=section, site=site)
    result = view()

    # Extract Element from Fragment (Layout wraps the result)
    element = _get_element(result)

    # Get the main element (content area) to avoid sidebar sections listing
    main = get_by_tag_name(element, "main")

    # Verify subject cards are rendered as links
    # Get the article element which contains the actual content (not sidebar)
    article = get_by_tag_name(main, "article")
    all_links = query_all_by_tag_name(article, "a")

    assert len(all_links) == 3  # 2 subject links + 1 parent link
    # Filter out parent link
    subject_links = [link for link in all_links if link.attrs.get("href") != ".."]

    assert len(subject_links) == 2
    # Links can be in any order since dict iteration order may vary
    link_texts = {get_text_content(link) for link in subject_links}
    assert link_texts == {"Button", "Input"}


def test_section_view_shows_empty_state() -> None:
    """Test SectionView shows empty state message when no subjects."""
    site = Site(title="My Site")
    section = Section(title="Empty Section")
    view = SectionView(section=section, site=site)
    result = view()

    # Extract Element from Fragment (Layout wraps the result)
    element = _get_element(result)

    # Verify empty state message
    all_p_tags = query_all_by_tag_name(element, "p")
    empty_state_found = any(
        "No subjects defined for this section" in get_text_content(p)
        for p in all_p_tags
    )
    assert empty_state_found


def test_section_view_includes_parent_link() -> None:
    """Test SectionView includes parent link."""
    site = Site(title="My Site")
    section = Section(title="Components")
    view = SectionView(section=section, site=site)
    result = view()

    # Extract Element from Fragment (Layout wraps the result)
    element = _get_element(result)

    # Get the main element (content area)
    main = get_by_tag_name(element, "main")

    # Verify parent link exists in main content
    all_links = query_all_by_tag_name(main, "a")
    parent_links = [link for link in all_links if link.attrs.get("href") == ".."]
    assert len(parent_links) == 1
    assert get_text_content(parent_links[0]) == "Parent"
