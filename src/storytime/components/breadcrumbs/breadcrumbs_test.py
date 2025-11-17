"""Test the Breadcrumbs component."""

from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name
from tdom import Element, Fragment, Node

from storytime.components.breadcrumbs import Breadcrumbs


def _get_element(result: Node) -> Element | None:
    """Extract Element from result (handles Fragment wrapper).

    Returns None if result is empty Fragment or empty content.
    """
    if isinstance(result, Fragment):
        # Fragment may contain empty children for empty breadcrumbs
        for child in result.children:
            if isinstance(child, Element):
                return child
        return None
    # Type guard - we know result is an Element if not Fragment
    if not isinstance(result, Element):
        return None
    return result


def test_breadcrumbs_renders_nothing_when_path_is_none() -> None:
    """Test Breadcrumbs renders nothing when current_path is None."""
    breadcrumbs = Breadcrumbs(current_path=None)
    result = breadcrumbs()

    # Extract Element from Fragment
    element = _get_element(result)

    # Should render nothing (no nav element)
    assert element is None


def test_breadcrumbs_renders_nothing_when_path_is_empty() -> None:
    """Test Breadcrumbs renders nothing when current_path is empty string."""
    breadcrumbs = Breadcrumbs(current_path="")
    result = breadcrumbs()

    # Extract Element from Fragment
    element = _get_element(result)

    # Should render nothing (no nav element)
    assert element is None


def test_breadcrumbs_renders_home_and_section_for_section_path() -> None:
    """Test Breadcrumbs renders Home link and section name for section-level path."""
    breadcrumbs = Breadcrumbs(current_path="getting-started")
    result = breadcrumbs()

    # Extract Element from Fragment
    element = _get_element(result)
    assert element is not None

    # Verify nav element with aria-label
    nav = get_by_tag_name(element, "nav")
    assert nav.attrs.get("aria-label") == "Breadcrumb"

    # Get all links
    all_links = query_all_by_tag_name(nav, "a")
    assert len(all_links) == 1

    # Home should be a link
    home_link = all_links[0]
    assert home_link.attrs.get("href") == "/"
    assert get_text_content(home_link) == "Home"

    # Section should be plain text (current page)
    all_text = get_text_content(nav)
    assert "getting-started" in all_text
    assert " > " in all_text  # Separator between items


def test_breadcrumbs_renders_separator_between_items() -> None:
    """Test Breadcrumbs uses ' > ' as separator between items."""
    breadcrumbs = Breadcrumbs(current_path="getting-started/installation")
    result = breadcrumbs()

    # Extract Element from Fragment
    element = _get_element(result)
    assert element is not None

    # Get full text content
    nav = get_by_tag_name(element, "nav")
    text_content = get_text_content(nav)

    # Verify separator appears between items
    # Should have: "Home > getting-started > installation"
    assert " > " in text_content
    # Count separators (should be 2)
    separator_count = text_content.count(" > ")
    assert separator_count == 2


def test_breadcrumbs_renders_all_ancestors_as_links() -> None:
    """Test Breadcrumbs renders all ancestor levels as clickable links."""
    breadcrumbs = Breadcrumbs(current_path="getting-started/installation/quick-start")
    result = breadcrumbs()

    # Extract Element from Fragment
    element = _get_element(result)
    assert element is not None

    nav = get_by_tag_name(element, "nav")
    all_links = query_all_by_tag_name(nav, "a")

    # Should have 3 links: Home, section, subject
    assert len(all_links) == 3

    # Home link
    home_link = all_links[0]
    assert home_link.attrs.get("href") == "/"
    assert get_text_content(home_link) == "Home"

    # Section link
    section_link = all_links[1]
    assert section_link.attrs.get("href") == "/section/getting-started"
    assert get_text_content(section_link) == "getting-started"

    # Subject link
    subject_link = all_links[2]
    assert subject_link.attrs.get("href") == "/section/getting-started/subject/installation"
    assert get_text_content(subject_link) == "installation"


def test_breadcrumbs_current_page_not_clickable() -> None:
    """Test Breadcrumbs renders current page as plain text (not a link)."""
    breadcrumbs = Breadcrumbs(current_path="getting-started/installation/quick-start")
    result = breadcrumbs()

    # Extract Element from Fragment
    element = _get_element(result)
    assert element is not None

    nav = get_by_tag_name(element, "nav")

    # Get all links (should NOT include the story)
    all_links = query_all_by_tag_name(nav, "a")
    link_texts = {get_text_content(link) for link in all_links}

    # Story name should NOT be in link texts (it's the current page)
    assert "quick-start" not in link_texts

    # But it should be in the overall text content
    text_content = get_text_content(nav)
    assert "quick-start" in text_content


def test_breadcrumbs_subject_level_path() -> None:
    """Test Breadcrumbs renders correctly for subject-level path."""
    breadcrumbs = Breadcrumbs(current_path="components/button")
    result = breadcrumbs()

    # Extract Element from Fragment
    element = _get_element(result)
    assert element is not None

    nav = get_by_tag_name(element, "nav")
    all_links = query_all_by_tag_name(nav, "a")

    # Should have 2 links: Home and section
    assert len(all_links) == 2

    # Home link
    assert all_links[0].attrs.get("href") == "/"

    # Section link
    assert all_links[1].attrs.get("href") == "/section/components"

    # Subject should be plain text (current page)
    text_content = get_text_content(nav)
    assert "button" in text_content

    # Verify "button" is not a link
    link_texts = {get_text_content(link) for link in all_links}
    assert "button" not in link_texts
