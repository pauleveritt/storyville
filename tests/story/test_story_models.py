"""Test the Story model."""

from tdom import Element, html

from storyville.story import Story
from storyville.subject import Subject


# Story.post_update Tests
def test_story_post_update_basic() -> None:
    """Test Story post_update sets parent."""
    parent = Subject(title="Components")
    parent.package_path = ".components"
    story = Story()
    story.post_update(parent=parent)

    assert story.parent is parent


def test_story_post_update_inherits_component(my_component) -> None:
    """Test Story post_update inherits target from parent."""
    parent = Subject(title="Components", target=my_component)
    parent.package_path = ".components"

    story = Story()
    story.post_update(parent=parent)

    assert story.target is my_component


def test_story_post_update_keeps_own_component(parent_component, own_component) -> None:
    """Test Story post_update keeps its own target."""
    parent = Subject(title="Components", target=parent_component)
    parent.package_path = ".components"

    story = Story(target=own_component)
    story.post_update(parent=parent)

    assert story.target is own_component


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
    """Test Story.instance returns None when no target."""
    story = Story()
    assert story.instance is None


def test_story_instance_with_props() -> None:
    """Test Story.instance passes props to target."""

    def my_component(name: str = "default"):
        """Component that returns a Node."""
        return html(t"<div>{name}</div>")

    story = Story(target=my_component, props={"name": "custom"})
    instance = story.instance

    assert instance is not None
    assert isinstance(instance, Element)


def test_story_instance_returns_element_when_component_provided() -> None:
    """Test Story.instance returns Element when target provided."""

    def element_component(title: str = "Test"):
        """A component that returns a Node."""
        return html(t"<div>{title}</div>")

    story = Story(target=element_component, props={"title": "Hello"})
    instance = story.instance

    assert instance is not None
    assert isinstance(instance, Element)


def test_story_instance_type_guard_with_element_returning_component() -> None:
    """Test type guard assertion with Element-returning target."""

    def valid_component(content: str = "default"):
        """A component that returns a Node."""
        return html(t"<p>{content}</p>")

    story = Story(target=valid_component, props={"content": "World"})
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
        target=complex_component,
        props={"title": "Test", "count": 42, "items": ["a", "b", "c"]},
    )
    instance = story.instance

    assert instance is not None
    assert isinstance(instance, Element)
