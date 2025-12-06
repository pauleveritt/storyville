"""Tests for StoryView description rendering."""

from dataclasses import dataclass

from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name
from tdom import Node, html

from storyville.section.models import Section
from storyville.catalog.models import Catalog
from storyville.story.models import Story
from storyville.story.views import StoryView
from storyville.subject.models import Subject


@dataclass
class SimpleComponent:
    """A simple test component."""

    name: str = "test"

    def __call__(self) -> Node:
        """Render the component."""
        return html(t"<div>{self.name}</div>")


def test_story_view_description_renders_mode_b() -> None:
    """Test that story description renders in Mode B above Props line."""
    catalog = Catalog(title="Test Catalog")
    section = Section(title="Components", parent=catalog)
    subject = Subject(title="Button", parent=section, target=SimpleComponent)
    story = Story(
        title="Primary Button",
        description="A primary button with emphasis",
        props={"name": "primary"},
        parent=subject,
    )

    view = StoryView(story=story, site=catalog, with_assertions=False)
    result = view()

    # Verify result is not None
    assert result is not None

    # Get the main element (content area) to avoid layout elements
    main = get_by_tag_name(result, "main")

    # Find all paragraph elements within main
    paragraphs = query_all_by_tag_name(main, "p")

    # Should have description + Props paragraph
    assert len(paragraphs) >= 2

    # First paragraph should be the description
    description_p = paragraphs[0]
    assert get_text_content(description_p) == "A primary button with emphasis"

    # Second paragraph should be Props line
    props_p = paragraphs[1]
    props_text = get_text_content(props_p)
    assert "Props:" in props_text


def test_story_view_description_renders_mode_c() -> None:
    """Test that story description renders in Mode C above Props line."""

    def custom_themed_layout(
        story_title: str | None = None, children: Node | None = None
    ) -> Node:
        """Custom themed layout for testing Mode C."""
        return html(t"<html><body>{children}</body></html>")

    catalog = Catalog(title="Test Catalog", themed_layout=custom_themed_layout)
    section = Section(title="Components", parent=catalog)
    subject = Subject(title="Button", parent=section, target=SimpleComponent)
    story = Story(
        title="Primary Button",
        description="A primary button with themed layout",
        props={"name": "themed"},
        parent=subject,
    )

    view = StoryView(story=story, site=catalog, with_assertions=False)
    result = view()

    # Verify result is not None
    assert result is not None

    # Get the main element (content area) to avoid layout elements
    main = get_by_tag_name(result, "main")

    # Find all paragraph elements within main
    paragraphs = query_all_by_tag_name(main, "p")

    # Should have description + Props paragraph
    assert len(paragraphs) >= 2

    # First paragraph should be the description
    description_p = paragraphs[0]
    assert get_text_content(description_p) == "A primary button with themed layout"

    # Second paragraph should be Props line
    props_p = paragraphs[1]
    props_text = get_text_content(props_p)
    assert "Props:" in props_text


def test_story_view_description_not_rendered_mode_a() -> None:
    """Test that story description is NOT rendered in Mode A (Custom Template)."""

    def custom_template() -> Node:
        """Custom template for the story."""
        return html(t"<div>Custom Template Content</div>")

    catalog = Catalog(title="Test Catalog")
    section = Section(title="Components", parent=catalog)
    subject = Subject(title="Button", parent=section)
    story = Story(
        title="Custom Story",
        description="This should not be rendered",
        template=custom_template,
        parent=subject,
    )

    view = StoryView(story=story, site=catalog, with_assertions=False)
    result = view()

    # Verify result is not None
    assert result is not None

    # Find all divs
    divs = query_all_by_tag_name(result, "div")
    # Should contain the custom template content
    found_custom = False
    for div in divs:
        text = get_text_content(div)
        if "Custom Template Content" in text:
            found_custom = True
            break
    assert found_custom

    # Description should NOT be present anywhere
    all_text = get_text_content(result)
    assert "This should not be rendered" not in all_text


def test_story_view_description_skipped_when_none_mode_b() -> None:
    """Test that description is not rendered when None in Mode B."""
    catalog = Catalog(title="Test Catalog")
    section = Section(title="Components", parent=catalog)
    subject = Subject(title="Button", parent=section, target=SimpleComponent)
    story = Story(
        title="Button Story",
        description=None,
        props={"name": "test"},
        parent=subject,
    )

    view = StoryView(story=story, site=catalog, with_assertions=False)
    result = view()

    # Verify result is not None
    assert result is not None

    # Get the main element (content area) to avoid layout elements
    main = get_by_tag_name(result, "main")

    # Find all paragraph elements within main
    paragraphs = query_all_by_tag_name(main, "p")

    # Should only have Props paragraph (description skipped)
    assert len(paragraphs) == 1

    # First paragraph should be Props line
    props_p = paragraphs[0]
    props_text = get_text_content(props_p)
    assert "Props:" in props_text


def test_story_view_description_html_escaped_mode_b() -> None:
    """Test that dangerous HTML characters are automatically escaped in Mode B."""
    catalog = Catalog(title="Test Catalog")
    section = Section(title="Components", parent=catalog)
    subject = Subject(title="Button", parent=section, target=SimpleComponent)
    story = Story(
        title="Button Story",
        description="<script>alert('xss')</script>Safe text",
        props={"name": "test"},
        parent=subject,
    )

    view = StoryView(story=story, site=catalog, with_assertions=False)
    result = view()

    # Verify result is not None
    assert result is not None

    # Get the main element (content area) to avoid layout elements
    main = get_by_tag_name(result, "main")

    # Find all paragraph elements within main
    paragraphs = query_all_by_tag_name(main, "p")

    # First paragraph should be the description
    description_p = paragraphs[0]
    description_text = get_text_content(description_p)

    # Text content should contain the literal script tags (escaped)
    assert "<script>alert('xss')</script>Safe text" in description_text
