"""Test the SubjectView rendering."""

from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name
from tdom import Element, Fragment, Node, html
from typing import cast

from storytime.story import Story
from storytime.subject import Subject
from storytime.subject.views import SubjectView
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


def test_subject_view_renders_title_in_h1() -> None:
    """Test SubjectView renders subject title in h1 element."""
    site = Site(title="My Site")
    subject = Subject(title="Button Component")
    view = SubjectView(subject=subject, site=site)
    result = view()

    # Extract Element from Fragment (Layout wraps the result)
    element = _get_element(result)

    # Verify title is in h1
    h1 = get_by_tag_name(element, "h1")
    assert get_text_content(h1) == "Button Component"


def test_subject_view_renders_story_cards() -> None:
    """Test SubjectView renders story cards as simple list with title and link."""

    def button_component():
        """Button component."""
        return html(t"<button>Click me</button>")

    site = Site(title="My Site")
    subject = Subject(title="Button Component", target=button_component)
    subject.package_path = ".components.button"

    # Add stories to subject
    story1 = Story(title="Primary Button", props={"variant": "primary"})
    story1.post_update(parent=subject)
    story2 = Story(title="Secondary Button", props={"variant": "secondary"})
    story2.post_update(parent=subject)

    subject.items = [story1, story2]

    view = SubjectView(subject=subject, site=site)
    result = view()

    # Extract Element from Fragment (Layout wraps the result)
    element = _get_element(result)

    # Get the main element (content area) to avoid sidebar sections listing
    main = get_by_tag_name(element, "main")

    # Verify story cards are rendered as links
    # Get the article element which contains the actual content (not sidebar)
    article = get_by_tag_name(main, "article")
    all_links = query_all_by_tag_name(article, "a")

    # Should have 2 story links + 1 parent link = 3 total
    assert len(all_links) == 3
    # Filter out parent link
    story_links = [link for link in all_links if link.attrs.get("href") != ".."]

    assert len(story_links) == 2
    assert get_text_content(story_links[0]) == "Primary Button"
    assert get_text_content(story_links[1]) == "Secondary Button"


def test_subject_view_shows_empty_state() -> None:
    """Test SubjectView shows empty state message when no stories."""
    site = Site(title="My Site")
    subject = Subject(title="Empty Component")
    view = SubjectView(subject=subject, site=site)
    result = view()

    # Extract Element from Fragment (Layout wraps the result)
    element = _get_element(result)

    # Verify empty state message
    all_p_tags = query_all_by_tag_name(element, "p")
    empty_state_found = any(
        "No stories defined for this component" in get_text_content(p)
        for p in all_p_tags
    )
    assert empty_state_found


def test_subject_view_returns_element_type() -> None:
    """Test SubjectView.__call__ returns an Element or Fragment type."""
    site = Site(title="My Site")
    subject = Subject(title="Test Component")
    view = SubjectView(subject=subject, site=site)
    result = view()

    # Type guard assertion in test - now accepts Fragment too (from Layout)
    assert isinstance(result, (Element, Fragment))
