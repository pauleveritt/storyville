"""Test assertion execution in StoryView."""

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


def test_assertion_execution_skipped_when_assertions_empty() -> None:
    """Test assertion execution is skipped when story has no assertions."""

    def sample_component() -> Node:
        """A simple component."""
        return html(t"<div>Content</div>")

    story = Story(
        title="Test Story",
        target=sample_component,
        assertions=[],  # Empty list
    )

    # Create mock site
    site = MagicMock()

    # Execute assertions (should be skipped)
    view = StoryView(story=story, site=site)
    view._execute_assertions(with_assertions=True)

    # Verify no results were stored
    assert len(story.assertion_results) == 0
