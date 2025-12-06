"""Integration tests for Story Assertions feature end-to-end."""

from aria_testing import get_text_content, query_all_by_tag_name
from tdom import html

from storyville.catalog.models import Catalog
from storyville.story import Story
from storyville.story.views import StoryView
from storyville.subject import Subject


def test_complete_workflow_story_with_assertions_to_badges() -> None:
    """Test complete flow: Story with assertions -> execution -> badge display."""

    def simple_component():
        return html(t"<div id='test'>Content</div>")

    def passing_assertion(element) -> None:
        """Assertion that validates the component."""
        assert element is not None

    def failing_assertion(element) -> None:
        """Assertion that fails."""
        raise AssertionError("Something is wrong")

    # Create story with assertions
    catalog = Catalog(title="Test Catalog")
    parent = Subject(title="Test Subject")
    parent.package_path = ".test"

    story = Story(
        target=simple_component,
        title="Integration Test Story",
        assertions=[passing_assertion, failing_assertion],
    )
    story.post_update(parent=parent)

    # Execute the view with assertions enabled
    view = StoryView(story=story, site=catalog, with_assertions=True)
    result = view()

    # Verify the rendered output
    element = result

    # Verify badges were rendered
    all_spans = query_all_by_tag_name(element, "span")
    badge_spans = [span for span in all_spans if "Assertion" in get_text_content(span)]

    # Should have 2 badges (one pass, one fail)
    assert len(badge_spans) == 2

    # Verify first badge is green (passing)
    badge1 = badge_spans[0]
    badge1_class = str(badge1.attrs.get("class", ""))
    assert "success" in badge1_class or "assertion-badge-pass" in badge1_class

    # Verify second badge is red (failing) with error tooltip
    badge2 = badge_spans[1]
    badge2_class = str(badge2.attrs.get("class", ""))
    assert "danger" in badge2_class or "assertion-badge-fail" in badge2_class
    badge2_title = str(badge2.attrs.get("title", ""))
    assert "Something is wrong" in badge2_title


def test_cli_flag_with_assertions_enabled() -> None:
    """Test CLI flag integration: --with-assertions enables assertion execution."""

    def simple_component():
        return html(t"<div>Test</div>")

    assertion_executed = False

    def tracking_assertion(element) -> None:
        nonlocal assertion_executed
        assertion_executed = True
        assert element is not None

    catalog = Catalog(title="Test Catalog")
    parent = Subject(title="Test")
    parent.package_path = ".test"

    story = Story(
        target=simple_component,
        assertions=[tracking_assertion],
    )
    story.post_update(parent=parent)

    # Simulate --with-assertions flag enabled (default)
    view = StoryView(story=story, site=catalog, with_assertions=True)
    result = view()

    # Verify assertion was executed
    assert assertion_executed

    # Verify badge was rendered
    element = result
    all_spans = query_all_by_tag_name(element, "span")
    badge_spans = [span for span in all_spans if "Assertion" in get_text_content(span)]
    assert len(badge_spans) == 1


def test_cli_flag_no_with_assertions_disabled() -> None:
    """Test CLI flag integration: --no-with-assertions disables assertion execution."""

    def simple_component():
        return html(t"<div>Test</div>")

    assertion_executed = False

    def tracking_assertion(element) -> None:
        nonlocal assertion_executed
        assertion_executed = True
        assert element is not None

    catalog = Catalog(title="Test Catalog")
    parent = Subject(title="Test")
    parent.package_path = ".test"

    story = Story(
        target=simple_component,
        assertions=[tracking_assertion],
    )
    story.post_update(parent=parent)

    # Simulate --no-with-assertions flag
    view = StoryView(story=story, site=catalog, with_assertions=False)
    result = view()

    # Verify assertion was NOT executed
    assert not assertion_executed

    # Verify NO badges were rendered
    element = result
    all_spans = query_all_by_tag_name(element, "span")
    badge_spans = [span for span in all_spans if "Assertion" in get_text_content(span)]
    assert len(badge_spans) == 0


def test_error_handling_does_not_crash_rendering() -> None:
    """Test that assertion failures don't crash the rendering process."""

    def simple_component():
        return html(t"<div>Test</div>")

    def critical_error_assertion(element) -> None:
        """Assertion that raises unexpected error."""
        raise RuntimeError("Unexpected critical error")

    catalog = Catalog(title="Test Catalog")
    parent = Subject(title="Test")
    parent.package_path = ".test"

    story = Story(
        target=simple_component,
        assertions=[critical_error_assertion],
    )
    story.post_update(parent=parent)

    # Execute view - should not crash despite critical error
    view = StoryView(story=story, site=catalog, with_assertions=True)
    result = view()

    # Verify rendering completed successfully
    assert result is not None
    element = result

    # Verify error badge was rendered with "Critical error:" prefix
    all_spans = query_all_by_tag_name(element, "span")
    badge_spans = [span for span in all_spans if "Assertion" in get_text_content(span)]
    assert len(badge_spans) == 1

    badge = badge_spans[0]
    badge_title = str(badge.attrs.get("title", ""))
    assert "Critical error:" in badge_title
    assert "Unexpected critical error" in badge_title


def test_multiple_assertions_in_single_story() -> None:
    """Test multiple assertions execute correctly in sequence."""

    def simple_component():
        return html(t"<div id='content'>Test Content</div>")

    execution_order = []

    def assertion1(element) -> None:
        execution_order.append(1)
        assert element is not None

    def assertion2(element) -> None:
        execution_order.append(2)
        assert element is not None

    def assertion3(element) -> None:
        execution_order.append(3)
        assert element is not None

    catalog = Catalog(title="Test Catalog")
    parent = Subject(title="Test")
    parent.package_path = ".test"

    story = Story(
        target=simple_component,
        assertions=[assertion1, assertion2, assertion3],
    )
    story.post_update(parent=parent)

    view = StoryView(story=story, site=catalog, with_assertions=True)
    result = view()

    # Verify assertions executed in order
    assert execution_order == [1, 2, 3]

    # Verify all badges rendered
    element = result
    all_spans = query_all_by_tag_name(element, "span")
    badge_spans = [span for span in all_spans if "Assertion" in get_text_content(span)]
    assert len(badge_spans) == 3


def test_mixed_pass_fail_assertions_in_single_story() -> None:
    """Test story with both passing and failing assertions."""

    def simple_component():
        return html(t"<div>Test</div>")

    def pass1(element) -> None:
        assert element is not None

    def fail1(element) -> None:
        raise AssertionError("Fail 1")

    def pass2(element) -> None:
        assert element is not None

    def fail2(element) -> None:
        raise AssertionError("Fail 2")

    catalog = Catalog(title="Test Catalog")
    parent = Subject(title="Test")
    parent.package_path = ".test"

    story = Story(
        target=simple_component,
        assertions=[pass1, fail1, pass2, fail2],
    )
    story.post_update(parent=parent)

    view = StoryView(story=story, site=catalog, with_assertions=True)
    result = view()

    # Verify all 4 badges rendered
    element = result
    all_spans = query_all_by_tag_name(element, "span")
    badge_spans = [span for span in all_spans if "Assertion" in get_text_content(span)]
    assert len(badge_spans) == 4

    # Verify correct pass/fail styling
    badge1_class = str(badge_spans[0].attrs.get("class", ""))
    assert "success" in badge1_class or "assertion-badge-pass" in badge1_class

    badge2_class = str(badge_spans[1].attrs.get("class", ""))
    assert "danger" in badge2_class or "assertion-badge-fail" in badge2_class

    badge3_class = str(badge_spans[2].attrs.get("class", ""))
    assert "success" in badge3_class or "assertion-badge-pass" in badge3_class

    badge4_class = str(badge_spans[3].attrs.get("class", ""))
    assert "danger" in badge4_class or "assertion-badge-fail" in badge4_class
