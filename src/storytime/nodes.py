"""Tree node utilities for organizing stories hierarchically."""

from __future__ import annotations

from dataclasses import dataclass, field
from importlib import import_module
from inspect import getmembers, isfunction
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING, Any, get_type_hints

if TYPE_CHECKING:
    from storytime.section import Section
    from storytime.site import Site
    from storytime.subject import Subject


def get_package_path(package_name: str) -> Path:
    """Get the filesystem path for a package.

    Handles both regular packages (with __init__.py) and namespace packages (without).

    Args:
        package_name: The dotted package name (e.g., "examples.minimal").

    Returns:
        The Path to the package directory.

    Raises:
        ValueError: If the package has neither __file__ nor __path__.
    """
    package = import_module(package_name)
    if package.__file__ is None:
        # Namespace package without __init__.py - use __path__
        if not hasattr(package, "__path__"):
            raise ValueError(f"Package '{package_name}' has no __file__ or __path__")
        return Path(package.__path__[0])
    return Path(package.__file__).parent


def get_certain_callable(module: ModuleType) -> Site | Section | Subject | None:
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
    from storytime.section import Section
    from storytime.site import Site
    from storytime.subject import Subject

    valid_returns = (Site, Section, Subject)
    for _name, obj in getmembers(module):
        if isfunction(obj) and obj.__module__ is module.__name__:
            th = get_type_hints(obj)
            return_type = th.get("return")
            if return_type and return_type in valid_returns:
                # Call the obj to let it construct and return the
                # Site/Section/Subject
                target: Site | Section | Subject = obj()
                return target

    # We didn't find an appropriate callable
    return None


@dataclass
class TreeNode:
    """Adapt a story path into all info needed to seat in a tree.

    Extracting a ``stories.py`` into a tree node is somewhat complicated.
    You have to import the module, convert the path to a dotted-package-name
    form, find the parent, etc.
    """

    package_location: str  # E.g. examples.minimal
    stories_path: Path
    name: str = field(init=False)
    called_instance: object = field(init=False)
    this_package_location: str = field(init=False)
    parent_path: str | None = field(init=False)

    def __repr__(self) -> str:
        """Provide a friendly representation."""
        return self.this_package_location

    def __post_init__(self) -> None:
        """Assign calculated fields."""
        root_package_path = get_package_path(self.package_location)
        this_package_path = self.stories_path.parent
        relative_stories_path = this_package_path.relative_to(root_package_path)

        # Configure based on whether this is root or nested location
        if relative_stories_path.name == "":
            # Root location
            self.name = ""
            self.parent_path = None
            self.this_package_location = "."
        else:
            # Nested location
            self.name = relative_stories_path.name
            self.this_package_location = f".{relative_stories_path}".replace("/", ".")

            # Calculate parent path
            parent_path = relative_stories_path.parent
            if parent_path.name == "":
                self.parent_path = f"{parent_path}".replace("/", ".")
            else:
                self.parent_path = f".{parent_path}".replace("/", ".")

        story_module = self._import_story_module()
        self.called_instance = get_certain_callable(story_module)

    def _import_story_module(self) -> Any:
        """Import the story module based on package location."""
        if self.this_package_location == ".":
            module_path = f"{self.package_location}.stories"
        else:
            module_path = f"{self.package_location}{self.this_package_location}.stories"
        return import_module(module_path)


@dataclass
class BaseNode[T]:
    """Shared logic for Site/Section/Subject."""

    name: str = ""
    parent: None = None
    title: str | None = None
    context: object | None = None
    package_path: str = field(init=False, default="")

    def post_update(
        self,
        parent: BaseNode[T] | None,
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

        self.parent = parent  # type: ignore[assignment]
        self.name = tree_node.name  # type: ignore[attr-defined]
        self.package_path = tree_node.this_package_location  # type: ignore[attr-defined]
        if self.title is None:
            self.title = self.package_path
        return self  # type: ignore[return-value]
