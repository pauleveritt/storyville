"""Tests for pytest plugin discovery and collection."""

import pytest


def test_collect_discovers_story_files(pytestconfig: pytest.Config):
    """Test that pytest_collect_file discovers stories.py files."""
    # This is an integration test - when we run pytest it should discover
    # stories.py files in the examples/ directory
    # We verify this by checking that the plugin is loaded
    assert pytestconfig.pluginmanager.has_plugin("storyville")


def test_discovery_respects_enabled_setting(pytestconfig: pytest.Config):
    """Test that discovery respects the enabled setting."""
    enabled: bool = pytestconfig.getini("storyville_enabled")

    # Verify the enabled setting can be read
    assert isinstance(enabled, bool)
    # Plugin should be enabled by default
    assert enabled is True


@pytest.mark.slow
def test_collect_builds_story_tree(pytestconfig: pytest.Config):
    """Test that make_catalog() builds story tree correctly."""
    from storyville.catalog.helpers import make_catalog

    # Build the site for the examples.huge_assertions package
    catalog = make_catalog("examples.huge_assertions")

    # Verify site structure
    assert catalog is not None
    assert catalog.title == "Huge Scale Example"
    assert len(catalog.items) > 0


@pytest.mark.slow
def test_traversal_finds_stories_with_assertions(pytestconfig: pytest.Config):
    """Test that traversal finds stories with non-empty assertions."""
    from storyville.catalog.helpers import make_catalog

    # Build the site
    catalog = make_catalog("examples.huge_assertions")

    # Find stories with assertions by traversing the tree
    stories_with_assertions = []
    for section_name, section in catalog.items.items():
        for subject_name, subject in section.items.items():
            for story in subject.items:
                if story.assertions:
                    stories_with_assertions.append(story)

    # Should find at least one story with assertions
    assert len(stories_with_assertions) > 0


@pytest.mark.slow
def test_story_has_assertions_field(pytestconfig: pytest.Config):
    """Test that stories have the assertions field."""
    from storyville.catalog.helpers import make_catalog

    catalog = make_catalog("examples.huge_assertions")

    # Find a story with assertions
    for section in catalog.items.values():
        for subject in section.items.values():
            for story in subject.items:
                if story.assertions:
                    # Verify assertions is a list
                    assert isinstance(story.assertions, list)
                    assert len(story.assertions) > 0
                    return

    pytest.fail("No story with assertions found")
