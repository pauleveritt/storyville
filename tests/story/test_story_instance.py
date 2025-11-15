"""Test the updated Story.instance property for Node return type."""

from tdom import Element, html

from storytime.story import Story


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


def test_story_instance_returns_none_when_no_component() -> None:
    """Test Story.instance returns None when no component exists."""
    story = Story()
    assert story.instance is None


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
