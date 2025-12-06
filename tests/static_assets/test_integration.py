"""Integration tests for copy_all_static_assets."""

from pathlib import Path

from storyville.static_assets import copy_all_static_assets


def test_copy_all_static_assets_from_both_sources(tmp_path: Path) -> None:
    """Test copy_all_static_assets discovers and copies from both sources."""
    # Create storyville static folders
    storyville_base = tmp_path / "storyville"
    st_nav_static = storyville_base / "components" / "nav" / "static"
    st_nav_static.mkdir(parents=True)
    (st_nav_static / "nav.css").write_text("nav styles")

    st_button_static = storyville_base / "components" / "button" / "static"
    st_button_static.mkdir(parents=True)
    (st_button_static / "button.css").write_text("button styles")

    # Create input_dir static folders
    input_dir = tmp_path / "input"
    input_widget_static = input_dir / "widgets" / "calendar" / "static"
    input_widget_static.mkdir(parents=True)
    (input_widget_static / "calendar.js").write_text("calendar code")

    # Copy all static assets
    output_dir = tmp_path / "output"
    file_count = copy_all_static_assets(storyville_base, input_dir, output_dir)

    # Verify correct number of files copied
    assert file_count == 3

    # Verify all assets copied to single static/ directory with path preservation
    static_output = output_dir / "static"
    assert static_output.exists()
    assert (static_output / "components" / "nav" / "static" / "nav.css").read_text() == "nav styles"
    assert (static_output / "components" / "button" / "static" / "button.css").read_text() == "button styles"
    assert (static_output / "widgets" / "calendar" / "static" / "calendar.js").read_text() == "calendar code"


def test_copy_all_static_assets_handles_empty_directories(tmp_path: Path) -> None:
    """Test copy_all_static_assets handles directories with no static folders."""
    # Create empty directories
    storyville_base = tmp_path / "storyville"
    storyville_base.mkdir()

    input_dir = tmp_path / "input"
    input_dir.mkdir()

    # Copy all static assets
    output_dir = tmp_path / "output"
    file_count = copy_all_static_assets(storyville_base, input_dir, output_dir)

    # Verify no files copied
    assert file_count == 0


def test_copy_all_static_assets_returns_correct_file_count(tmp_path: Path) -> None:
    """Test copy_all_static_assets returns correct file count."""
    # Create static folders
    storyville_base = tmp_path / "storyville"
    st_static = storyville_base / "components" / "test" / "static"
    st_static.mkdir(parents=True)
    (st_static / "file.css").write_text("test")

    input_dir = tmp_path / "input"
    input_static = input_dir / "views" / "home" / "static"
    input_static.mkdir(parents=True)
    (input_static / "file.js").write_text("test")

    # Copy all static assets
    output_dir = tmp_path / "output"
    file_count = copy_all_static_assets(storyville_base, input_dir, output_dir)

    # Verify correct file count
    assert file_count == 2

    # Verify files are in single static/ directory with paths preserved
    static_dir = output_dir / "static"
    assert (static_dir / "components" / "test" / "static" / "file.css").exists()
    assert (static_dir / "views" / "home" / "static" / "file.js").exists()


def test_copy_all_static_assets_preserves_subdirectories(tmp_path: Path) -> None:
    """Test copy_all_static_assets preserves subdirectory structure within static folder."""
    # Create static folder with subdirectories
    storyville_base = tmp_path / "storyville"
    st_static = storyville_base / "components" / "gallery" / "static"
    st_static.mkdir(parents=True)

    # Create subdirectory structure
    images_dir = st_static / "images"
    images_dir.mkdir()
    (images_dir / "photo1.jpg").write_text("photo1")

    scripts_dir = st_static / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "app.js").write_text("app code")

    # Copy all static assets
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    output_dir = tmp_path / "output"
    file_count = copy_all_static_assets(storyville_base, input_dir, output_dir)

    # Verify files copied with full path preservation including subdirectories
    assert file_count == 2
    output_static = output_dir / "static"
    assert (output_static / "components" / "gallery" / "static" / "images" / "photo1.jpg").exists()
    assert (output_static / "components" / "gallery" / "static" / "scripts" / "app.js").exists()


def test_copy_all_static_assets_handles_nonexistent_input_dir(tmp_path: Path) -> None:
    """Test copy_all_static_assets handles nonexistent input_dir gracefully."""
    # Create only storyville_base
    storyville_base = tmp_path / "storyville"
    st_static = storyville_base / "components" / "nav" / "static"
    st_static.mkdir(parents=True)
    (st_static / "nav.css").write_text("nav styles")

    # Use nonexistent input_dir
    input_dir = tmp_path / "nonexistent"

    # Copy all static assets
    output_dir = tmp_path / "output"
    file_count = copy_all_static_assets(storyville_base, input_dir, output_dir)

    # Verify only storyville assets copied with path preservation
    assert file_count == 1
    st_nav_output = output_dir / "static"
    assert (st_nav_output / "components" / "nav" / "static" / "nav.css").exists()
