"""Tests for change detection and classification system."""

from pathlib import Path

import pytest

from storyville.watchers import ChangeType, classify_change


def test_classify_global_asset_themed_story_html() -> None:
    """Test classification of themed_story.html as a global asset."""
    # File path to themed_story.html in any story directory
    changed_path = Path("/output/components/heading/story-0/themed_story.html")

    change_type, story_id = classify_change(changed_path)

    assert change_type == ChangeType.GLOBAL_ASSET
    assert story_id is None


def test_classify_global_asset_css_in_static() -> None:
    """Test classification of CSS files in static directories as global assets."""
    # CSS file in static directory
    changed_path = Path("/output/static/bundle.css")

    change_type, story_id = classify_change(changed_path)

    assert change_type == ChangeType.GLOBAL_ASSET
    assert story_id is None


def test_classify_global_asset_js_in_static() -> None:
    """Test classification of JS files in static directories as global assets."""
    # JS file in static directory
    changed_path = Path("/output/static/ws.mjs")

    change_type, story_id = classify_change(changed_path)

    assert change_type == ChangeType.GLOBAL_ASSET
    assert story_id is None


def test_classify_story_specific_index_html() -> None:
    """Test classification of individual story index.html as story-specific."""
    # Individual story index.html
    changed_path = Path("/output/components/heading/story-0/index.html")

    change_type, story_id = classify_change(changed_path)

    assert change_type == ChangeType.STORY_SPECIFIC
    assert story_id == "components/heading/story-0"


def test_classify_story_specific_nested_path() -> None:
    """Test classification of story index.html with deeper nesting."""
    # Story with deeper nesting
    changed_path = Path("/output/ui/buttons/primary/story-1/index.html")

    change_type, story_id = classify_change(changed_path)

    assert change_type == ChangeType.STORY_SPECIFIC
    assert story_id == "ui/buttons/primary/story-1"


def test_classify_non_story_documentation() -> None:
    """Test classification of documentation pages as non-story."""
    # Documentation page
    changed_path = Path("/output/docs/getting-started.html")

    change_type, story_id = classify_change(changed_path)

    assert change_type == ChangeType.NON_STORY
    assert story_id is None


def test_classify_non_story_section_index() -> None:
    """Test classification of section index pages as non-story."""
    # Section index page
    changed_path = Path("/output/components/index.html")

    change_type, story_id = classify_change(changed_path)

    assert change_type == ChangeType.NON_STORY
    assert story_id is None


def test_classify_non_story_catalog_index() -> None:
    """Test classification of catalog index as non-story."""
    # Catalog index
    changed_path = Path("/output/index.html")

    change_type, story_id = classify_change(changed_path)

    assert change_type == ChangeType.NON_STORY
    assert story_id is None


def test_story_id_extraction_from_various_paths() -> None:
    """Test story ID extraction from various file path formats."""
    test_cases = [
        # (file_path, expected_story_id)
        (
            Path("/output/components/heading/story-0/index.html"),
            "components/heading/story-0",
        ),
        (
            Path("/output/ui/buttons/story-2/index.html"),
            "ui/buttons/story-2",
        ),
        (
            Path("/output/forms/inputs/text/story-10/index.html"),
            "forms/inputs/text/story-10",
        ),
    ]

    for file_path, expected_story_id in test_cases:
        change_type, story_id = classify_change(file_path)
        assert change_type == ChangeType.STORY_SPECIFIC
        assert story_id == expected_story_id


@pytest.mark.parametrize(
    "file_path,expected_type",
    [
        (Path("/output/themed_story.html"), ChangeType.GLOBAL_ASSET),
        (Path("/output/static/main.css"), ChangeType.GLOBAL_ASSET),
        (Path("/output/static/app.js"), ChangeType.GLOBAL_ASSET),
        (
            Path("/output/components/story-0/index.html"),
            ChangeType.STORY_SPECIFIC,
        ),
        (Path("/output/docs/guide.html"), ChangeType.NON_STORY),
        (Path("/output/components/index.html"), ChangeType.NON_STORY),
    ],
)
def test_classify_change_parametrized(
    file_path: Path, expected_type: ChangeType
) -> None:
    """Parametrized test for various change classifications."""
    change_type, _ = classify_change(file_path)
    assert change_type == expected_type
