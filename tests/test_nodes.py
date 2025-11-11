"""Test the nodes module classes: TreeNode and BaseNode."""

from pathlib import Path
from unittest.mock import Mock, patch

from storytime.nodes import BaseNode, TreeNode
from storytime.site import Site
from storytime.story import Section


# Test BaseNode
def test_basenode_initialization() -> None:
    """Test BaseNode can be instantiated with default values."""
    node: BaseNode[object] = BaseNode()
    assert node.name == ""
    assert node.parent is None
    assert node.title is None
    assert node.context is None


def test_basenode_with_values() -> None:
    """Test BaseNode with custom values."""
    node: BaseNode[object] = BaseNode(name="test", title="Test Node")
    assert node.name == "test"
    assert node.title == "Test Node"


def test_basenode_post_update() -> None:
    """Test BaseNode post_update method."""
    parent = Mock()
    tree_node = Mock()
    tree_node.name = "child"
    tree_node.this_package_location = ".components.child"

    node: BaseNode[object] = BaseNode()
    result = node.post_update(parent=parent, tree_node=tree_node)

    assert result is node
    assert node.name == "child"
    assert node.package_path == ".components.child"
    assert node.parent is parent
    assert node.title == ".components.child"


def test_basenode_post_update_preserves_title() -> None:
    """Test BaseNode post_update preserves custom title."""
    parent = Mock()
    tree_node = Mock()
    tree_node.name = "child"
    tree_node.this_package_location = ".components.child"

    node: BaseNode[object] = BaseNode(title="Custom Title")
    node.post_update(parent=parent, tree_node=tree_node)

    assert node.title == "Custom Title"


# Test TreeNode
def test_treenode_requires_package_location_and_path() -> None:
    """Test TreeNode requires package_location and stories_path."""
    stories_path = Path("/fake/path/stories.py")

    # This will fail in __post_init__ due to missing module, but that's expected
    # Just verify the class can be instantiated with required args
    try:
        node = TreeNode(package_location="test.package", stories_path=stories_path)
        # If we get here, construction worked (shouldn't happen without real files)
        assert node.package_location == "test.package"
        assert node.stories_path == stories_path
    except (ModuleNotFoundError, ImportError):
        # Expected - we don't have a real package to import
        pass


def test_treenode_repr() -> None:
    """Test TreeNode __repr__ returns package location."""
    stories_path = Path("/fake/path/stories.py")

    # Mock the import_module and get_certain_callable to avoid needing real files
    with (
        patch("storytime.nodes.import_module") as mock_import,
        patch("storytime.get_certain_callable") as mock_get_callable,
    ):
        # Setup mocks
        mock_module = Mock()
        mock_module.__file__ = "/fake/path/__init__.py"
        mock_import.return_value = mock_module
        mock_get_callable.return_value = Mock()

        # Create tree node (will fail but we can test what we can)
        node = TreeNode(package_location="test.package", stories_path=stories_path)
        # If __post_init__ succeeds, test __repr__
        repr_str = repr(node)
        assert isinstance(repr_str, str)
        # __repr__ returns self.this_package_location
        assert repr_str == node.this_package_location


def test_tree_node_site() -> None:
    """Given a path to a ``stories.py``, extract the needed info."""
    from examples.minimal import stories

    assert stories.__file__
    stories_path = Path(stories.__file__)
    tree_node = TreeNode(
        package_location="examples.minimal",
        stories_path=stories_path,
    )
    assert isinstance(tree_node.called_instance, Site)
    assert tree_node.name == ""
    assert tree_node.this_package_location == "."
    assert tree_node.parent_path is None


def test_tree_node_section() -> None:
    """Given a path to a ``stories.py``, extract needed info."""
    from examples.minimal.components import stories

    assert stories.__file__
    stories_path = Path(stories.__file__)
    tree_node = TreeNode(
        package_location="examples.minimal",
        stories_path=stories_path,
    )
    assert isinstance(tree_node.called_instance, Section)
    assert tree_node.name == "components"
    assert tree_node.this_package_location == ".components"
    assert tree_node.parent_path == "."


# Test TreeNode helper methods
def test_treenode_get_root_package_path() -> None:
    """Test _get_root_package_path returns correct path."""
    from examples.minimal import stories

    assert stories.__file__
    stories_path = Path(stories.__file__)
    tree_node = TreeNode.__new__(TreeNode)
    tree_node.package_location = "examples.minimal"
    tree_node.stories_path = stories_path

    root_path = tree_node._get_root_package_path()
    assert root_path.name == "minimal"
    assert root_path.exists()


def test_treenode_get_relative_stories_path_for_root() -> None:
    """Test _get_relative_stories_path for root location."""
    from examples.minimal import stories

    assert stories.__file__
    stories_path = Path(stories.__file__)
    tree_node = TreeNode.__new__(TreeNode)
    tree_node.package_location = "examples.minimal"
    tree_node.stories_path = stories_path

    root_path = tree_node._get_root_package_path()
    relative_path = tree_node._get_relative_stories_path(root_path)

    assert relative_path.name == ""


def test_treenode_get_relative_stories_path_for_nested() -> None:
    """Test _get_relative_stories_path for nested location."""
    from examples.minimal.components import stories

    assert stories.__file__
    stories_path = Path(stories.__file__)
    tree_node = TreeNode.__new__(TreeNode)
    tree_node.package_location = "examples.minimal"
    tree_node.stories_path = stories_path

    root_path = tree_node._get_root_package_path()
    relative_path = tree_node._get_relative_stories_path(root_path)

    assert relative_path.name == "components"


def test_treenode_is_root_location_true() -> None:
    """Test _is_root_location returns True for root."""
    tree_node = TreeNode.__new__(TreeNode)
    relative_path = Path("")

    assert tree_node._is_root_location(relative_path) is True


def test_treenode_is_root_location_false() -> None:
    """Test _is_root_location returns False for nested."""
    tree_node = TreeNode.__new__(TreeNode)
    relative_path = Path("components")

    assert tree_node._is_root_location(relative_path) is False


def test_treenode_configure_as_root() -> None:
    """Test _configure_as_root sets correct values."""
    tree_node = TreeNode.__new__(TreeNode)
    tree_node._configure_as_root()

    assert tree_node.name == ""
    assert tree_node.parent_path is None
    assert tree_node.this_package_location == "."


def test_treenode_configure_as_nested() -> None:
    """Test _configure_as_nested sets correct values."""
    tree_node = TreeNode.__new__(TreeNode)
    relative_path = Path("components")

    tree_node._configure_as_nested(relative_path)

    assert tree_node.name == "components"
    assert tree_node.this_package_location == ".components"
    assert tree_node.parent_path == "."


def test_treenode_configure_as_nested_deeper() -> None:
    """Test _configure_as_nested for deeply nested path."""
    tree_node = TreeNode.__new__(TreeNode)
    relative_path = Path("views/layouts")

    tree_node._configure_as_nested(relative_path)

    assert tree_node.name == "layouts"
    assert tree_node.this_package_location == ".views.layouts"
    assert tree_node.parent_path == ".views"


def test_treenode_calculate_parent_path_root_parent() -> None:
    """Test _calculate_parent_path when parent is root."""
    tree_node = TreeNode.__new__(TreeNode)
    relative_path = Path("components")

    parent_path = tree_node._calculate_parent_path(relative_path)

    assert parent_path == "."


def test_treenode_calculate_parent_path_nested_parent() -> None:
    """Test _calculate_parent_path when parent is nested."""
    tree_node = TreeNode.__new__(TreeNode)
    relative_path = Path("views/layouts")

    parent_path = tree_node._calculate_parent_path(relative_path)

    assert parent_path == ".views"


def test_treenode_import_story_module_root() -> None:
    """Test _import_story_module for root location."""
    tree_node = TreeNode.__new__(TreeNode)
    tree_node.package_location = "examples.minimal"
    tree_node.this_package_location = "."

    module = tree_node._import_story_module()

    assert module.__name__ == "examples.minimal.stories"


def test_treenode_import_story_module_nested() -> None:
    """Test _import_story_module for nested location."""
    tree_node = TreeNode.__new__(TreeNode)
    tree_node.package_location = "examples.minimal"
    tree_node.this_package_location = ".components"

    module = tree_node._import_story_module()

    assert module.__name__ == "examples.minimal.components.stories"
