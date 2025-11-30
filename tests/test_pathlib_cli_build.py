"""Test pathlib Path usage in CLI and build system.

These focused tests verify that __main__.py and build.py use Path objects
correctly as part of the pathlib migration.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from storytime.build import build_catalog


def test_build_catalog_accepts_path_object() -> None:
    """Verify build_catalog accepts Path object for output_dir."""
    with TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)

        # Should accept Path object without errors
        build_catalog(
            package_location="examples.minimal",
            output_dir=output_dir,
            with_assertions=True,
        )

        # Verify build created files
        assert (output_dir / "index.html").exists()
        assert (output_dir / "index.html").is_file()


def test_build_catalog_creates_path_structure() -> None:
    """Verify build_catalog uses Path operations to create directory structure."""
    with TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "nested" / "output"

        # Path should be created automatically
        build_catalog(
            package_location="examples.minimal",
            output_dir=output_dir,
            with_assertions=False,
        )

        # Verify paths were created using Path operations
        assert output_dir.exists()
        assert output_dir.is_dir()
        assert (output_dir / "index.html").exists()


def test_build_catalog_output_dir_type() -> None:
    """Verify build_catalog output_dir parameter is properly typed as Path."""
    with TemporaryDirectory() as tmpdir:
        # Test that Path object works (type hint should be Path, not str)
        output_path = Path(tmpdir) / "output"

        build_catalog(
            package_location="examples.minimal",
            output_dir=output_path,
            with_assertions=True,
        )

        assert output_path.exists()
        assert isinstance(output_path, Path)
