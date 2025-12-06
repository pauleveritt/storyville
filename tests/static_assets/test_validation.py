"""Tests for static asset validation utilities."""

from pathlib import Path

import pytest

from storyville.static_assets.models import StaticFolder
from storyville.static_assets.validation import validate_no_collisions


def test_validate_no_collisions_passes_with_no_conflicts() -> None:
    """Test validate_no_collisions passes when no collisions exist."""
    folders = [
        StaticFolder(
            source_path=Path("src/storyville/components/nav/static"),
            source_type="storyville",
            relative_path=Path("components/nav"),
        ),
        StaticFolder(
            source_path=Path("src/storyville/components/button/static"),
            source_type="storyville",
            relative_path=Path("components/button"),
        ),
    ]

    # Should not raise
    validate_no_collisions(folders)


def test_validate_no_collisions_passes_with_different_source_types() -> None:
    """Test validate_no_collisions passes when same path but different source types."""
    folders = [
        StaticFolder(
            source_path=Path("src/storyville/components/nav/static"),
            source_type="storyville",
            relative_path=Path("components/nav"),
        ),
        StaticFolder(
            source_path=Path("input/components/nav/static"),
            source_type="input_dir",
            relative_path=Path("components/nav"),
        ),
    ]

    # Should not raise - different prefixes (storyville_static vs static)
    validate_no_collisions(folders)


def test_validate_no_collisions_passes_with_empty_list() -> None:
    """Test validate_no_collisions handles empty list gracefully."""
    # Should not raise
    validate_no_collisions([])


def test_validate_no_collisions_passes_with_single_folder() -> None:
    """Test validate_no_collisions handles single folder gracefully."""
    folders = [
        StaticFolder(
            source_path=Path("src/storyville/components/nav/static"),
            source_type="storyville",
            relative_path=Path("components/nav"),
        )
    ]

    # Should not raise
    validate_no_collisions(folders)


def test_validate_no_collisions_detects_identical_paths() -> None:
    """Test validate_no_collisions detects collision with identical output paths."""
    # This is a hypothetical case - shouldn't happen in practice
    folders = [
        StaticFolder(
            source_path=Path("src/a/static"),
            source_type="storyville",
            relative_path=Path("components/nav"),
        ),
        StaticFolder(
            source_path=Path("src/b/static"),
            source_type="storyville",
            relative_path=Path("components/nav"),
        ),
    ]

    # Should raise ValueError with descriptive message
    with pytest.raises(ValueError, match="Static folder collision detected"):
        validate_no_collisions(folders)


def test_validate_no_collisions_error_message_includes_details() -> None:
    """Test validate_no_collisions error includes source paths and types."""
    folders = [
        StaticFolder(
            source_path=Path("src/first/static"),
            source_type="storyville",
            relative_path=Path("test"),
        ),
        StaticFolder(
            source_path=Path("src/second/static"),
            source_type="storyville",
            relative_path=Path("test"),
        ),
    ]

    # Verify error message contains useful debugging info
    with pytest.raises(ValueError) as exc_info:
        validate_no_collisions(folders)

    error_msg = str(exc_info.value)
    assert "src/first/static" in error_msg
    assert "src/second/static" in error_msg
    assert "storyville" in error_msg


def test_validate_no_collisions_handles_multiple_unique_folders() -> None:
    """Test validate_no_collisions handles many unique folders."""
    folders = [
        StaticFolder(
            source_path=Path(f"src/component{i}/static"),
            source_type="storyville" if i % 2 == 0 else "input_dir",
            relative_path=Path(f"components/component{i}"),
        )
        for i in range(10)
    ]

    # Should not raise - all unique paths
    validate_no_collisions(folders)
