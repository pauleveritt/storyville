"""Integration tests for build process with static asset handling."""

from pathlib import Path

import pytest
from storytime import PACKAGE_DIR
from storytime.build import build_site


@pytest.fixture
def tmp_build_dir(tmp_path: Path) -> Path:
    """Create a temporary directory for build tests."""
    build_dir = tmp_path / "build_output"
    build_dir.mkdir()
    return build_dir


def test_build_discovers_storytime_static_folders(tmp_build_dir: Path) -> None:
    """Test that build discovers static folders from src/storytime."""
    build_site(package_location="examples.minimal", output_dir=tmp_build_dir)

    # Verify storytime_static directory exists
    storytime_static = tmp_build_dir / "storytime_static"
    assert storytime_static.exists()

    # Verify layout static folder was discovered and copied
    layout_static = storytime_static / "components" / "layout" / "static"
    assert layout_static.exists()
    assert (layout_static / "pico-main.css").exists()


def test_build_copies_static_to_correct_output_paths(tmp_build_dir: Path) -> None:
    """Test that static assets are copied to correct disambiguated paths."""
    build_site(package_location="examples.minimal", output_dir=tmp_build_dir)

    # Storytime assets should be in storytime_static/ with full path preservation
    storytime_static = tmp_build_dir / "storytime_static" / "components" / "layout" / "static"
    assert storytime_static.exists()
    assert (storytime_static / "pico-main.css").exists()
    assert (storytime_static / "storytime.css").exists()
    assert (storytime_static / "ws.js").exists()


def test_build_preserves_directory_structure(tmp_build_dir: Path) -> None:
    """Test that directory structure is preserved in output."""
    build_site(package_location="examples.minimal", output_dir=tmp_build_dir)

    # Full path should be preserved: storytime_static/components/layout/static/
    expected_path = tmp_build_dir / "storytime_static" / "components" / "layout" / "static"
    assert expected_path.exists()

    # The "static" directory name should be preserved at the end
    assert expected_path.name == "static"
    assert expected_path.parent.name == "layout"
    assert expected_path.parent.parent.name == "components"


def test_build_without_static_dir_succeeds(tmp_build_dir: Path) -> None:
    """Test that build succeeds even if no static folders exist."""
    # This test uses examples.minimal which might not have input_dir static folders
    # The build should succeed without errors
    build_site(package_location="examples.minimal", output_dir=tmp_build_dir)

    # Verify HTML files are created
    assert (tmp_build_dir / "index.html").exists()

    # Storytime static should still exist
    assert (tmp_build_dir / "storytime_static").exists()


def test_build_clears_old_static_directories(tmp_build_dir: Path) -> None:
    """Test that old static directories are cleared before new build."""
    # Create old static directories
    old_storytime = tmp_build_dir / "storytime_static" / "old"
    old_storytime.mkdir(parents=True)
    (old_storytime / "old_file.css").write_text("old content")

    # Build the site
    build_site(package_location="examples.minimal", output_dir=tmp_build_dir)

    # Old file should be gone
    assert not (old_storytime / "old_file.css").exists()

    # New static assets should exist
    assert (tmp_build_dir / "storytime_static" / "components" / "layout" / "static").exists()


def test_build_static_phase_completes(tmp_build_dir: Path, caplog) -> None:
    """Test that static assets phase completes successfully."""
    import logging
    caplog.set_level(logging.INFO)

    build_site(package_location="examples.minimal", output_dir=tmp_build_dir)

    # Check for static assets phase log
    static_logs = [r for r in caplog.records if "Static Assets" in r.message]
    assert len(static_logs) > 0

    # Verify phase completed
    assert any("discovered and copied" in r.message for r in static_logs)


def test_build_reports_static_folder_count(tmp_build_dir: Path, caplog) -> None:
    """Test that build logs the number of static folders discovered."""
    import logging
    caplog.set_level(logging.INFO)

    build_site(package_location="examples.minimal", output_dir=tmp_build_dir)

    # Check that the log mentions number of folders
    static_logs = [r for r in caplog.records if "Phase Static Assets" in r.message]
    assert len(static_logs) > 0

    # Should mention folder count
    log_message = static_logs[0].message
    assert "folders" in log_message.lower()


def test_build_no_site_static_dir_property(tmp_build_dir: Path) -> None:
    """Test that Site model no longer has static_dir property."""
    from storytime.stories import make_site

    site = make_site(package_location="examples.minimal")

    # Verify static_dir property doesn't exist
    assert not hasattr(site, "static_dir")


def test_layout_uses_new_static_paths(tmp_build_dir: Path) -> None:
    """Test that Layout component uses new storytime_static/ paths."""
    build_site(package_location="examples.minimal", output_dir=tmp_build_dir)

    # Read the generated HTML
    index_html = (tmp_build_dir / "index.html").read_text()

    # Verify it references storytime_static/components/layout/static/
    assert "storytime_static/components/layout/static/pico-main.css" in index_html
    assert "storytime_static/components/layout/static/storytime.css" in index_html
    assert "storytime_static/components/layout/static/ws.js" in index_html

    # Should NOT reference old site-level static/
    assert 'href="../static/pico-main.css"' not in index_html
    assert 'href="../static/storytime.css"' not in index_html


@pytest.mark.parametrize(
    "page_path,expected_prefix",
    [
        ("index.html", "../storytime_static/"),
        ("components/index.html", "../storytime_static/"),
        ("components/heading/index.html", "../../storytime_static/"),
    ],
)
def test_relative_paths_correct_at_different_depths(
    tmp_build_dir: Path, page_path: str, expected_prefix: str
) -> None:
    """Test that relative paths to static assets are correct at different page depths."""
    build_site(package_location="examples.minimal", output_dir=tmp_build_dir)

    page_file = tmp_build_dir / page_path
    assert page_file.exists()

    html_content = page_file.read_text()

    # Verify the expected prefix is used
    assert f'href="{expected_prefix}components/layout/static/pico-main.css"' in html_content
