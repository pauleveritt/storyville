"""Edge case tests for Story Assertions feature."""

from unittest.mock import MagicMock

from tdom import Element, Fragment, Node, html

from storytime.story import Story
from storytime.story.views import StoryView


def test_assertion_with_empty_error_message() -> None:
    """Test assertion that raises AssertionError with empty message."""

    def simple_component() -> Node:
        return html(t"<div>Test</div>")

    def empty_message_assertion(element: Element | Fragment) -> None:
        """Assertion with empty error message."""
        raise AssertionError("")

    story = Story(
        title="Test Story",
        target=simple_component,
        assertions=[empty_message_assertion],
    )

    site = MagicMock()
    view = StoryView(story=story, site=site)
    view._execute_assertions(with_assertions=True)

    # Verify result was stored with empty error message
    assert len(story.assertion_results) == 1
    name, passed, error_msg = story.assertion_results[0]
    assert name == "Assertion 1"
    assert passed is False
    assert error_msg == ""  # Empty string, not None


def test_story_instance_returns_none() -> None:
    """Test assertion execution when story.instance returns None."""

    def none_component() -> None:
        """Component that returns None."""
        return None

    def sample_assertion(element: Element | Fragment) -> None:
        """Assertion that should not be called."""
        raise AssertionError("Should not execute")

    story = Story(
        title="Test Story",
        target=none_component,
        assertions=[sample_assertion],
    )

    site = MagicMock()
    view = StoryView(story=story, site=site)

    # Execute assertions - should skip when instance is None
    view._execute_assertions(with_assertions=True)

    # Verify no results were stored (assertions skipped)
    assert len(story.assertion_results) == 0


def test_assertion_that_returns_non_none_value() -> None:
    """Test that assertions returning non-None values still pass."""

    def simple_component() -> Node:
        return html(t"<div>Test</div>")

    def returning_assertion(element: Element | Fragment) -> int:
        """Assertion that returns a value instead of None."""
        # In pytest, assertions can return values - they still pass if no exception
        return 42

    story = Story(
        title="Test Story",
        target=simple_component,
        assertions=[returning_assertion],  # type: ignore
    )

    site = MagicMock()
    view = StoryView(story=story, site=site)
    view._execute_assertions(with_assertions=True)

    # Verify assertion passed (no exception raised)
    assert len(story.assertion_results) == 1
    assert story.assertion_results[0] == ("Assertion 1", True, None)


def test_multiple_consecutive_critical_errors() -> None:
    """Test handling of multiple critical errors in sequence."""

    def simple_component() -> Node:
        return html(t"<div>Test</div>")

    def critical_error_1(element: Element | Fragment) -> None:
        """First critical error."""
        raise ValueError("Critical 1")

    def critical_error_2(element: Element | Fragment) -> None:
        """Second critical error."""
        raise TypeError("Critical 2")

    def critical_error_3(element: Element | Fragment) -> None:
        """Third critical error."""
        raise RuntimeError("Critical 3")

    story = Story(
        title="Test Story",
        target=simple_component,
        assertions=[critical_error_1, critical_error_2, critical_error_3],
    )

    site = MagicMock()
    view = StoryView(story=story, site=site)
    view._execute_assertions(with_assertions=True)

    # Verify all three errors were captured
    assert len(story.assertion_results) == 3

    # Verify each has "Critical error:" prefix
    for i, (name, passed, error_msg) in enumerate(story.assertion_results, start=1):
        assert name == f"Assertion {i}"
        assert passed is False
        assert error_msg is not None
        assert error_msg.startswith("Critical error: ")
        assert f"Critical {i}" in error_msg


def test_mixed_assertion_error_and_critical_error_messages() -> None:
    """Test that AssertionError and critical errors are distinguished."""

    def simple_component() -> Node:
        return html(t"<div>Test</div>")

    def normal_assertion_error(element: Element | Fragment) -> None:
        """Normal assertion error."""
        raise AssertionError("Normal assertion failure")

    def critical_error(element: Element | Fragment) -> None:
        """Critical error."""
        raise ValueError("Unexpected error")

    story = Story(
        title="Test Story",
        target=simple_component,
        assertions=[normal_assertion_error, critical_error],
    )

    site = MagicMock()
    view = StoryView(story=story, site=site)
    view._execute_assertions(with_assertions=True)

    # Verify results
    assert len(story.assertion_results) == 2

    # First: normal AssertionError (no prefix)
    name1, passed1, error_msg1 = story.assertion_results[0]
    assert name1 == "Assertion 1"
    assert passed1 is False
    assert error_msg1 == "Normal assertion failure"
    assert not error_msg1.startswith("Critical error: ")

    # Second: critical error (with prefix)
    name2, passed2, error_msg2 = story.assertion_results[1]
    assert name2 == "Assertion 2"
    assert passed2 is False
    assert error_msg2 is not None
    assert error_msg2.startswith("Critical error: ")
    assert "Unexpected error" in error_msg2
