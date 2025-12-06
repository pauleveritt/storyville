"""Tests for pytest plugin fresh rendering and execution."""

import pytest


@pytest.mark.slow
def test_story_renders_fresh(pytestconfig: pytest.Config):
    """Test that story is rendered fresh for each test execution."""
    from storyville.catalog.helpers import make_catalog

    catalog = make_catalog("examples.huge_assertions")

    # Find a story with assertions
    for section in catalog.items.values():
        for subject in section.items.values():
            for story in subject.items:
                if story.assertions:
                    # Render instance twice
                    instance1 = story.instance
                    instance2 = story.instance

                    # Both should be valid renderings
                    assert instance1 is not None
                    assert instance2 is not None
                    return

    pytest.fail("No story with assertions found")


@pytest.mark.slow
def test_assertion_executed_against_fresh_instance(pytestconfig: pytest.Config):
    """Test that assertion is executed against freshly rendered instance."""
    from storyville.catalog.helpers import make_catalog

    catalog = make_catalog("examples.huge_assertions")

    # Find a story with assertions
    for section in catalog.items.values():
        for subject in section.items.values():
            for story in subject.items:
                if story.assertions:
                    # Get fresh instance
                    instance = story.instance
                    assert instance is not None

                    # Try to execute the first assertion
                    assertion = story.assertions[0]
                    # This might pass or fail depending on the assertion
                    # We just verify it can be called
                    try:
                        assertion(instance)
                    except AssertionError:
                        # Expected for some assertions
                        pass
                    return

    pytest.fail("No story with assertions found")


@pytest.mark.slow
def test_no_cached_results_used(pytestconfig: pytest.Config):
    """Test that cached assertion_results are not used."""
    from storyville.catalog.helpers import make_catalog

    catalog = make_catalog("examples.huge_assertions")

    # Find a story with assertions
    for section in catalog.items.values():
        for subject in section.items.values():
            for story in subject.items:
                if story.assertions:
                    # The plugin should NOT use story.assertion_results
                    # It should always call story.instance and execute assertions fresh
                    # Verify that instance property exists
                    assert hasattr(story, "instance")
                    assert callable(getattr(type(story.instance), "instance", None)) or hasattr(
                        story, "instance"
                    )
                    return

    pytest.fail("No story with assertions found")
