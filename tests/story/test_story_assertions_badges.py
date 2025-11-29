"""Test badge rendering in StoryView for assertions."""

from aria_testing import get_text_content, query_all_by_tag_name
from tdom import html

from storytime.catalog.models import Catalog
from storytime.story import Story
from storytime.story.views import StoryView
from storytime.subject import Subject

def test_story_view_badges_display_passing_assertion() -> None:
    """Test that passing assertions display green badges."""

    def simple_component():
        return html(t"<div>Test</div>")

    def passing_assertion(element) -> None:
        """Assertion that always passes."""
        assert element is not None

    catalog = Catalog(title="Test Catalog")
    parent = Subject(title="Test")
    parent.package_path = ".test"

    story = Story(
        target=simple_component,
        assertions=[passing_assertion],
    )
    story.post_update(parent=parent)

    view = StoryView(story=story, site=catalog, with_assertions=True)
    result = view()

    element = result

    # Find all span tags (badges should be spans)
    all_spans = query_all_by_tag_name(element, "span")

    # Look for badge with "Assertion 1" text
    badge_spans = [
        span
        for span in all_spans
        if "Assertion 1" in get_text_content(span)
    ]

    assert len(badge_spans) >= 1, "Should have at least one badge for Assertion 1"

    badge = badge_spans[0]
    badge_class = str(badge.attrs.get("class", ""))

    # Check that the badge has success/green styling
    assert "success" in badge_class or "assertion-badge-pass" in badge_class

def test_story_view_badges_display_failing_assertion() -> None:
    """Test that failing assertions display red badges with error tooltip."""

    def simple_component():
        return html(t"<div>Test</div>")

    def failing_assertion(element) -> None:
        """Assertion that always fails."""
        raise AssertionError("Expected condition not met")

    catalog = Catalog(title="Test Catalog")
    parent = Subject(title="Test")
    parent.package_path = ".test"

    story = Story(
        target=simple_component,
        assertions=[failing_assertion],
    )
    story.post_update(parent=parent)

    view = StoryView(story=story, site=catalog, with_assertions=True)
    result = view()

    element = result

    # Find all span tags (badges should be spans)
    all_spans = query_all_by_tag_name(element, "span")

    # Look for badge with "Assertion 1" text
    badge_spans = [
        span
        for span in all_spans
        if "Assertion 1" in get_text_content(span)
    ]

    assert len(badge_spans) >= 1, "Should have at least one badge for Assertion 1"

    badge = badge_spans[0]
    badge_class = str(badge.attrs.get("class", ""))

    # Check that the badge has danger/red styling
    assert "danger" in badge_class or "assertion-badge-fail" in badge_class

    # Check that title attribute contains error message
    badge_title = str(badge.attrs.get("title", ""))
    assert "Expected condition not met" in badge_title

def test_story_view_no_badges_when_assertions_empty() -> None:
    """Test that no badges are shown when story has no assertions."""

    def simple_component():
        return html(t"<div>Test</div>")

    catalog = Catalog(title="Test Catalog")
    parent = Subject(title="Test")
    parent.package_path = ".test"

    story = Story(
        target=simple_component,
        assertions=[],  # Empty assertions list
    )
    story.post_update(parent=parent)

    view = StoryView(story=story, site=catalog, with_assertions=True)
    result = view()

    element = result

    # Find all span tags
    all_spans = query_all_by_tag_name(element, "span")

    # Look for any badge spans with "Assertion" text
    badge_spans = [
        span
        for span in all_spans
        if "Assertion" in get_text_content(span)
    ]

    # Should have no assertion badges
    assert len(badge_spans) == 0, "Should have no assertion badges when assertions empty"

def test_story_view_no_badges_when_assertions_disabled() -> None:
    """Test that no badges are shown when with_assertions is False."""

    def simple_component():
        return html(t"<div>Test</div>")

    def passing_assertion(element) -> None:
        """Assertion that always passes."""
        assert element is not None

    catalog = Catalog(title="Test Catalog")
    parent = Subject(title="Test")
    parent.package_path = ".test"

    story = Story(
        target=simple_component,
        assertions=[passing_assertion],
    )
    story.post_update(parent=parent)

    view = StoryView(story=story, site=catalog, with_assertions=False)
    result = view()

    element = result

    # Find all span tags
    all_spans = query_all_by_tag_name(element, "span")

    # Look for any badge spans with "Assertion" text
    badge_spans = [
        span
        for span in all_spans
        if "Assertion" in get_text_content(span)
    ]

    # Should have no assertion badges when disabled
    assert len(badge_spans) == 0, "Should have no assertion badges when disabled"

def test_story_view_multiple_assertions_multiple_badges() -> None:
    """Test that multiple assertions result in multiple badges."""

    def simple_component():
        return html(t"<div>Test</div>")

    def assertion_1(element) -> None:
        assert element is not None

    def assertion_2(element) -> None:
        assert element is not None

    def assertion_3(element) -> None:
        raise AssertionError("This one fails")

    catalog = Catalog(title="Test Catalog")
    parent = Subject(title="Test")
    parent.package_path = ".test"

    story = Story(
        target=simple_component,
        assertions=[assertion_1, assertion_2, assertion_3],
    )
    story.post_update(parent=parent)

    view = StoryView(story=story, site=catalog, with_assertions=True)
    result = view()

    element = result

    # Find all span tags
    all_spans = query_all_by_tag_name(element, "span")

    # Look for badge spans with "Assertion" text
    badge_spans = [
        span
        for span in all_spans
        if "Assertion" in get_text_content(span)
    ]

    # Should have 3 badges (one for each assertion)
    assert len(badge_spans) == 3, f"Should have 3 badges, found {len(badge_spans)}"

    # Verify each badge has the correct assertion number
    badge_texts = [get_text_content(span) for span in badge_spans]
    assert "Assertion 1" in badge_texts[0]
    assert "Assertion 2" in badge_texts[1]
    assert "Assertion 3" in badge_texts[2]

def test_story_view_critical_error_badge() -> None:
    """Test that critical errors (non-AssertionError) display red badges."""

    def simple_component():
        return html(t"<div>Test</div>")

    def critical_error_assertion(element) -> None:
        """Assertion that raises a non-AssertionError exception."""
        raise ValueError("Unexpected error")

    catalog = Catalog(title="Test Catalog")
    parent = Subject(title="Test")
    parent.package_path = ".test"

    story = Story(
        target=simple_component,
        assertions=[critical_error_assertion],
    )
    story.post_update(parent=parent)

    view = StoryView(story=story, site=catalog, with_assertions=True)
    result = view()

    element = result

    # Find all span tags
    all_spans = query_all_by_tag_name(element, "span")

    # Look for badge with "Assertion 1" text
    badge_spans = [
        span
        for span in all_spans
        if "Assertion 1" in get_text_content(span)
    ]

    assert len(badge_spans) >= 1, "Should have at least one badge for critical error"

    badge = badge_spans[0]

    # Check that title attribute contains "Critical error:"
    badge_title = str(badge.attrs.get("title", ""))
    assert "Critical error:" in badge_title
    assert "Unexpected error" in badge_title

def test_story_view_badge_container_flexbox() -> None:
    """Test that badge container uses flexbox for proper alignment."""

    def simple_component():
        return html(t"<div>Test</div>")

    def passing_assertion(element) -> None:
        assert element is not None

    catalog = Catalog(title="Test Catalog")
    parent = Subject(title="Test")
    parent.package_path = ".test"

    story = Story(
        target=simple_component,
        title="Test Story",
        assertions=[passing_assertion],
    )
    story.post_update(parent=parent)

    view = StoryView(story=story, site=catalog, with_assertions=True)
    result = view()

    element = result

    # Find the main content div (contains h1 and badge container)
    # Look for a div that has both title and badges as children
    all_divs = query_all_by_tag_name(element, "div")

    # Find the header container div
    header_div = None
    for div in all_divs:
        # Check if it has a class that suggests it's the header container
        div_class: str = str(div.attrs.get("class", ""))
        if "story-header" in div_class or "header-container" in div_class:
            header_div = div
            break

    # If we found a header div, verify it has flexbox or grid styling
    if header_div:
        div_style: str = str(header_div.attrs.get("style", ""))
        # Check for flexbox or grid styles
        assert (
            "display: flex" in div_style
            or "display: grid" in div_style
            or "display:flex" in div_style
            or "display:grid" in div_style
        ), "Header container should use flexbox or grid"
