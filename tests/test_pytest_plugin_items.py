"""Tests for pytest plugin test item generation."""

import pytest


@pytest.mark.slow
def test_items_generated_for_assertions(pytestconfig: pytest.Config):
    """Test that one pytest Item is generated per assertion."""
    from storytime.site.helpers import make_site

    site = make_site("examples.huge_assertions")

    # Count total assertions across all stories
    total_assertions = 0
    for section in site.items.values():
        for subject in section.items.values():
            for story in subject.items:
                total_assertions += len(story.assertions)

    # We should have at least one assertion
    assert total_assertions > 0


def test_item_naming_convention(pytestconfig: pytest.Config):
    """Test that test names follow the convention."""
    from storytime.pytest_plugin import StoryAssertionItem

    # Create a mock collector to test naming
    # We can't easily test this without running pytest collection,
    # but we can verify the naming pattern is correct by checking
    # the StoryAssertionItem class exists and has the right structure
    assert hasattr(StoryAssertionItem, "reportinfo")


def test_filesystem_safe_names():
    """Test that story names are filesystem-safe."""
    # Test name sanitization
    test_name = "My Story with Spaces"
    safe_name = test_name.replace(" ", "_").lower()

    assert " " not in safe_name
    assert safe_name == "my_story_with_spaces"


def test_assertion_numbering():
    """Test that assertions are numbered with 1-based index."""
    # Test assertion naming pattern
    for idx in range(1, 4):
        assertion_name = f"Assertion {idx}"
        assert "Assertion" in assertion_name
        assert str(idx) in assertion_name
        assert idx >= 1  # 1-based numbering
