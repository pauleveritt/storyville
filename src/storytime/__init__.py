"""Promote component-driven-development with a browseable catalog.

Storytime is a system for component-driven-development (CDD.)
You write stories as you develop components, expressing all the variations.
You can then browse them in a web page, as well as use these stories in testing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from importlib import import_module
from importlib.resources import files
from inspect import getmembers, isfunction
from pathlib import Path
from types import ModuleType
from typing import (
    Iterable,
    Optional,
    Union,
    cast,
    get_type_hints,
)

# Import all node classes from story module
from storytime.story import BaseNode as BaseNode
from storytime.story import Section as Section
from storytime.story import Site as Site
from storytime.story import Story as Story
from storytime.story import Subject as Subject

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
    registry: Optional[object] = None,
    parent: Optional[object] = None,
    scannables: Optional[Scannables] = None,
    singletons: Optional[Singletons] = None,
) -> Optional[object]:
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
            from hopscotch import Registry

            return Registry()
        return parent

    # Time to make a registry for this node, we were given some
    # stuff for a local registry.
    from hopscotch import Registry

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
