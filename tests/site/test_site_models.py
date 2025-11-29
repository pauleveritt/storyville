"""Test the Site model."""



from storytime.site.models import Site


def test_site_post_update(mock_tree_node) -> None:
    """Test Site.post_update method for parent assignment and naming."""
    site = Site(title="My Site")

    tree_node = mock_tree_node(name="root", package_location=".")

    result = site.post_update(parent=None, tree_node=tree_node)

    assert result is site
    assert site.name == "root"
    assert site.package_path == "."
    assert site.parent is None


def test_site_post_update_title_fallback(mock_tree_node) -> None:
    """Test Site.post_update uses package_path when title is None."""
    site = Site()  # No title provided

    tree_node = mock_tree_node(name="root", package_location="examples.minimal")

    site.post_update(parent=None, tree_node=tree_node)

    assert site.title == "examples.minimal"


def test_site_has_no_parent(mock_tree_node) -> None:
    """Test Site parent is always None (Site is root)."""
    site = Site(title="My Site")
    assert site.parent is None

    # Even after post_update, parent should remain None
    tree_node = mock_tree_node(name="root", package_location=".")

    site.post_update(parent=None, tree_node=tree_node)
    assert site.parent is None
