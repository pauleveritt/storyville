"""Integration tests for build process with static asset handling."""

from pathlib import Path

import pytest
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

    # Verify single static/ directory exists
    static_dir = tmp_build_dir / "static"
    assert static_dir.exists()

    # Verify layout static assets were discovered and copied with path preservation
    assert (static_dir / "components" / "layout" / "static" / "pico-main.css").exists()


def test_build_copies_static_to_correct_output_paths(tmp_build_dir: Path) -> None:
    """Test that static assets are copied to single static/ directory with path preservation."""
    build_site(package_location="examples.minimal", output_dir=tmp_build_dir)

    # All assets should be in single static/ directory with preserved paths
    static_dir = tmp_build_dir / "static"
    assert static_dir.exists()
    layout_static = static_dir / "components" / "layout" / "static"
    assert (layout_static / "pico-main.css").exists()
    assert (layout_static / "storytime.css").exists()
    assert (layout_static / "ws.js").exists()


def test_build_preserves_directory_structure(tmp_build_dir: Path) -> None:
    """Test that build preserves directory structure within static/."""
    build_site(package_location="examples.minimal", output_dir=tmp_build_dir)

    # Path structure should be preserved: static/components/layout/static/
    static_path = tmp_build_dir / "static"
    assert static_path.exists()

    # Verify the full path exists
    layout_static = static_path / "components" / "layout" / "static"
    assert layout_static.exists()
    assert (layout_static / "pico-main.css").exists()


def test_build_without_static_dir_succeeds(tmp_build_dir: Path) -> None:
    """Test that build succeeds even if no static folders exist."""
    # This test uses examples.minimal which might not have input_dir static folders
    # The build should succeed without errors
    build_site(package_location="examples.minimal", output_dir=tmp_build_dir)

    # Verify HTML files are created
    assert (tmp_build_dir / "index.html").exists()

    # Storytime static should still exist
    assert (tmp_build_dir / "static").exists()


def test_build_clears_old_static_directories(tmp_build_dir: Path) -> None:
    """Test that old static directories are cleared before new build."""
    # Create old static directory
    old_static = tmp_build_dir / "static"
    old_static.mkdir(parents=True)
    (old_static / "old_file.css").write_text("old content")

    # Build the site
    build_site(package_location="examples.minimal", output_dir=tmp_build_dir)

    # Old file should be gone
    assert not (old_static / "old_file.css").exists()

    # New static assets should exist with preserved paths
    assert (tmp_build_dir / "static").exists()
    assert (tmp_build_dir / "static" / "components" / "layout" / "static" / "pico-main.css").exists()


def test_build_static_phase_completes(tmp_build_dir: Path, caplog) -> None:
    """Test that static assets phase completes successfully."""
    import logging
    caplog.set_level(logging.INFO)

    build_site(package_location="examples.minimal", output_dir=tmp_build_dir)

    # Check for static assets phase log
    static_logs = [r for r in caplog.records if "Static Assets" in r.message]
    assert len(static_logs) > 0

    # Verify phase completed with file count
    assert any("copied" in r.message and "files" in r.message for r in static_logs)


def test_build_reports_static_file_count(tmp_build_dir: Path, caplog) -> None:
    """Test that build logs the number of static files copied."""
    import logging
    caplog.set_level(logging.INFO)

    build_site(package_location="examples.minimal", output_dir=tmp_build_dir)

    # Check that the log mentions number of files
    static_logs = [r for r in caplog.records if "Phase Static Assets" in r.message]
    assert len(static_logs) > 0

    # Should mention file count
    log_message = static_logs[0].message
    assert "files" in log_message.lower()


def test_build_no_site_static_dir_property(tmp_build_dir: Path) -> None:
    """Test that Site model no longer has static_dir property."""
    from storytime.stories import make_site

    site = make_site(package_location="examples.minimal")

    # Verify static_dir property doesn't exist
    assert not hasattr(site, "static_dir")


def test_layout_uses_new_static_paths(tmp_build_dir: Path) -> None:
    """Test that Layout component uses new single static/ paths."""
    build_site(package_location="examples.minimal", output_dir=tmp_build_dir)

    # Read the generated HTML
    index_html = (tmp_build_dir / "index.html").read_text()

    # Verify it references static assets with full nested path (no ../ prefix for root pages)
    assert "static/components/layout/static/pico-main.css" in index_html
    assert "static/components/layout/static/storytime.css" in index_html
    assert "static/components/layout/static/ws.js" in index_html


@pytest.mark.parametrize(
    "page_path,expected_prefix",
    [
        ("index.html", "static/components/layout/static/"),  # Root level: 0 dirs deep
        ("components/index.html", "../static/components/layout/static/"),  # 1 dir deep
        ("components/heading/index.html", "../../static/components/layout/static/"),  # 2 dirs deep
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

    # Verify the expected prefix is used with full nested path
    assert f'href="{expected_prefix}pico-main.css"' in html_content
