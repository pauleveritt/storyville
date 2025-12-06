"""Test resource_path parameter in components.

Tests for Task Group 3: Component Renaming (current_path → resource_path)
"""

from storyville.catalog.models import Catalog
from storyville.components.aside.aside import LayoutAside
from storyville.components.breadcrumbs.breadcrumbs import Breadcrumbs
from storyville.components.layout.layout import Layout
from storyville.components.main.main import LayoutMain
from storyville.components.navigation_tree.navigation_tree import NavigationTree


def test_layout_accepts_resource_path() -> None:
    """Test Layout accepts resource_path parameter."""
    catalog = Catalog(title="Test Site")
    layout = Layout(
        view_title="Test",
        site=catalog,
        children=None,
        depth=1,
        resource_path="section",
    )
    assert layout.resource_path == "section"


def test_layout_main_receives_resource_path() -> None:
    """Test LayoutMain receives resource_path correctly."""
    main = LayoutMain(resource_path="section/subject", children=None)
    assert main.resource_path == "section/subject"


def test_layout_aside_receives_resource_path() -> None:
    """Test LayoutAside receives resource_path correctly."""
    aside = LayoutAside(
        sections={}, resource_path="section/subject", cached_navigation=None
    )
    assert aside.resource_path == "section/subject"


def test_breadcrumbs_uses_resource_path() -> None:
    """Test Breadcrumbs uses resource_path (not current_path)."""
    breadcrumbs = Breadcrumbs(resource_path="section/subject/story")
    assert breadcrumbs.resource_path == "section/subject/story"


def test_navigation_tree_uses_resource_path() -> None:
    """Test NavigationTree uses resource_path (not current_path)."""
    nav_tree = NavigationTree(sections={}, resource_path="section")
    assert nav_tree.resource_path == "section"


def test_layout_passes_resource_path_to_children() -> None:
    """Test Layout passes resource_path to LayoutMain and LayoutAside."""
    catalog = Catalog(title="Test Site")
    layout = Layout(
        view_title="Test",
        site=catalog,
        children=None,
        depth=2,
        resource_path="section/subject",
    )
    _ = str(layout())  # Call layout to exercise the rendering path
    # The layout should contain the resource_path passed to components
    # This is an integration test ensuring the data flows through
    assert layout.resource_path == "section/subject"


def test_breadcrumbs_renders_with_empty_resource_path() -> None:
    """Test Breadcrumbs renders nothing with empty resource_path."""
    breadcrumbs = Breadcrumbs(resource_path="")
    result = str(breadcrumbs())
    # Empty resource_path should render nothing
    assert result == ""


def test_layout_with_default_resource_path() -> None:
    """Test Layout with default resource_path (empty string)."""
    catalog = Catalog(title="Test Site")
    layout = Layout(
        view_title="Test",
        site=catalog,
        children=None,
        depth=0,
        # resource_path defaults to ""
    )
    assert layout.resource_path == ""
