"""Tests for static folder copying utilities."""

from pathlib import Path

import pytest

from storytime.static_assets.copying import copy_static_folder
from storytime.static_assets.models import StaticFolder


def test_copy_static_folder_copies_contents(tmp_path: Path) -> None:
    """Test copy_static_folder copies all contents to output."""
    # Create source static folder with files
    source_dir = tmp_path / "source" / "components" / "nav" / "static"
    source_dir.mkdir(parents=True)
    (source_dir / "style.css").write_text("body { }")
    (source_dir / "script.js").write_text("console.log('test');")

    # Create subfolder
    assets_dir = source_dir / "assets"
    assets_dir.mkdir()
    (assets_dir / "icon.svg").write_text("<svg></svg>")

    # Create StaticFolder instance
    folder = StaticFolder(
        source_path=source_dir,
        source_type="storytime",
        relative_path=Path("components/nav"),
    )

    # Copy to output
    output_dir = tmp_path / "output"
    copy_static_folder(folder, output_dir)

    # Verify files copied
    output_static = output_dir / "storytime_static" / "components" / "nav" / "static"
    assert output_static.exists()
    assert (output_static / "style.css").exists()
    assert (output_static / "script.js").exists()
    assert (output_static / "assets" / "icon.svg").exists()

    # Verify content preserved
    assert (output_static / "style.css").read_text() == "body { }"
    assert (output_static / "script.js").read_text() == "console.log('test');"


def test_copy_static_folder_creates_parent_directories(tmp_path: Path) -> None:
    """Test copy_static_folder creates parent directories as needed."""
    # Create source static folder
    source_dir = tmp_path / "source" / "static"
    source_dir.mkdir(parents=True)
    (source_dir / "test.css").write_text("test")

    # Create StaticFolder instance
    folder = StaticFolder(
        source_path=source_dir,
        source_type="input_dir",
        relative_path=Path("deep/nested/component"),
    )

    # Copy to output (output directory doesn't exist yet)
    output_dir = tmp_path / "output"
    copy_static_folder(folder, output_dir)

    # Verify parent directories created
    output_static = output_dir / "static" / "deep" / "nested" / "component" / "static"
    assert output_static.exists()
    assert (output_static / "test.css").exists()


def test_copy_static_folder_handles_existing_directory(tmp_path: Path) -> None:
    """Test copy_static_folder handles existing directories with dirs_exist_ok=True."""
    # Create source static folder
    source_dir = tmp_path / "source" / "static"
    source_dir.mkdir(parents=True)
    (source_dir / "new.css").write_text("new content")

    # Create existing output directory with file
    output_dir = tmp_path / "output"
    output_static = output_dir / "static" / "component" / "static"
    output_static.mkdir(parents=True)
    (output_static / "old.css").write_text("old content")

    # Create StaticFolder instance
    folder = StaticFolder(
        source_path=source_dir,
        source_type="input_dir",
        relative_path=Path("component"),
    )

    # Copy to output (should merge with existing)
    copy_static_folder(folder, output_dir)

    # Verify both files exist
    assert (output_static / "new.css").exists()
    assert (output_static / "old.css").exists()
    assert (output_static / "new.css").read_text() == "new content"


def test_copy_static_folder_raises_on_nonexistent_source(tmp_path: Path) -> None:
    """Test copy_static_folder raises ValueError for nonexistent source."""
    # Create StaticFolder with nonexistent source
    folder = StaticFolder(
        source_path=Path("/nonexistent/static"),
        source_type="storytime",
        relative_path=Path("test"),
    )

    # Attempt to copy should raise ValueError
    with pytest.raises(ValueError, match="Source static folder does not exist"):
        copy_static_folder(folder, tmp_path / "output")


def test_copy_static_folder_empty_directory(tmp_path: Path) -> None:
    """Test copy_static_folder handles empty static directories."""
    # Create empty source static folder
    source_dir = tmp_path / "source" / "static"
    source_dir.mkdir(parents=True)

    # Create StaticFolder instance
    folder = StaticFolder(
        source_path=source_dir,
        source_type="storytime",
        relative_path=Path("component"),
    )

    # Copy to output
    output_dir = tmp_path / "output"
    copy_static_folder(folder, output_dir)

    # Verify directory created even if empty
    output_static = output_dir / "storytime_static" / "component" / "static"
    assert output_static.exists()
    assert output_static.is_dir()
