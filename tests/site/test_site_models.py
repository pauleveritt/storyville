"""Test the Site model."""


from tdom import Node, html

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


def test_site_has_no_parent(mock_tree_node) -> None:
    """Test Site parent is always None (Site is root)."""
    site = Site(title="My Site")
    assert site.parent is None

    # Even after post_update, parent should remain None
    tree_node = mock_tree_node(name="root", package_location=".")

    site.post_update(parent=None, tree_node=tree_node)
    assert site.parent is None


def test_site_themed_layout_none_default() -> None:
    """Test Site with themed_layout=None (default behavior)."""
    site = Site(title="My Site")
    assert site.themed_layout is None


def test_site_themed_layout_callable() -> None:
    """Test Site with themed_layout=callable (custom ThemedLayout)."""
    # Define a simple callable that returns a Node
    def custom_themed_layout(story_title: str | None = None, children: Node | None = None) -> Node:
        return html(t'<div>{story_title}</div>')

    site = Site(title="My Site", themed_layout=custom_themed_layout)
    assert site.themed_layout is custom_themed_layout
    assert callable(site.themed_layout)


def test_site_themed_layout_type_annotation() -> None:
    """Test Site.themed_layout accepts Callable[..., Node] | None."""
    # Test with None
    site1 = Site(title="My Site", themed_layout=None)
    assert site1.themed_layout is None

    # Test with callable
    def themed_layout_func(story_title: str | None = None, children: Node | None = None) -> Node:
        return html(t'<html><body>{children}</body></html>')

    site2 = Site(title="My Site", themed_layout=themed_layout_func)
    assert site2.themed_layout is themed_layout_func

    # Verify the callable works
    result = site2.themed_layout(story_title="Test", children=html(t'<p>Content</p>'))
    assert result is not None
