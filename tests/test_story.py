"""Test the Story class."""

from dataclasses import dataclass

from storytime.story import Story
from storytime.subject import Subject


# Test Story
def test_story_initialization() -> None:
    """Test Story can be instantiated."""
    story = Story(title="Default")
    assert story.title == "Default"
    assert story.component is None
    assert story.props == {}
    assert story.template is None


def test_story_with_component() -> None:
    """Test Story with component."""

    @dataclass
    class MyComponent:
        name: str = "test"

    story = Story(title="Default", component=MyComponent)
    assert story.component is MyComponent


def test_story_with_props() -> None:
    """Test Story with props."""
    story = Story(title="Default", props={"name": "value"})
    assert story.props == {"name": "value"}


def test_story_post_update_basic() -> None:
    """Test Story post_update sets parent."""
    parent = Subject(title="Components")
    parent.package_path = ".components"
    story = Story()
    story.post_update(parent=parent)

    assert story.parent is parent


def test_story_post_update_inherits_component() -> None:
    """Test Story post_update inherits component from parent."""

    @dataclass
    class MyComponent:
        name: str = "test"

    parent = Subject(title="Components", component=MyComponent)
    parent.package_path = ".components"

    story = Story()
    story.post_update(parent=parent)

    assert story.component is MyComponent


def test_story_post_update_keeps_own_component() -> None:
    """Test Story post_update keeps its own component."""

    @dataclass
    class ParentComponent:
        name: str = "parent"

    @dataclass
    class OwnComponent:
        name: str = "own"

    parent = Subject(title="Components", component=ParentComponent)
    parent.package_path = ".components"

    story = Story(component=OwnComponent)
    story.post_update(parent=parent)

    assert story.component is OwnComponent


def test_story_post_update_generates_title_from_parent_title() -> None:
    """Test Story post_update generates title from parent title."""
    parent = Subject(title="Heading Component")
    parent.package_path = ".components.heading"

    story = Story()
    story.post_update(parent=parent)

    assert story.title == "Heading Component Story"


def test_story_post_update_generates_title_from_package_path() -> None:
    """Test Story post_update uses package_path when parent has no title."""
    parent = Subject()
    parent.package_path = ".components.heading"

    story = Story()
    story.post_update(parent=parent)

    assert story.title == ".components.heading"


def test_story_post_update_preserves_custom_title() -> None:
    """Test Story post_update preserves custom title."""
    parent = Subject(title="Components")
    parent.package_path = ".components"

    story = Story(title="Custom Title")
    story.post_update(parent=parent)

    assert story.title == "Custom Title"


def test_story_instance_without_component() -> None:
    """Test Story.instance returns None when no component."""
    story = Story()
    assert story.instance is None


def test_story_instance_with_props() -> None:
    """Test Story.instance passes props to component."""

    @dataclass
    class MyComponent:
        name: str = "default"

    story = Story(component=MyComponent, props={"name": "custom"})
    instance = story.instance

    assert instance is not None
    assert isinstance(instance, MyComponent)
    assert instance.name == "custom"  # type: ignore
