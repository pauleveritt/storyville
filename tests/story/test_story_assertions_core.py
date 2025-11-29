"""Core tests for Story Assertions execution."""

from unittest.mock import MagicMock

from tdom import Element, Fragment, Node, html

from storytime.story import Story
from storytime.story.views import StoryView


def test_assertion_execution_with_passing_assertions() -> None:
    """Test assertion execution stores results for passing assertions."""

    def sample_component() -> Node:
        """A simple component."""
        return html(t"<div>Content</div>")

    # Create assertions that pass
    assertion1_called = False
    assertion2_called = False

    def assertion1(element: Element | Fragment) -> None:
        nonlocal assertion1_called
        assertion1_called = True
        assert element is not None

    def assertion2(element: Element | Fragment) -> None:
        nonlocal assertion2_called
        assertion2_called = True
        assert isinstance(element, (Element, Fragment))

    story = Story(
        title="Test Story",
        target=sample_component,
        assertions=[assertion1, assertion2],
    )

    # Create mock site
    site = MagicMock()
    site.title = "Test Site"

    # Execute assertions by creating view and calling it with assertions enabled
    view = StoryView(story=story, site=site)
    view._execute_assertions(with_assertions=True)

    # Verify assertions were called
    assert assertion1_called
    assert assertion2_called

    # Verify results were stored
    assert len(story.assertion_results) == 2
    assert story.assertion_results[0] == ("Assertion 1", True, None)
    assert story.assertion_results[1] == ("Assertion 2", True, None)


def test_assertion_execution_with_failing_assertions() -> None:
    """Test assertion execution captures AssertionError failures."""

    def sample_component() -> Node:
        """A simple component."""
        return html(t"<div>Content</div>")

    def failing_assertion(element: Element | Fragment) -> None:
        """An assertion that always fails."""
        raise AssertionError("Expected value not found")

    story = Story(
        title="Test Story",
        target=sample_component,
        assertions=[failing_assertion],
    )

    # Create mock site
    site = MagicMock()

    # Execute assertions
    view = StoryView(story=story, site=site)
    view._execute_assertions(with_assertions=True)

    # Verify result was stored with error message
    assert len(story.assertion_results) == 1
    assert story.assertion_results[0] == (
        "Assertion 1",
        False,
        "Expected value not found",
    )


def test_assertion_execution_with_critical_errors() -> None:
    """Test assertion execution handles non-AssertionError exceptions."""

    def sample_component() -> Node:
        """A simple component."""
        return html(t"<div>Content</div>")

    def error_assertion(element: Element | Fragment) -> None:
        """An assertion that raises a critical error."""
        raise ValueError("Something went wrong")

    story = Story(
        title="Test Story",
        target=sample_component,
        assertions=[error_assertion],
    )

    # Create mock site
    site = MagicMock()

    # Execute assertions (should not crash)
    view = StoryView(story=story, site=site)
    view._execute_assertions(with_assertions=True)

    # Verify result was stored with critical error prefix
    assert len(story.assertion_results) == 1
    name, passed, error_msg = story.assertion_results[0]
    assert name == "Assertion 1"
    assert passed is False
    assert error_msg is not None
    assert error_msg.startswith("Critical error: ")
    assert "Something went wrong" in error_msg


def test_assertion_execution_position_based_naming() -> None:
    """Test assertions are named by position (for lambda compatibility)."""

    def sample_component() -> Node:
        """A simple component."""
        return html(t"<div>Content</div>")

    # Use lambdas to test position-based naming
    assertion1 = lambda e: None  # noqa: E731
    assertion2 = lambda e: None  # noqa: E731
    assertion3 = lambda e: None  # noqa: E731

    story = Story(
        title="Test Story",
        target=sample_component,
        assertions=[assertion1, assertion2, assertion3],
    )

    # Create mock site
    site = MagicMock()

    # Execute assertions
    view = StoryView(story=story, site=site)
    view._execute_assertions(with_assertions=True)

    # Verify position-based names
    assert len(story.assertion_results) == 3
    assert story.assertion_results[0][0] == "Assertion 1"
    assert story.assertion_results[1][0] == "Assertion 2"
    assert story.assertion_results[2][0] == "Assertion 3"


def test_assertion_execution_extracts_first_line_of_error() -> None:
    """Test error messages are truncated to first line only."""

    def sample_component() -> Node:
        """A simple component."""
        return html(t"<div>Content</div>")

    def multiline_error_assertion(element: Element | Fragment) -> None:
        """An assertion with multi-line error message."""
        raise AssertionError("First line\nSecond line\nThird line")

    story = Story(
        title="Test Story",
        target=sample_component,
        assertions=[multiline_error_assertion],
    )

    # Create mock site
    site = MagicMock()

    # Execute assertions
    view = StoryView(story=story, site=site)
    view._execute_assertions(with_assertions=True)

    # Verify only first line was captured
    assert len(story.assertion_results) == 1
    assert story.assertion_results[0] == ("Assertion 1", False, "First line")


def test_assertion_execution_skipped_when_disabled() -> None:
    """Test assertions are not executed when with_assertions=False."""

    def sample_component() -> Node:
        """A simple component."""
        return html(t"<div>Content</div>")

    assertion_called = False

    def assertion(element: Element | Fragment) -> None:
        nonlocal assertion_called
        assertion_called = True

    story = Story(
        title="Test Story",
        target=sample_component,
        assertions=[assertion],
    )

    # Create mock site
    site = MagicMock()

    # Execute with assertions disabled
    view = StoryView(story=story, site=site)
    view._execute_assertions(with_assertions=False)

    # Verify assertion was NOT called
    assert not assertion_called

    # Verify no results were stored
    assert len(story.assertion_results) == 0


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
