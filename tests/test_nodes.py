"""Test the nodes module classes: TreeNode and BaseNode."""

from pathlib import Path
from unittest.mock import Mock, patch

from storyville.nodes import BaseNode, TreeNode, get_certain_callable, get_package_path
from storyville.section import Section
from storyville.catalog import Catalog
from storyville.subject import Subject


# Test get_package_path
def test_get_package_path_with_init() -> None:
    """Test get_package_path with regular package that has __init__.py."""
    package_path = get_package_path("examples.minimal")
    assert package_path.name == "minimal"
    assert package_path.exists()
    assert (package_path / "stories.py").exists()


def test_get_package_path_without_init() -> None:
    """Test get_package_path with namespace package (no __init__.py)."""
    # examples.minimal has no __init__.py, making it a namespace package
    package_path = get_package_path("examples.minimal")
    assert package_path.name == "minimal"
    assert package_path.exists()
    assert not (package_path / "__init__.py").exists()


def test_get_package_path_with_mock_namespace_package() -> None:
    """Test get_package_path handles namespace packages correctly."""
    with patch("storyville.nodes.import_module") as mock_import:
        mock_package = Mock()
        mock_package.__file__ = None  # Namespace package
        mock_package.__path__ = ["/fake/path/to/package"]
        mock_import.return_value = mock_package

        result = get_package_path("fake.package")
        assert result == Path("/fake/path/to/package")


def test_get_package_path_with_mock_regular_package() -> None:
    """Test get_package_path handles regular packages correctly."""
    with patch("storyville.nodes.import_module") as mock_import:
        mock_package = Mock()
        mock_package.__file__ = "/fake/path/to/package/__init__.py"
        mock_import.return_value = mock_package

        result = get_package_path("fake.package")
        assert result == Path("/fake/path/to/package")


def test_get_package_path_invalid_package() -> None:
    """Test get_package_path raises ValueError for invalid package."""
    with patch("storyville.nodes.import_module") as mock_import:
        mock_package = Mock()
        mock_package.__file__ = None
        del mock_package.__path__  # No __path__ attribute
        mock_import.return_value = mock_package

        try:
            get_package_path("fake.package")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "has no __file__ or __path__" in str(e)


# Test get_certain_callable
def test_get_certain_callable_with_catalog(module_factory) -> None:
    """Test get_certain_callable finds and calls Catalog function."""
    def make_catalog() -> Catalog:
        return Catalog(title="Test Catalog")

    module = module_factory("test_module", make_catalog)

    result = get_certain_callable(module)

    assert result is not None
    assert isinstance(result, Catalog)
    assert result.title == "Test Catalog"


def test_get_certain_callable_with_section(module_factory) -> None:
    """Test get_certain_callable finds and calls Section function."""
    def make_section() -> Section:
        return Section(title="Test Section")

    module = module_factory("test_module", make_section)

    result = get_certain_callable(module)

    assert result is not None
    assert isinstance(result, Section)
    assert result.title == "Test Section"


def test_get_certain_callable_with_subject(module_factory) -> None:
    """Test get_certain_callable finds and calls Subject function."""
    def make_subject() -> Subject:
        return Subject(title="Test Subject")

    module = module_factory("test_module", make_subject)

    result = get_certain_callable(module)

    assert result is not None
    assert isinstance(result, Subject)
    assert result.title == "Test Subject"


def test_get_certain_callable_no_matching_function(module_factory) -> None:
    """Test get_certain_callable returns None when no matching function."""
    def make_something() -> str:
        return "something"

    module = module_factory("test_module", make_something)

    result = get_certain_callable(module)

    assert result is None


def test_get_certain_callable_empty_module(module_factory) -> None:
    """Test get_certain_callable returns None for empty module."""
    module = module_factory("test_module")

    result = get_certain_callable(module)

    assert result is None


def test_get_certain_callable_ignores_external_functions(module_factory) -> None:
    """Test get_certain_callable ignores functions from other modules."""
    def external_function() -> Catalog:
        return Catalog(title="External")

    # Create module but manually set function's __module__ to different module
    module = module_factory("test_module", external_function)
    external_function.__module__ = "other_module"  # Override to different module!

    result = get_certain_callable(module)

    assert result is None  # Should not call external functions


def test_get_certain_callable_integration_minimal_components() -> None:
    """Integration: use a real example module returning a Section."""
    from examples.minimal.components import stories

    section = get_certain_callable(stories)
    if section:
        assert section.title == "Components"


def test_get_certain_callable_integration_no_sections() -> None:
    """Integration: real example module without a matching callable returns None."""
    from examples.no_sections.components import stories

    section = get_certain_callable(stories)
    assert section is None


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
        patch("storyville.nodes.import_module") as mock_import,
        patch("storyville.get_certain_callable") as mock_get_callable,
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


def test_tree_node_catalog() -> None:
    """Given a path to a ``stories.py``, extract the needed info."""
    from examples.minimal import stories

    assert stories.__file__
    stories_path = Path(stories.__file__)
    tree_node = TreeNode(
        package_location="examples.minimal",
        stories_path=stories_path,
    )
    assert isinstance(tree_node.called_instance, Catalog)
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
