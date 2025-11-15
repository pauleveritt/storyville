"""Test the StoryView rendering with dual modes."""

from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name
from tdom import Element, html

from storytime.story import Story
from storytime.story.views import StoryView
from storytime.subject import Subject


def test_story_view_with_custom_template_mode() -> None:
    """Test StoryView uses a custom template when provided."""

    def custom_template():
        """Custom template with full control over rendering."""
        return html(t"<div><h1>Custom Template Output</h1></div>")

    story = Story(title="Test Story", template=custom_template)
    view = StoryView(story=story)
    result = view()

    # Type guard in test to verify Element
    assert isinstance(result, Element)

    # Verify custom template content is present
    h1 = get_by_tag_name(result, "h1")
    assert get_text_content(h1) == "Custom Template Output"


def test_story_view_with_default_layout_mode() -> None:
    """Test StoryView renders the default layout when no template."""

    def simple_component(name: str = "default"):
        """Simple component that returns a Node."""
        return html(t"<p>Hello {name}</p>")

    parent = Subject(title="Components")
    parent.package_path = ".components"

    story = Story(target=simple_component, props={"name": "World"})
    story.post_update(parent=parent)

    view = StoryView(story=story)
    result = view()

    # Type guard in test to verify Element
    assert isinstance(result, Element)

    # Verify the story title is present
    h1 = get_by_tag_name(result, "h1")
    assert story.title is not None
    assert get_text_content(h1) == story.title

    # Verify component instance is rendered - there are multiple p tags
    all_p_tags = query_all_by_tag_name(result, "p")
    # One p tag for Props display, one from a component
    assert len(all_p_tags) == 2
    # Find the one from the component (contains "Hello World")
    component_p = [p for p in all_p_tags if "Hello World" in get_text_content(p)][0]
    assert get_text_content(component_p) == "Hello World"

    # Verify parent link is present
    a = get_by_tag_name(result, "a")
    assert a.attrs.get("href") == ".."


def test_story_view_default_layout_shows_props() -> None:
    """Test StoryView default layout displays props."""

    def test_component(title: str = "test", count: int = 0):
        """Component with multiple props."""
        return html(t"<div>{title}: {count}</div>")

    parent = Subject(title="Test Component")
    parent.package_path = ".components.test"

    story = Story(target=test_component, props={"title": "Example", "count": 42})
    story.post_update(parent=parent)

    view = StoryView(story=story)
    result = view()

    # Type guard in test to verify Element
    assert isinstance(result, Element)

    # Verify props are displayed
    code = get_by_tag_name(result, "code")
    props_text = get_text_content(code)
    assert "Example" in props_text or "42" in props_text


def test_story_view_default_layout_with_empty_props() -> None:
    """Test StoryView default layout handles empty props dict."""

    def no_props_component():
        """Component that takes no props."""
        return html(t"<span>No props needed</span>")

    parent = Subject(title="Simple")
    parent.package_path = ".simple"

    story = Story(target=no_props_component, props={})
    story.post_update(parent=parent)

    view = StoryView(story=story)
    result = view()

    # Type guard in test to verify Element
    assert isinstance(result, Element)

    # Verify component is still rendered
    span = get_by_tag_name(result, "span")
    assert get_text_content(span) == "No props needed"

    # Verify empty props are shown
    code = get_by_tag_name(result, "code")
    props_text = get_text_content(code)
    assert props_text == "{}"


def test_story_view_returns_element_type() -> None:
    """Test StoryView.__call__ returns an Element type."""

    def basic_component():
        """Basic component."""
        return html(t"<div>Test</div>")

    story = Story(target=basic_component)
    parent = Subject()
    parent.package_path = ".test"
    story.post_update(parent=parent)

    view = StoryView(story=story)
    result = view()

    # Type guard assertion in a test
    assert isinstance(result, Element)
    assert type(result).__name__ == "Element"


def test_story_view_custom_template_no_wrapping() -> None:
    """Test custom template mode has no wrapping elements."""

    def minimal_template():
        """Minimal template for testing."""
        return html(t"<article>Pure template content</article>")

    story = Story(title="Minimal", template=minimal_template)
    view = StoryView(story=story)
    result = view()

    # Type guard in test
    assert isinstance(result, Element)

    # Should only have the article from the template, no additional wrapping
    assert result.tag == "article"
    article_text = get_text_content(result)
    assert article_text == "Pure template content"


def test_story_view_default_layout_complete_structure() -> None:
    """Test default layout includes all required elements."""

    def full_component(message: str = "Hello"):
        """Component with a prop."""
        return html(t"<section>{message}</section>")

    parent = Subject(title="Full Test")
    parent.package_path = ".components.full"

    story = Story(
        target=full_component, title="Full Story", props={"message": "Complete"}
    )
    story.post_update(parent=parent)

    view = StoryView(story=story)
    result = view()

    # Type guard in test
    assert isinstance(result, Element)

    # Verify all required elements are present
    h1 = get_by_tag_name(result, "h1")
    assert get_text_content(h1) == "Full Story"

    code = get_by_tag_name(result, "code")
    assert "message" in get_text_content(code) or "Complete" in get_text_content(code)

    section = get_by_tag_name(result, "section")
    assert get_text_content(section) == "Complete"

    a = get_by_tag_name(result, "a")
    assert a.attrs.get("href") == ".."
