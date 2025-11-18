"""Test the Story model assertion fields."""

from tdom import Element, Fragment

from storytime.story import Story


# Story Assertions Field Tests
def test_story_assertions_defaults_to_empty_list() -> None:
    """Test Story assertions field defaults to empty list."""
    story = Story(title="Test")
    assert story.assertions == []
    assert isinstance(story.assertions, list)


def test_story_assertion_results_defaults_to_empty_list() -> None:
    """Test Story assertion_results field defaults to empty list."""
    story = Story(title="Test")
    assert story.assertion_results == []
    assert isinstance(story.assertion_results, list)


def test_story_with_populated_assertions() -> None:
    """Test Story with populated assertions list."""

    def assertion1(element: Element | Fragment) -> None:
        """Sample assertion callable."""
        assert element is not None

    def assertion2(element: Element | Fragment) -> None:
        """Another sample assertion callable."""
        assert element is not None

    story = Story(title="Test", assertions=[assertion1, assertion2])
    assert len(story.assertions) == 2
    assert story.assertions[0] is assertion1
    assert story.assertions[1] is assertion2


def test_story_with_populated_assertion_results() -> None:
    """Test Story with populated assertion_results list."""
    results = [
        ("Assertion 1", True, None),
        ("Assertion 2", False, "Expected value not found"),
    ]
    story = Story(title="Test", assertion_results=results)
    assert len(story.assertion_results) == 2
    assert story.assertion_results[0] == ("Assertion 1", True, None)
    assert story.assertion_results[1] == ("Assertion 2", False, "Expected value not found")


def test_story_assertions_accepts_lambda_callables() -> None:
    """Test Story assertions field accepts lambda functions."""
    assertion = lambda element: None  # noqa: E731
    story = Story(title="Test", assertions=[assertion])
    assert len(story.assertions) == 1
    assert callable(story.assertions[0])


def test_story_assertions_independent_between_instances() -> None:
    """Test assertions list is independent between Story instances."""
    story1 = Story(title="Story 1")
    story2 = Story(title="Story 2")

    # Modify one story's assertions
    story1.assertions.append(lambda e: None)

    # Verify other story is unaffected
    assert len(story1.assertions) == 1
    assert len(story2.assertions) == 0


def test_story_assertion_results_independent_between_instances() -> None:
    """Test assertion_results list is independent between Story instances."""
    story1 = Story(title="Story 1")
    story2 = Story(title="Story 2")

    # Modify one story's results
    story1.assertion_results.append(("Assertion 1", True, None))

    # Verify other story is unaffected
    assert len(story1.assertion_results) == 1
    assert len(story2.assertion_results) == 0
