"""Tree node utilities for organizing stories hierarchically."""

from dataclasses import dataclass, field
from importlib import import_module
from pathlib import Path
from typing import Any


@dataclass()
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
        from storytime.utils import get_certain_callable

        root_package_path = self._get_root_package_path()
        relative_stories_path = self._get_relative_stories_path(root_package_path)

        if self._is_root_location(relative_stories_path):
            self._configure_as_root()
        else:
            self._configure_as_nested(relative_stories_path)

        story_module = self._import_story_module()
        self.called_instance = get_certain_callable(story_module)

    def _get_root_package_path(self) -> Path:
        """Get the root package path for relative calculations."""
        root_package = import_module(self.package_location)
        return Path(root_package.__file__).parent  # type: ignore[union-attr]

    def _get_relative_stories_path(self, root_package_path: Path) -> Path:
        """Get the relative path from root to the stories directory."""
        this_package_path = self.stories_path.parent
        return this_package_path.relative_to(root_package_path)

    def _is_root_location(self, relative_stories_path: Path) -> bool:
        """Check if this is the root location."""
        return relative_stories_path.name == ""

    def _configure_as_root(self) -> None:
        """Configure fields for root location."""
        self.name = ""
        self.parent_path = None
        self.this_package_location = "."

    def _configure_as_nested(self, relative_stories_path: Path) -> None:
        """Configure fields for nested location."""
        self.name = relative_stories_path.name
        self.this_package_location = f".{relative_stories_path}".replace("/", ".")
        self.parent_path = self._calculate_parent_path(relative_stories_path)

    def _calculate_parent_path(self, relative_stories_path: Path) -> str:
        """Calculate the parent path location string."""
        parent_path = relative_stories_path.parent
        if parent_path.name == "":
            return f"{parent_path}".replace("/", ".")
        return f".{parent_path}".replace("/", ".")

    def _import_story_module(self) -> Any:
        """Import the story module based on package location."""
        if self.this_package_location == ".":
            module_path = f"{self.package_location}.stories"
        else:
            module_path = f"{self.package_location}{self.this_package_location}.stories"
        return import_module(module_path)


@dataclass()
class BaseNode[T]:
    """Shared logic for Site/Section/Subject."""

    name: str = ""
    parent: None = None
    title: str | None = None
    context: object | None = None
    package_path: str = field(init=False, default="")

    def post_update(
        self,
        parent: "BaseNode[T] | None",
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
