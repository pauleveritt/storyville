"""Tests for catalog module structure and imports.

This test module verifies that the catalog package is correctly structured
and that the core classes are available through the public API.
"""


def test_catalog_module_exists():
    """Verify that the storytime.catalog module exists and is importable."""
    import storytime.catalog

    assert storytime.catalog is not None


def test_catalog_class_importable():
    """Verify that Catalog class is available from storytime.catalog."""
    from storytime.catalog import Catalog

    assert Catalog is not None
    assert hasattr(Catalog, "__name__")
    assert Catalog.__name__ == "Catalog"


def test_catalog_exported_from_main_package():
    """Verify that Catalog is exported from the main storytime package."""
    from storytime import Catalog

    assert Catalog is not None
    assert hasattr(Catalog, "__name__")
    assert Catalog.__name__ == "Catalog"


def test_catalog_view_importable():
    """Verify that CatalogView is available from storytime.catalog.views."""
    from storytime.catalog.views import CatalogView

    assert CatalogView is not None
    assert hasattr(CatalogView, "__name__")
    assert CatalogView.__name__ == "CatalogView"
