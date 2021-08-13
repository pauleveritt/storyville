"""Ensure all variations of a ``Story`` obey policies."""
from dataclasses import dataclass

from hopscotch import Registry
from hopscotch.operators import get
from viewdom import VDOM
from viewdom.render import html

from storytime import Section
from storytime import Story


@dataclass()
class DummyConfig:
    """Simple configuration to inject."""

    title: str = "Dummy Config"


def test_empty() -> None:
    """The simplest possible story."""
    story = Story(title="Empty")
    assert story.title == "Empty"


def test_generate_title() -> None:
    """Default to a title from the parent."""
    parent = Section(title="Components")
    story = Story()
    story.post_update(parent=parent)
    assert story.title == "Components Story"


def test_static_template_no_registry() -> None:
    """The simplest possible *useful* story."""
    template = html("<div>Hello</div>")
    story = Story(template=template)
    assert story.template == template
    assert story.instance is None
    assert story.vdom.tag == "div"
    assert story.vdom.props == {}
    assert story.vdom.children == ["Hello"]
    div = story.soup.select_one("div")
    assert div.text == "Hello"


def test_static_template_with_registry() -> None:
    """The simplest possible *useful* story with an unused empty registry."""
    registry = Registry()
    template = html("<div>Hello</div>")
    story = Story(registry=registry, template=template)
    assert story.instance is None
    div = story.soup.select_one("div")
    assert div.text == "Hello"


def test_template_local_symbol() -> None:
    """Template uses a local symbol."""
    name = "World"
    assert name
    template = html("<div>Hello {name}</div>")
    story = Story(template=template)
    assert story.instance is None
    div = story.soup.select_one("div")
    assert div.text == "Hello World"


def test_template_local_component() -> None:
    """Template uses a local component."""

    def Hello(name: str = "World") -> VDOM:  # noqa: N802
        assert name
        return html("<div>Hello {name}</div>")

    template = html("<{Hello} />")
    story = Story(template=template)
    assert story.instance is None
    assert story.vdom.tag == Hello
    div = story.soup.select_one("div")
    assert div.text == "Hello World"


def test_template_singleton() -> None:
    """Template gets a simple value from the registry."""
    registry = Registry()
    registry.register(DummyConfig())

    def Hello(dummy_config: DummyConfig) -> VDOM:  # noqa: N802
        name = dummy_config.title
        assert name
        return html("<div>Hello {name}</div>")

    template = html("<{Hello} />")
    story = Story(registry=registry, template=template)
    assert story.instance is None
    assert story.vdom.tag == Hello
    div = story.soup.select_one("div")
    assert div.text == "Hello Dummy Config"


def test_template_component() -> None:
    """Template uses a dataclass component which injects something."""

    @dataclass()  # noqa: D202
    class Hello:
        """A simple component."""

        name: str = get(DummyConfig, attr="title")

        def __call__(self) -> VDOM:
            """Render to a VDOM."""
            return html("<div>Hello {self.name}</div>")

    registry = Registry()
    registry.register(DummyConfig())
    registry.register(Hello)

    template = html("<{Hello} />")
    story = Story(registry=registry, template=template)
    assert story.instance is None
    assert story.vdom.tag == Hello
    div = story.soup.select_one("div")
    assert div.text == "Hello Dummy Config"


def test_component() -> None:
    """Story points at a component, no registry, no template."""

    @dataclass()
    class Hello:
        """A simple component."""

        name: str = "World"

        def __call__(self) -> VDOM:
            """Render to a VDOM."""
            return html("<div>Hello {self.name}</div>")

    story = Story(component=Hello)
    assert story.instance.__class__ is Hello
    assert story.instance.name == "World"
    assert story.vdom.tag == Hello
    div = story.soup.select_one("div")
    assert div.text == "Hello World"


def test_component_props() -> None:
    """Story points at a component, no registry, no template."""

    @dataclass()
    class Hello:
        """A simple component."""

        name: str = "World"

        def __call__(self) -> VDOM:
            """Render to a VDOM."""
            return html("<div>Hello {self.name}</div>")

    story = Story(component=Hello, props=dict(name="Override"))
    assert story.instance.__class__ is Hello
    assert story.instance.name == "Override"
    assert story.vdom.tag == Hello
    div = story.soup.select_one("div")
    assert div.text == "Hello Override"


def test_component_from_registry() -> None:
    """Story gets a component from registry."""

    @dataclass()
    class Hello:
        """A simple component."""

        name: str = "World"

        def __call__(self) -> VDOM:
            """Render to a VDOM."""
            return html("<div>Hello {self.name}</div>")

    registry = Registry()
    registry.register(Hello)

    story = Story(component=Hello, registry=registry)
    assert story.instance.__class__ is Hello
    assert story.instance.name == "World"
    assert story.vdom.tag == Hello
    div = story.soup.select_one("div")
    assert div.text == "Hello World"
