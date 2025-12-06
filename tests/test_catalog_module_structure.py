"""Tests for catalog module structure and imports.

This test module verifies that the catalog package is correctly structured
and that the core classes are available through the public API.
"""


def test_catalog_module_exists():
    """Verify that the storyville.catalog module exists and is importable."""
    import storyville.catalog

    assert storyville.catalog is not None


def test_catalog_class_importable():
    """Verify that Catalog class is available from storyville.catalog."""
    from storyville.catalog import Catalog

    assert Catalog is not None
    assert hasattr(Catalog, "__name__")
    assert Catalog.__name__ == "Catalog"


def test_catalog_exported_from_main_package():
    """Verify that Catalog is exported from the main storyville package."""
    from storyville import Catalog

    assert Catalog is not None
    assert hasattr(Catalog, "__name__")
    assert Catalog.__name__ == "Catalog"


def test_catalog_view_importable():
    """Verify that CatalogView is available from storyville.catalog.views."""
    from storyville.catalog.views import CatalogView

    assert CatalogView is not None
    assert hasattr(CatalogView, "__name__")
    assert CatalogView.__name__ == "CatalogView"
