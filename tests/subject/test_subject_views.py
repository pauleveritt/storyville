"""Test the SubjectView rendering."""

from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name
from tdom import html

from storyville.story import Story
from storyville.subject import Subject
from storyville.subject.views import SubjectView
from storyville.catalog.models import Catalog

def test_subject_view_renders_title_in_h1() -> None:
    """Test SubjectView renders subject title in h1 element."""
    catalog = Catalog(title="My Catalog")
    subject = Subject(title="Button Component")
    view = SubjectView(subject=subject, site=catalog)
    result = view()

    # Extract  from  (Layout wraps the result)
    element = result

    # Verify title is in h1
    h1 = get_by_tag_name(element, "h1")
    assert get_text_content(h1) == "Button Component"

def test_subject_view_renders_story_cards() -> None:
    """Test SubjectView renders story cards as simple list with title and link."""

    def button_component():
        """Button component."""
        return html(t"<button>Click me</button>")

    catalog = Catalog(title="My Catalog")
    subject = Subject(title="Button Component", target=button_component)
    subject.package_path = ".components.button"

    # Add stories to subject
    story1 = Story(title="Primary Button", props={"variant": "primary"})
    story1.post_update(parent=subject)
    story2 = Story(title="Secondary Button", props={"variant": "secondary"})
    story2.post_update(parent=subject)

    subject.items = [story1, story2]

    view = SubjectView(subject=subject, site=catalog)
    result = view()

    # Extract  from  (Layout wraps the result)
    element = result

    # Get the main element (content area) to avoid sidebar sections listing
    main = get_by_tag_name(element, "main")

    # Verify story cards are rendered as links (no parent link anymore)
    all_links = query_all_by_tag_name(main, "a")

    # Should have 2 story links (parent link has been removed and replaced by breadcrumbs)
    assert len(all_links) == 2
    assert get_text_content(all_links[0]) == "Primary Button"
    assert get_text_content(all_links[1]) == "Secondary Button"

def test_subject_view_shows_empty_state() -> None:
    """Test SubjectView shows empty state message when no stories."""
    catalog = Catalog(title="My Catalog")
    subject = Subject(title="Empty Component")
    view = SubjectView(subject=subject, site=catalog)
    result = view()

    # Extract  from  (Layout wraps the result)
    element = result

    # Verify empty state message
    all_p_tags = query_all_by_tag_name(element, "p")
    empty_state_found = any(
        "No stories defined for this component" in get_text_content(p)
        for p in all_p_tags
    )
    assert empty_state_found

def test_subject_view_returns_element_type() -> None:
    """Test SubjectView.__call__ returns an  or  type."""
    catalog = Catalog(title="My Catalog")
    subject = Subject(title="Test Component")
    view = SubjectView(subject=subject, site=catalog)
    result = view()

    # Verify result is a valid Node (could be Element or Fragment from Layout)
    assert result is not None
    # Verify it contains an html element (from Layout wrapper)
    html_elem = get_by_tag_name(result, "html")
    assert html_elem is not None
