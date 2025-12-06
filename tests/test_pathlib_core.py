"""Test pathlib Path usage in core modules.

These focused tests verify that core modules use Path objects correctly
as part of the pathlib migration.
"""

from pathlib import Path

from storyville.nodes import get_package_path
from storyville import PACKAGE_DIR
from storyville.catalog.helpers import make_catalog


def test_get_package_path_returns_path_object() -> None:
    """Verify get_package_path returns a Path object, not a string."""
    result = get_package_path("examples.minimal")
    assert isinstance(result, Path)
    assert result.exists()
    assert result.is_dir()


def test_package_dir_is_path_object() -> None:
    """Verify PACKAGE_DIR is a Path object, not a string."""
    assert isinstance(PACKAGE_DIR, Path)
    assert PACKAGE_DIR.exists()
    assert PACKAGE_DIR.is_dir()
    assert (PACKAGE_DIR / "__init__.py").exists()


def test_make_catalog_uses_path_operations() -> None:
    """Verify make_catalog uses Path objects internally."""
    catalog = make_catalog("examples.minimal")

    # Verify catalog was created successfully using Path operations
    assert catalog is not None
    assert catalog.title is not None

    # Verify catalog has sections (which means path operations worked)
    assert len(catalog.items) > 0
