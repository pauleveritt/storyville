"""Test the SectionView rendering."""

from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name
from tdom import Element

from storytime.section.models import Section
from storytime.section.views import SectionView
from storytime.subject import Subject


def test_section_view_renders_title_in_h1() -> None:
    """Test SectionView renders section title in h1 element."""
    section = Section(title="Components")
    view = SectionView(section=section)
    result = view()

    # Type guard in test to verify Element
    assert isinstance(result, Element)

    # Verify title is in h1
    h1 = get_by_tag_name(result, "h1")
    assert get_text_content(h1) == "Components"


def test_section_view_renders_description() -> None:
    """Test SectionView renders description when present."""
    section = Section(title="Components", description="UI component library")
    view = SectionView(section=section)
    result = view()

    # Type guard in test to verify Element
    assert isinstance(result, Element)

    # Verify description is rendered in a p element
    all_p_tags = query_all_by_tag_name(result, "p")
    description_found = any(
        "UI component library" in get_text_content(p)
        for p in all_p_tags
    )
    assert description_found


def test_section_view_renders_subject_cards() -> None:
    """Test SectionView renders subject cards as list with title and link."""
    section = Section(title="Components")
    section.package_path = ".components"

    # Add subjects to section
    subject1 = Subject(title="Button")
    subject2 = Subject(title="Input")
    section.items = {"button": subject1, "input": subject2}

    view = SectionView(section=section)
    result = view()

    # Type guard in test to verify Element
    assert isinstance(result, Element)

    # Verify ul element exists
    get_by_tag_name(result, "ul")

    # Verify subject cards are rendered as links
    all_links = query_all_by_tag_name(result, "a")
    # Filter out parent link
    subject_links = [link for link in all_links if link.attrs.get("href") != ".."]

    assert len(subject_links) == 2
    # Links can be in any order since dict iteration order may vary
    link_texts = {get_text_content(link) for link in subject_links}
    assert link_texts == {"Button", "Input"}


def test_section_view_shows_empty_state() -> None:
    """Test SectionView shows empty state message when no subjects."""
    section = Section(title="Empty Section")
    view = SectionView(section=section)
    result = view()

    # Type guard in test to verify Element
    assert isinstance(result, Element)

    # Verify empty state message
    all_p_tags = query_all_by_tag_name(result, "p")
    empty_state_found = any(
        "No subjects defined for this section" in get_text_content(p)
        for p in all_p_tags
    )
    assert empty_state_found


def test_section_view_includes_parent_link() -> None:
    """Test SectionView includes parent link."""
    section = Section(title="Components")
    view = SectionView(section=section)
    result = view()

    # Type guard in test to verify Element
    assert isinstance(result, Element)

    # Verify parent link exists
    all_links = query_all_by_tag_name(result, "a")
    parent_links = [link for link in all_links if link.attrs.get("href") == ".."]
    assert len(parent_links) == 1
    assert get_text_content(parent_links[0]) == "Parent"
