"""Promote component-driven-development with a browseable catalog.

Storytime is a system for component-driven-development (CDD.)
You write stories as you develop components, expressing all the variations.
You can then browse them in a web page, as well as use these stories in testing.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from importlib import import_module
from importlib.resources import files
from inspect import getmembers
from inspect import isfunction
from pathlib import Path
from types import ModuleType
from typing import Any
from typing import Callable
from typing import Generic
from typing import Iterable
from typing import Optional
from typing import TypeVar
from typing import Union
from typing import cast
from typing import get_type_hints

from bs4 import BeautifulSoup
from hopscotch import Registry
from viewdom import html, render, VDOM

Scannable = ModuleType  # Wanted to use Union[str, ModuleType] but PyCharm
Scannables = Union[Iterable[Scannable], Scannable]
Singleton = Union[tuple[object, object], object]
Singletons = list[Singleton, ...]

PACKAGE_DIR = Path(__file__).resolve().parent


def get_certain_callable(module: ModuleType) -> Optional[Union[Site, Section, Subject]]:
    """Return the first Site/Section/Subject in given module that returns correct type.

    A ``stories.py`` file should have a function that, when called,
    constructs an instance of a Section, Subject, etc. This helper
    function does the locating and construction. If no function
    is found with the correct return value, return None.

    We do it this way instead of magically-named functions, meaning,
    we don't do convention over configuration.

    Args:
        module: A stories.py module that should have the right function.

    Returns:
        The Site/Section/Story instance or ``None`` if there wasn't an
        appropriate function.
    """
    valid_returns = (Site, Section, Subject)
    for _name, obj in getmembers(module):
        if isfunction(obj) and obj.__module__ is module.__name__:
            th = get_type_hints(obj)
            return_type = th.get("return")
            if return_type and return_type in valid_returns:
                # Call the obj to let it construct and return the
                # Site/Section/Subject
                target: Union[Site, Section, Subject] = obj()
                return target

    # We didn't find an appropriate callable
    return None


@dataclass()
class TreeNode:
    """Adapt a story path into all info needed to seat in tree.

    Extracting a ``stories.py`` into a tree node is somewhat complicated.
    You have to import the module, convert path to dotted-package-name form,
    find the parent, etc.
    """

    package_location: str  # E.g. examples.minimal
    stories_path: Path
    name: str = field(init=False)
    called_instance: object = field(init=False)
    this_package_location: str = field(init=False)
    parent_path: Optional[str] = field(init=False)

    def __repr__(self) -> str:
        """Provide a friendly representation."""
        return self.this_package_location

    def __post_init__(self) -> None:
        """Assign calculated fields."""
        # We want:
        # - The full-dotted path (to import the module)
        # - The relative-dotted path, e.g. .components.heading (for display)
        # - The Location-style name e.g. heading (to store in parent)
        # - Location-style name for  parent e.g. .components (to look up in tree)
        # - The callable instance

        # Get the PosixPath to the root so we can use pathlib for some
        # relative operations.
        root_package = import_module(self.package_location)
        root_package_path = Path(root_package.__file__).parent

        # Whichever subpackage we are pointed at, get its path so we
        # can calculate some relative operations, particular, to get a
        # relative "Location" string such as ".components.heading".
        this_package_path = self.stories_path.parent
        relative_stories_path = this_package_path.relative_to(root_package_path)
        relative_stories_package_path = relative_stories_path.name
        if relative_stories_package_path == "":
            # We are at the root
            self.name = ""
            self.parent_path = None
            self.this_package_location = "."
            story_module = import_module(self.package_location + ".stories")
        else:
            self.name = relative_stories_path.name
            self.this_package_location = f".{relative_stories_path}".replace("/", ".")
            parent_path = relative_stories_path.parent
            if parent_path.name == "":
                self.parent_path = f"{parent_path}".replace("/", ".")
            else:
                self.parent_path = f".{parent_path}".replace("/", ".")
            sm = self.package_location + self.this_package_location + ".stories"
            story_module = import_module(sm)
        self.called_instance = get_certain_callable(story_module)


def make_site(package_location: str) -> Site:
    """Create a site with a populated tree.

    This is called from the CLI with a package-name path such
    as ``examples.minimal`` which is the root of a Storytime tree.

    Args:
        package_location: The top-level dotted-package-name of the root.

    Returns:
        A populated site.
    """
    # Turn the package dotted name of self.target into ``Path``
    stories_package_name = cast(Path, files(package_location))

    # Get all the stories.py under here
    tree_nodes: list[TreeNode] = [
        TreeNode(
            package_location=package_location,
            stories_path=stories_path,
        )
        for stories_path in stories_package_name.glob("**/stories.py")
    ]
    # First get the Site
    site: Optional[Site] = None
    for tree_node in tree_nodes:
        if isinstance(tree_node.called_instance, Site):
            site = tree_node.called_instance
            site.post_update(
                parent=None,
                tree_node=tree_node,
            )
    site = cast(Site, site)

    # Now the sections
    for tree_node in tree_nodes:
        section = tree_node.called_instance
        if isinstance(section, Section):
            section.post_update(parent=site, tree_node=tree_node)
            site.items[section.name] = section

    # Now the subjects
    for tree_node in tree_nodes:
        subject = tree_node.called_instance
        if isinstance(subject, Subject):
            parent = site.find_path(tree_node.parent_path)
            if isinstance(parent, Section):
                subject.post_update(parent=parent, tree_node=tree_node)
                parent.items[subject.name] = subject
            for story in subject.stories:
                story.post_update(subject)

    return site


def make_tree_node_registry(
    context: Optional[object] = None,
    registry: Optional[Registry] = None,
    parent: Optional[Registry] = None,
    scannables: Optional[Scannables] = None,
    singletons: Optional[Singletons] = None,
) -> Optional[Registry]:
    """Used by tree nodes to encode the policy of registry-making."""
    if registry is not None:
        # This node is being instantiated with a custom registry,
        # so we ignore context/scannables/plugins/parent
        return registry

    if context is None and scannables is None and singletons is None:
        # This node does not have any custom stuff for a registry,
        # so just use the parent, unless it's the site and we need
        # to make one.
        if parent is None:
            return Registry()
        return parent

    # Time to make a registry for this node, we were given some
    # stuff for a local registry.
    this_registry = Registry(context=context, parent=parent)
    if scannables:
        for scannable in scannables:
            this_registry.scan(scannable)
    if singletons:
        for singleton in singletons:
            # Allow a story to use a singleton just by itself
            # or registered as a kind.
            if isinstance(singleton, tuple):
                obj, kind = singleton
                this_registry.register(obj, kind=kind)
            else:
                this_registry.register(singleton)
    return this_registry


T = TypeVar("T")


@dataclass()
class BaseNode(Generic[T]):
    """Shared logic for Site/Section/Subject."""

    name: str = ""
    parent: None = None
    title: Optional[str] = None
    context: Optional[object] = None
    registry: Optional[Registry] = None
    scannables: Optional[Scannables] = None
    singletons: Optional[Singletons] = None
    package_path: str = field(init=False)

    def post_update(
        self,
        parent: Optional[BaseNode],
        tree_node: TreeNode,
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
        self.parent = parent
        self.name = tree_node.name
        self.package_path = tree_node.this_package_location
        self.registry = make_tree_node_registry(
            context=self.context,
            parent=parent.registry if parent else None,
            registry=self.registry,
            scannables=self.scannables,
            singletons=self.singletons,
        )
        if self.title is None:
            self.title = self.package_path
        return self


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
    registry: Optional[Registry] = None
    singletons: Optional[Singletons] = None
    title: Optional[str] = None
    template: Optional[VDOM] = None

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
                return self.registry.get(self.component, **self.props)

        return None

    @property
    def vdom(self) -> VDOM:
        """Generate a VDOM for the usage in this story."""
        if self.component:
            # We ignore the template if we are given a component and
            # instead construct a template.
            return html("<{self.component} ...{self.props} />")
        elif self.template:
            return self.template
        else:
            raise ValueError("Could not generate VDOM for story.")

    @property
    def soup(self) -> BeautifulSoup:
        """Render to a DOM-like BeautifulSoup representation."""
        rendered = render(self.vdom, registry=self.registry)
        this_html = BeautifulSoup(rendered, "html.parser")
        return this_html
