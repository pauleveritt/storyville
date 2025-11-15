"""Test the Story model."""

from dataclasses import dataclass

from tdom import Element, html

from storytime.story import Story
from storytime.subject import Subject


# Story Initialization Tests
def test_story_initialization() -> None:
    """Test Story can be instantiated."""
    story = Story(title="Default")
    assert story.title == "Default"
    assert story.component is None
    assert story.props == {}
    assert story.template is None


# Story Configuration Tests
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


# Story.post_update Tests
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


# Story.instance Tests
def test_story_instance_without_component() -> None:
    """Test Story.instance returns None when no component."""
    story = Story()
    assert story.instance is None


def test_story_instance_with_props() -> None:
    """Test Story.instance passes props to component."""

    def my_component(name: str = "default"):
        """Component that returns a Node."""
        return html(t"<div>{name}</div>")

    story = Story(component=my_component, props={"name": "custom"})
    instance = story.instance

    assert instance is not None
    assert isinstance(instance, Element)


def test_story_instance_returns_element_when_component_provided() -> None:
    """Test Story.instance returns Element when component provided."""

    def element_component(title: str = "Test"):
        """A component that returns a Node."""
        return html(t"<div>{title}</div>")

    story = Story(component=element_component, props={"title": "Hello"})
    instance = story.instance

    assert instance is not None
    assert isinstance(instance, Element)


def test_story_instance_type_guard_with_element_returning_component() -> None:
    """Test type guard assertion with Element-returning component."""

    def valid_component(content: str = "default"):
        """A component that returns a Node."""
        return html(t"<p>{content}</p>")

    story = Story(component=valid_component, props={"content": "World"})
    instance = story.instance

    # The type guard in the test ensures this is an Element
    assert isinstance(instance, Element)
    assert type(instance).__name__ == "Element"


def test_story_instance_with_complex_props() -> None:
    """Test Story.instance handles complex props correctly."""

    def complex_component(
        title: str = "default", count: int = 0, items: list[str] | None = None
    ):
        """A component with multiple props."""
        items_html = "".join(f"<li>{item}</li>" for item in (items or []))
        return html(
            t"<div><h1>{title}</h1><p>Count: {count}</p><ul>{items_html}</ul></div>"
        )

    story = Story(
        component=complex_component,
        props={"title": "Test", "count": 42, "items": ["a", "b", "c"]},
    )
    instance = story.instance

    assert instance is not None
    assert isinstance(instance, Element)
