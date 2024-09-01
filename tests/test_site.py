"""The ``Site`` is the top of the Storytime catalog."""

from pathlib import Path

import pytest
from hopscotch import Registry

from storytime import get_certain_callable
from storytime import make_site
from storytime import make_tree_node_registry
from storytime import Section
from storytime import Site
from storytime import TreeNode


@pytest.fixture(scope="session")
def minimal_site() -> Site:
    """Construct the example minimal site."""
    site = make_site("examples.minimal")
    return site


def test_tree_node_registry_no_registry() -> None:
    """Not passed in registry but no extras."""
    registry = make_tree_node_registry()
    if registry:
        assert registry.parent is None
        assert registry.context is None


def test_tree_node_registry_no_registry_plus_extras() -> None:
    """Not passed in registry but with extras."""
    context = object()
    parent = Registry()
    registry = make_tree_node_registry(
        context=context,
        parent=parent,
    )
    if registry:
        assert registry.parent is parent
        assert registry.context is context


def test_tree_node_site() -> None:
    """Given a path to a ``stories.py``, extract needed info."""
    from examples.minimal import stories

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

    stories_path = Path(stories.__file__)
    tree_node = TreeNode(
        package_location="examples.minimal",
        stories_path=stories_path,
    )
    assert isinstance(tree_node.called_instance, Section)
    assert tree_node.name == "components"
    assert tree_node.this_package_location == ".components"
    assert tree_node.parent_path == "."


def test_make_site(minimal_site: Site) -> None:
    """Construct a story catalog."""
    assert minimal_site.name == ""
    assert minimal_site.parent is None
    assert minimal_site.package_path == "."
    assert minimal_site.title == "Minimal Site"
    components = minimal_site.items["components"]
    assert components.parent is minimal_site
    assert components.name == "components"
    assert components.package_path == ".components"
    assert components.registry is minimal_site.registry
    assert components.registry.parent is None
    assert components.title == "Components"
    found_components = minimal_site.find_path(".components")
    if found_components:
        assert found_components.title == "Components"

    heading = components.items["heading"]
    assert heading.parent is components
    assert heading.name == "heading"
    assert heading.package_path == ".components.heading"
    assert heading.title == "Heading"
    found_heading = minimal_site.find_path(".components.heading")
    if found_heading:
        assert found_heading.title == "Heading"


def test_stories(minimal_site: Site) -> None:
    """Grab a subject and get its list of stories."""
    heading = minimal_site.items["components"].items["heading"]
    stories = heading.stories
    first_story = stories[0]
    assert first_story.title == "Heading Story"


def test_get_certain_callable() -> None:
    """Given a module, find the function that returns certain type."""
    from examples.minimal.components import stories

    section = get_certain_callable(stories)
    if section:
        assert section.title == "Components"


def test_no_callable() -> None:
    """This example does not have a function with correct return type."""
    from examples.no_sections.components import stories

    section = get_certain_callable(stories)
    assert section is None
