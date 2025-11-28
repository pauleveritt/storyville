"""Integration tests for copy_all_static_assets."""

from pathlib import Path

from storytime.static_assets import copy_all_static_assets


def test_copy_all_static_assets_from_both_sources(tmp_path: Path) -> None:
    """Test copy_all_static_assets discovers and copies from both sources."""
    # Create storytime static folders
    storytime_base = tmp_path / "storytime"
    st_nav_static = storytime_base / "components" / "nav" / "static"
    st_nav_static.mkdir(parents=True)
    (st_nav_static / "nav.css").write_text("nav styles")

    st_button_static = storytime_base / "components" / "button" / "static"
    st_button_static.mkdir(parents=True)
    (st_button_static / "button.css").write_text("button styles")

    # Create input_dir static folders
    input_dir = tmp_path / "input"
    input_widget_static = input_dir / "widgets" / "calendar" / "static"
    input_widget_static.mkdir(parents=True)
    (input_widget_static / "calendar.js").write_text("calendar code")

    # Copy all static assets
    output_dir = tmp_path / "output"
    output_paths = copy_all_static_assets(storytime_base, input_dir, output_dir)

    # Verify correct number of output paths returned
    assert len(output_paths) == 3

    # Verify storytime assets copied to storytime_static/
    st_nav_output = output_dir / "storytime_static" / "components" / "nav" / "static"
    assert st_nav_output.exists()
    assert (st_nav_output / "nav.css").read_text() == "nav styles"

    st_button_output = output_dir / "storytime_static" / "components" / "button" / "static"
    assert st_button_output.exists()
    assert (st_button_output / "button.css").read_text() == "button styles"

    # Verify input_dir assets copied to static/
    input_widget_output = output_dir / "static" / "widgets" / "calendar" / "static"
    assert input_widget_output.exists()
    assert (input_widget_output / "calendar.js").read_text() == "calendar code"


def test_copy_all_static_assets_handles_empty_directories(tmp_path: Path) -> None:
    """Test copy_all_static_assets handles directories with no static folders."""
    # Create empty directories
    storytime_base = tmp_path / "storytime"
    storytime_base.mkdir()

    input_dir = tmp_path / "input"
    input_dir.mkdir()

    # Copy all static assets
    output_dir = tmp_path / "output"
    output_paths = copy_all_static_assets(storytime_base, input_dir, output_dir)

    # Verify empty list returned
    assert len(output_paths) == 0


def test_copy_all_static_assets_returns_correct_output_paths(tmp_path: Path) -> None:
    """Test copy_all_static_assets returns correct output paths."""
    # Create static folders
    storytime_base = tmp_path / "storytime"
    st_static = storytime_base / "components" / "test" / "static"
    st_static.mkdir(parents=True)
    (st_static / "file.css").write_text("test")

    input_dir = tmp_path / "input"
    input_static = input_dir / "views" / "home" / "static"
    input_static.mkdir(parents=True)
    (input_static / "file.js").write_text("test")

    # Copy all static assets
    output_dir = tmp_path / "output"
    output_paths = copy_all_static_assets(storytime_base, input_dir, output_dir)

    # Verify returned paths are correct
    expected_paths = {
        output_dir / "storytime_static" / "components" / "test" / "static",
        output_dir / "static" / "views" / "home" / "static",
    }
    assert set(output_paths) == expected_paths


def test_copy_all_static_assets_preserves_subdirectories(tmp_path: Path) -> None:
    """Test copy_all_static_assets preserves subdirectory structure."""
    # Create static folder with subdirectories
    storytime_base = tmp_path / "storytime"
    st_static = storytime_base / "components" / "gallery" / "static"
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
    copy_all_static_assets(storytime_base, input_dir, output_dir)

    # Verify subdirectories preserved
    output_static = output_dir / "storytime_static" / "components" / "gallery" / "static"
    assert (output_static / "images" / "photo1.jpg").exists()
    assert (output_static / "scripts" / "app.js").exists()


def test_copy_all_static_assets_handles_nonexistent_input_dir(tmp_path: Path) -> None:
    """Test copy_all_static_assets handles nonexistent input_dir gracefully."""
    # Create only storytime_base
    storytime_base = tmp_path / "storytime"
    st_static = storytime_base / "components" / "nav" / "static"
    st_static.mkdir(parents=True)
    (st_static / "nav.css").write_text("nav styles")

    # Use nonexistent input_dir
    input_dir = tmp_path / "nonexistent"

    # Copy all static assets
    output_dir = tmp_path / "output"
    output_paths = copy_all_static_assets(storytime_base, input_dir, output_dir)

    # Verify only storytime assets copied
    assert len(output_paths) == 1
    st_nav_output = output_dir / "storytime_static" / "components" / "nav" / "static"
    assert st_nav_output.exists()
