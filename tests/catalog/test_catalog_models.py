"""Test the Catalog model."""



from storyville.catalog.models import Catalog


def test_catalog_post_update(mock_tree_node) -> None:
    """Test Catalog.post_update method for parent assignment and naming."""
    catalog = Catalog(title="My Catalog")

    tree_node = mock_tree_node(name="root", package_location=".")

    result = catalog.post_update(parent=None, tree_node=tree_node)

    assert result is catalog
    assert catalog.name == "root"
    assert catalog.package_path == "."
    assert catalog.parent is None


def test_catalog_post_update_title_fallback(mock_tree_node) -> None:
    """Test Catalog.post_update uses package_path when title is None."""
    catalog = Catalog()  # No title provided

    tree_node = mock_tree_node(name="root", package_location="examples.minimal")

    catalog.post_update(parent=None, tree_node=tree_node)

    assert catalog.title == "examples.minimal"


def test_catalog_has_no_parent(mock_tree_node) -> None:
    """Test Catalog parent is always None (Catalog is root)."""
    catalog = Catalog(title="My Catalog")
    assert catalog.parent is None

    # Even after post_update, parent should remain None
    tree_node = mock_tree_node(name="root", package_location=".")

    catalog.post_update(parent=None, tree_node=tree_node)
    assert catalog.parent is None
