"""Story and Subject classes for component-driven development."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Generic, Optional, TypeVar, Union

if TYPE_CHECKING:
    from storytime import Singletons

T = TypeVar("T")


@dataclass()
class BaseNode(Generic[T]):
    """Shared logic for Site/Section/Subject."""

    name: str = ""
    parent: None = None
    title: Optional[str] = None
    context: Optional[object] = None
    registry: Optional[object] = None
    scannables: Optional[object] = None
    singletons: Optional[object] = None
    package_path: str = field(init=False, default="")

    def post_update(
        self,
        parent: Optional[BaseNode],
        tree_node: object,
    ) -> T:
        """The parent calls this after construction.

        We do this as a convenience, so authors don't have to put a bunch
        of attributes in their stories.

        Args:
            parent: The Site that is the parent in the tree.
            tree_node: The raw data from the scanning process.

        Returns:
            The updated Section.
        """
        from storytime import make_tree_node_registry

        self.parent = parent  # type: ignore
        self.name = tree_node.name  # type: ignore
        self.package_path = tree_node.this_package_location  # type: ignore
        self.registry = make_tree_node_registry(
            context=self.context,
            parent=parent.registry if parent else None,  # type: ignore
            registry=self.registry,
            scannables=self.scannables,  # type: ignore
            singletons=self.singletons,  # type: ignore
        )
        if self.title is None:
            self.title = self.package_path
        return self  # type: ignore


@dataclass()
class Site(BaseNode):
    """The top of a Storytime catalog.

    The site contains the organized collections of stories, with
    logic to render to disk.
    """

    items: dict[str, Section] = field(default_factory=dict)
    static_dir: Path | None = None

    def __post_init__(self):
        """Look for a static dir and assign it if present."""
        from storytime import PACKAGE_DIR

        sd = PACKAGE_DIR / "static"
        if sd.exists():
            self.static_dir = sd

    def find_path(self, path: str) -> Optional[Union[Site, Section, Subject, Story]]:
        """Given a dotted path, traverse to the object."""
        current = self
        segments = path.split(".")[1:]
        for segment in segments:
            if current is not None:
                current = current.items.get(segment)  # type: ignore
        return current


@dataclass()
class Section(BaseNode):
    """A grouping of stories, such as ``Views``."""

    parent: Optional[Site] = None
    items: dict[str, Subject] = field(default_factory=dict)


@dataclass()
class Subject(BaseNode):
    """The component that a group of stories or variants is about."""

    parent: Optional[Section] = None
    component: Optional[Union[type, Callable]] = None
    stories: list[Story] = field(default_factory=list)


@dataclass()
class Story:
    """One way to look at a component."""

    component: Optional[Union[type, Callable]] = None
    kind: Optional[type] = None
    parent: Subject = field(init=False)
    props: dict[str, Any] = field(default_factory=dict)
    registry: Optional[object] = None
    singletons: Optional[Singletons] = None
    title: Optional[str] = None
    template: Optional[object] = None

    def post_update(self, parent: Subject) -> Story:
        """The parent calls this after construction.

        We do this as a convenience, so authors don't have to put a bunch
        of attributes in their stories.

        Args:
            parent: The Section that is the parent in the tree.

        Returns:
            The updated Story.
        """
        self.parent = parent
        if self.registry is None:
            self.registry = parent.registry
        if self.component is None and self.parent.component:
            self.component = self.parent.component
        if self.title is None:
            if self.parent.title:
                self.title = self.parent.title + " Story"
            else:
                self.title = self.parent.package_path
        return self

    @property
    def instance(self) -> Optional[object]:
        """Get the component instance related to this story."""
        if self.component:
            if self.registry is None:
                return self.component(**self.props)
            else:
                return self.registry.get(self.component, **self.props)  # type: ignore

        return None

    @property
    def vdom(self) -> object:
        """Generate a VDOM for the usage in this story."""
        from tdom import html

        if self.component:
            # We ignore the template if we are given a component and
            # instead construct a template.
            return html("<{self.component} ...{self.props} />")
        elif self.template:
            return self.template
        else:
            raise ValueError("Could not generate VDOM for story.")

    # @property
    # def soup(self) -> BeautifulSoup:
    #     """Render to a DOM-like BeautifulSoup representation."""
    #     rendered = render(self.vdom, registry=self.registry)
    #     this_html = BeautifulSoup(rendered, "html.parser")
    #     return this_html
