"""Test the SubjectView rendering."""

from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name
from tdom import Element, html

from storytime.story import Story
from storytime.subject import Subject
from storytime.subject.views import SubjectView


def test_subject_view_renders_title_in_h1() -> None:
    """Test SubjectView renders subject title in h1 element."""
    subject = Subject(title="Button Component")
    view = SubjectView(subject=subject)
    result = view()

    # Type guard in test to verify Element
    assert isinstance(result, Element)

    # Verify title is in h1
    h1 = get_by_tag_name(result, "h1")
    assert get_text_content(h1) == "Button Component"


def test_subject_view_renders_story_cards() -> None:
    """Test SubjectView renders story cards as simple list with title and link."""

    def button_component():
        """Button component."""
        return html(t"<button>Click me</button>")

    subject = Subject(title="Button Component", target=button_component)
    subject.package_path = ".components.button"

    # Add stories to subject
    story1 = Story(title="Primary Button", props={"variant": "primary"})
    story1.post_update(parent=subject)
    story2 = Story(title="Secondary Button", props={"variant": "secondary"})
    story2.post_update(parent=subject)

    subject.stories = [story1, story2]

    view = SubjectView(subject=subject)
    result = view()

    # Type guard in test to verify Element
    assert isinstance(result, Element)

    # Verify ul element exists
    get_by_tag_name(result, "ul")

    # Verify story cards are rendered as links
    all_links = query_all_by_tag_name(result, "a")
    # Filter out parent link
    story_links = [link for link in all_links if link.attrs.get("href") != ".."]

    assert len(story_links) == 2
    assert get_text_content(story_links[0]) == "Primary Button"
    assert get_text_content(story_links[1]) == "Secondary Button"


def test_subject_view_shows_empty_state() -> None:
    """Test SubjectView shows empty state message when no stories."""
    subject = Subject(title="Empty Component")
    view = SubjectView(subject=subject)
    result = view()

    # Type guard in test to verify Element
    assert isinstance(result, Element)

    # Verify empty state message
    all_p_tags = query_all_by_tag_name(result, "p")
    empty_state_found = any(
        "No stories defined for this component" in get_text_content(p)
        for p in all_p_tags
    )
    assert empty_state_found


def test_subject_view_returns_element_type() -> None:
    """Test SubjectView.__call__ returns an Element type."""
    subject = Subject(title="Test Component")
    view = SubjectView(subject=subject)
    result = view()

    # Type guard assertion in test
    assert isinstance(result, Element)
    assert type(result).__name__ == "Element"
