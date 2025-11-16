"""Test the Site model."""

from pathlib import Path

from storytime.section import Section
from storytime.site.models import Site


def test_site_initialization() -> None:
    """Test Site can be instantiated with BaseNode inheritance."""
    site = Site(title="My Site")
    assert site.title == "My Site"
    assert site.parent is None
    assert site.items == {}
    assert site.name == ""


def test_site_items_field() -> None:
    """Test Site.items dict field holds Sections."""
    section1 = Section(title="Components")
    section2 = Section(title="Patterns")
    site = Site(
        title="My Site",
        items={"components": section1, "patterns": section2}
    )

    assert len(site.items) == 2
    assert site.items["components"] is section1
    assert site.items["patterns"] is section2


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


def test_site_static_dir_detection(tmp_path: Path) -> None:
    """Test Site.__post_init__ detects static directory."""
    import storytime

    # Save original PACKAGE_DIR
    original_package_dir = storytime.PACKAGE_DIR

    # Create a temporary static directory at new location
    static_dir = tmp_path / "components" / "layout" / "static"
    static_dir.mkdir(parents=True)

    # Temporarily set PACKAGE_DIR to tmp_path
    storytime.PACKAGE_DIR = tmp_path

    try:
        site = Site(title="My Site")
        assert site.static_dir == static_dir
    finally:
        # Restore original PACKAGE_DIR
        storytime.PACKAGE_DIR = original_package_dir


def test_site_no_static_dir(tmp_path: Path) -> None:
    """Test Site.__post_init__ when static directory doesn't exist."""
    import storytime

    # Save original PACKAGE_DIR
    original_package_dir = storytime.PACKAGE_DIR

    # Temporarily set PACKAGE_DIR to tmp_path (without creating static/)
    storytime.PACKAGE_DIR = tmp_path

    try:
        site = Site(title="My Site")
        assert site.static_dir is None
    finally:
        # Restore original PACKAGE_DIR
        storytime.PACKAGE_DIR = original_package_dir


def test_site_has_no_parent(mock_tree_node) -> None:
    """Test Site parent is always None (Site is root)."""
    site = Site(title="My Site")
    assert site.parent is None

    # Even after post_update, parent should remain None
    tree_node = mock_tree_node(name="root", package_location=".")

    site.post_update(parent=None, tree_node=tree_node)
    assert site.parent is None
