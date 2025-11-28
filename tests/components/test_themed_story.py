"""Test the ThemedStory component."""

from aria_testing import get_by_tag_name, get_text_content
from tdom import Node, html

from storytime.components.themed_story import ThemedStory
from storytime.site.models import Site


def test_themed_story_renders_with_custom_themed_layout() -> None:
    """Test ThemedStory renders with custom ThemedLayout callable."""
    # Define a custom themed layout function
    def custom_themed_layout(story_title: str | None = None, children: Node | None = None) -> Node:
        # Pre-compute the title to avoid tdom interpolation issues
        title = f"{story_title} - Custom Theme" if story_title else "Custom Theme"
        return html(t'''\
<!DOCTYPE html>
<html lang="EN">
<head>
    <title>{title}</title>
</head>
<body>
    <div class="custom-wrapper">{children}</div>
</body>
</html>
''')

    # Create site with custom themed_layout
    site = Site(title="My Site", themed_layout=custom_themed_layout)

    # Create ThemedStory with test content
    story_content = html(t'<p>Story content here</p>')
    themed_story = ThemedStory(
        story_title="Test Story",
        children=story_content,
        site=site
    )

    # Render and verify
    result = themed_story()
    element = result

    # Verify it uses custom themed layout
    title_elem = get_by_tag_name(element, "title")
    assert get_text_content(title_elem) == "Test Story - Custom Theme"

    # Verify custom wrapper is present
    body = get_by_tag_name(element, "body")
    div = get_by_tag_name(body, "div")
    class_attr = div.attrs.get("class", "")
    assert "custom-wrapper" in class_attr if class_attr else False


def test_themed_story_falls_back_to_layout_when_themed_layout_none() -> None:
    """Test ThemedStory falls back to Layout when themed_layout=None."""
    # Create site without themed_layout
    site = Site(title="My Site")
    assert site.themed_layout is None

    # Create ThemedStory with test content
    story_content = html(t'<p>Story content here</p>')
    themed_story = ThemedStory(
        story_title="Test Story",
        children=story_content,
        site=site
    )

    # Render and verify
    result = themed_story()
    element = result

    # Verify it uses standard Layout (will have site title in page title)
    title_elem = get_by_tag_name(element, "title")
    title_text = get_text_content(title_elem)
    assert "My Site" in title_text


def test_themed_story_passes_story_title_correctly() -> None:
    """Test ThemedStory passes story_title prop correctly."""
    # Define a themed layout function that uses story_title
    def title_themed_layout(story_title: str | None = None, children: Node | None = None) -> Node:
        # Pre-compute the title
        title = f"Title: {story_title}" if story_title else "Title: None"
        return html(t'''\
<!DOCTYPE html>
<html lang="EN">
<head>
    <title>{title}</title>
</head>
<body>{children}</body>
</html>
''')

    site = Site(title="My Site", themed_layout=title_themed_layout)
    story_content = html(t'<div>Content</div>')
    themed_story = ThemedStory(
        story_title="Amazing Story",
        children=story_content,
        site=site
    )

    result = themed_story()
    element = result

    title_elem = get_by_tag_name(element, "title")
    assert get_text_content(title_elem) == "Title: Amazing Story"


def test_themed_story_passes_children_correctly() -> None:
    """Test ThemedStory passes children prop correctly."""
    # Define a themed layout function that wraps children
    def wrapper_themed_layout(story_title: str | None = None, children: Node | None = None) -> Node:
        return html(t'''\
<!DOCTYPE html>
<html lang="EN">
<head>
    <title>Test</title>
</head>
<body>
    <div id="wrapper">{children}</div>
</body>
</html>
''')

    site = Site(title="My Site", themed_layout=wrapper_themed_layout)
    story_content = html(t'<p id="unique-content">My unique story content</p>')
    themed_story = ThemedStory(
        story_title="Test",
        children=story_content,
        site=site
    )

    result = themed_story()
    element = result

    # Verify children content is present
    body = get_by_tag_name(element, "body")
    wrapper = get_by_tag_name(body, "div")
    p = get_by_tag_name(wrapper, "p")
    assert get_text_content(p) == "My unique story content"


def test_themed_story_returns_full_html_structure() -> None:
    """Test ThemedStory returns full HTML structure (DOCTYPE, html, head, body)."""
    site = Site(title="My Site")
    story_content = html(t'<p>Content</p>')
    themed_story = ThemedStory(
        story_title="Test Story",
        children=story_content,
        site=site
    )

    result = themed_story()
    element = result

    # Verify full HTML structure (result might be Fragment with DOCTYPE + html)
    html_elem = get_by_tag_name(element, "html")
    assert html_elem is not None

    # Verify has head and body
    head = get_by_tag_name(html_elem, "head")
    assert head is not None

    body = get_by_tag_name(html_elem, "body")
    assert body is not None

    # Verify DOCTYPE is in result (check string representation)
    html_string = str(result)
    assert "<!DOCTYPE html>" in html_string
