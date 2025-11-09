"""Story and Subject classes for component-driven development."""

from dataclasses import dataclass, field
from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    pass


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
    parent_path: str | None = field(init=False)

    def __repr__(self) -> str:
        """Provide a friendly representation."""
        return self.this_package_location

    def __post_init__(self) -> None:
        """Assign calculated fields."""
        from storytime import get_certain_callable

        # We want:
        # - The full-dotted path (to import the module)
        # - The relative-dotted path, e.g. .components.heading (for display)
        # - The Location-style name e.g. heading (to store in parent)
        # - Location-style name for  parent e.g. .components (to look up in tree)
        # - The callable instance

        # Get the PosixPath to the root so we can use pathlib for some
        # relative operations.
        root_package = import_module(self.package_location)
        root_package_path = Path(root_package.__file__).parent  # type: ignore[union-attr]

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


@dataclass()
class Site(BaseNode["Site"]):
    """The top of a Storytime catalog.

    The site contains the organized collections of stories, with
    logic to render to disk.
    """

    items: dict[str, "Section"] = field(default_factory=dict)
    static_dir: Path | None = None

    def __post_init__(self) -> None:
        """Look for a static dir and assign it if present."""
        from storytime import PACKAGE_DIR

        sd = PACKAGE_DIR / "static"
        if sd.exists():
            self.static_dir = sd

    def find_path(self, path: str) -> Site | Section | Subject | Story | None:
        """Given a dotted path, traverse to the object."""
        current: Site | Section | Subject | Story | None = self
        segments = path.split(".")[1:]
        for segment in segments:
            if current is not None:
                current = current.items.get(segment)  # type: ignore[attr-defined, assignment]
        return current


@dataclass()
class Section(BaseNode["Section"]):
    """A grouping of stories, such as ``Views``."""

    parent: Site | None = None
    items: dict[str, "Subject"] = field(default_factory=dict)


@dataclass()
class Subject(BaseNode["Subject"]):
    """The component that a group of stories or variants is about."""

    parent: Section | None = None
    component: type | Callable | None = None
    stories: list["Story"] = field(default_factory=list)


@dataclass()
class Story:
    """One way to look at a component."""

    component: type | Callable | None = None
    kind: type | None = None
    parent: Subject = field(init=False)
    props: dict[str, Any] = field(default_factory=dict)
    title: str | None = None
    template: object | None = None

    def post_update(self, parent: Subject):
        """The parent calls this after construction.

        We do this as a convenience, so authors don't have to put a bunch
        of attributes in their stories.

        Args:
            parent: The Section that is the parent in the tree.

        Returns:
            The updated Story.
        """
        self.parent = parent
        if self.component is None and self.parent.component:
            self.component = self.parent.component
        if self.title is None:
            if self.parent.title:
                self.title = self.parent.title + " Story"
            else:
                self.title = self.parent.package_path
        return self

    @property
    def instance(self) -> object | None:
        """Construct the component instance related to this story."""
        if self.component:
            return self.component(**self.props)

        return None

    @property
    def vdom(self) -> object:
        """Generate a VDOM for the usage in this story."""
        if self.component:
            # We ignore the template if we are given a component and
            # instead construct a template.
            return self.instance
        elif self.template:
            return self.template
        else:
            raise ValueError("Could not generate VDOM for story.")
