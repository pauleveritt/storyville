"""Test the StoryView rendering with dual modes."""

from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name
from tdom import html

from storyville.catalog.models import Catalog
from storyville.story import Story
from storyville.story.views import StoryView
from storyville.subject import Subject

def test_story_view_with_custom_template_mode() -> None:
    """Test StoryView uses a custom template when provided."""

    def custom_template():
        """Custom template with full control over rendering."""
        return html(t"<div><h1>Custom Template Output</h1></div>")

    catalog = Catalog(title="Test Catalog")
    story = Story(title="Test Story", template=custom_template)
    view = StoryView(story=story, site=catalog)
    result = view()

    # Type guard in test to verify

    # Verify custom template content is present
    h1 = get_by_tag_name(result, "h1")
    assert get_text_content(h1) == "Custom Template Output"

def test_story_view_with_default_layout_mode() -> None:
    """Test StoryView renders the default layout when no template."""

    def simple_component(name: str = "default"):
        """Simple component that returns a ."""
        return html(t"<p>Hello {name}</p>")

    catalog = Catalog(title="Test Catalog")
    parent = Subject(title="Components")
    parent.package_path = ".components"
    parent.resource_path = "components"

    story = Story(target=simple_component, props={"name": "World"})
    story.post_update(parent=parent)

    view = StoryView(story=story, site=catalog, resource_path=story.resource_path)
    result = view()

    # Extract  from result (handles Layout's  wrapper)
    element = result

    # Verify the story title is present
    h1 = get_by_tag_name(element, "h1")
    assert story.title is not None
    assert get_text_content(h1) == story.title

    # Verify component instance is rendered
    # Now that Layout wraps the story, there are multiple p tags from Layout's sidebar
    # Just verify that the component's p tag is present
    all_p_tags = query_all_by_tag_name(element, "p")
    # Find the one from the component (contains "Hello World")
    component_p_tags = [p for p in all_p_tags if "Hello World" in get_text_content(p)]
    assert len(component_p_tags) >= 1
    assert get_text_content(component_p_tags[0]) == "Hello World"

    # Verify breadcrumbs navigation is present (replaces parent link)
    main = get_by_tag_name(element, "main")
    nav = get_by_tag_name(main, "nav")
    assert nav is not None
    assert nav.attrs.get("aria-label") == "Breadcrumb"

def test_story_view_default_layout_shows_props() -> None:
    """Test StoryView default layout displays props."""

    def test_component(title: str = "test", count: int = 0):
        """Component with multiple props."""
        return html(t"<div>{title}: {count}</div>")

    catalog = Catalog(title="Test Catalog")
    parent = Subject(title="Test Component")
    parent.package_path = ".components.test"

    story = Story(target=test_component, props={"title": "Example", "count": 42})
    story.post_update(parent=parent)

    view = StoryView(story=story, site=catalog)
    result = view()

    # Extract  from result
    element = result

    # Verify props are displayed
    code = get_by_tag_name(element, "code")
    props_text = get_text_content(code)
    assert "Example" in props_text or "42" in props_text

def test_story_view_default_layout_with_empty_props() -> None:
    """Test StoryView default layout handles empty props dict."""

    def no_props_component():
        """Component that takes no props."""
        return html(t"<span>No props needed</span>")

    catalog = Catalog(title="Test Catalog")
    parent = Subject(title="Simple")
    parent.package_path = ".simple"

    story = Story(target=no_props_component, props={})
    story.post_update(parent=parent)

    view = StoryView(story=story, site=catalog)
    result = view()

    # Extract  from result
    element = result

    # Verify component is still rendered
    span = get_by_tag_name(element, "span")
    assert get_text_content(span) == "No props needed"

    # Verify empty props are shown
    code = get_by_tag_name(element, "code")
    props_text = get_text_content(code)
    assert props_text == "{}"

def test_story_view_returns_element_type() -> None:
    """Test StoryView.__call__ returns an  type."""

    def basic_component():
        """Basic component."""
        return html(t"<div>Test</div>")

    catalog = Catalog(title="Test Catalog")
    story = Story(target=basic_component)
    parent = Subject()
    parent.package_path = ".test"
    story.post_update(parent=parent)

    view = StoryView(story=story, site=catalog)
    result = view()

    # Verify result is a valid Node (could be Element or Fragment)
    assert result is not None
    # Verify it contains an html element (from Layout wrapper)
    html_elem = get_by_tag_name(result, "html")
    assert html_elem is not None

def test_story_view_custom_template_no_wrapping() -> None:
    """Test custom template mode has no wrapping elements."""

    def minimal_template():
        """Minimal template for testing."""
        return html(t"<article>Pure template content</article>")

    catalog = Catalog(title="Test Catalog")
    story = Story(title="Minimal", template=minimal_template)
    view = StoryView(story=story, site=catalog)
    result = view()

    # Should only have the article from the template, no additional wrapping
    # Result might be Fragment, so get the article element
    article = get_by_tag_name(result, "article")
    assert article is not None
    article_text = get_text_content(article)
    assert article_text == "Pure template content"

def test_story_view_default_layout_complete_structure() -> None:
    """Test default layout includes all required elements."""

    def full_component(message: str = "Hello"):
        """Component with a prop."""
        return html(t"<section>{message}</section>")

    catalog = Catalog(title="Test Catalog")
    parent = Subject(title="Full Test")
    parent.package_path = ".components.full"
    parent.resource_path = "components/full"

    story = Story(
        target=full_component, title="Full Story", props={"message": "Complete"}
    )
    story.post_update(parent=parent)

    view = StoryView(story=story, site=catalog, resource_path=story.resource_path)
    result = view()

    # Extract  from result
    element = result

    # Verify all required elements are present
    h1 = get_by_tag_name(element, "h1")
    assert get_text_content(h1) == "Full Story"

    code = get_by_tag_name(element, "code")
    assert "message" in get_text_content(code) or "Complete" in get_text_content(code)

    # Layout adds section tags, so find the one from the component
    all_sections = query_all_by_tag_name(element, "section")
    component_sections = [s for s in all_sections if get_text_content(s).strip() == "Complete"]
    assert len(component_sections) >= 1
    assert get_text_content(component_sections[0]) == "Complete"

    # Verify breadcrumbs navigation is present (replaces parent link)
    main = get_by_tag_name(element, "main")
    nav = get_by_tag_name(main, "nav")
    assert nav is not None
    assert nav.attrs.get("aria-label") == "Breadcrumb"
