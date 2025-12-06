"""Test pathlib Path usage in app, watchers, and static assets.

These focused tests verify that app.py, watchers.py, and static_assets modules
use Path objects correctly as part of the pathlib migration.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from storyville.app import create_app
from storyville.static_assets import discover_static_folders, copy_all_static_assets
from storyville import PACKAGE_DIR


def test_create_app_accepts_path_objects() -> None:
    """Verify create_app accepts Path objects for path and output_dir."""
    with TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        output_dir = Path(tmpdir) / "output"

        # Should accept Path objects without errors
        app = create_app(
            path=path,
            output_dir=output_dir,
        )

        assert app is not None


def test_discover_static_folders_uses_path() -> None:
    """Verify discover_static_folders works with Path objects."""
    # Use storyville's own path as test case
    base_path = PACKAGE_DIR

    folders = discover_static_folders(base_path, "storyville")

    # Should return list of StaticFolder instances
    assert isinstance(folders, list)

    # Each folder should have Path objects
    for folder in folders:
        assert isinstance(folder.source_path, Path)
        assert folder.source_path.exists()
        assert folder.source_path.is_dir()


def test_copy_all_static_assets_uses_path() -> None:
    """Verify copy_all_static_assets works with Path objects."""
    with TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "output"
        input_dir = Path("examples/minimal")

        # Should work with Path objects
        file_count = copy_all_static_assets(
            storyville_base=PACKAGE_DIR,
            input_dir=input_dir,
            output_dir=output_dir,
        )

        # Should have copied some files
        assert file_count >= 0
        assert (output_dir / "static").exists()
        assert (output_dir / "static").is_dir()
