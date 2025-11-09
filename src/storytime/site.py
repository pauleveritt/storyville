"""Site class and site construction functionality."""

from dataclasses import dataclass, field
from importlib.resources import files
from pathlib import Path
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from storytime.story import BaseNode, Section, Subject, Story, TreeNode


@dataclass()
class Site:
    """The top of a Storytime catalog.

    The site contains the organized collections of stories, with
    logic to render to disk.
    """

    name: str = ""
    parent: None = None
    title: str | None = None
    context: object | None = None
    registry: object | None = None
    scannables: object | None = None
    singletons: object | None = None
    package_path: str = field(init=False, default="")
    items: dict[str, "Section"] = field(default_factory=dict)
    static_dir: Path | None = None

    def __post_init__(self) -> None:
        """Look for a static dir and assign it if present."""
        from storytime import PACKAGE_DIR

        sd = PACKAGE_DIR / "static"
        if sd.exists():
            self.static_dir = sd

    def post_update(
        self,
        parent: "BaseNode[Site] | None",
        tree_node: object,
    ) -> "Site":
        """The parent calls this after construction.

        We do this as a convenience, so authors don't have to put a bunch
        of attributes in their stories.

        Args:
            parent: The Site that is the parent in the tree.
            tree_node: The raw data from the scanning process.

        Returns:
            The updated Site.
        """
        from storytime import make_tree_node_registry

        self.parent = parent  # type: ignore[assignment]
        self.name = tree_node.name  # type: ignore[attr-defined]
        self.package_path = tree_node.this_package_location  # type: ignore[attr-defined]
        self.registry = make_tree_node_registry(
            context=self.context,
            parent=parent.registry if parent else None,  # type: ignore[attr-defined]
            registry=self.registry,
            scannables=self.scannables,  # type: ignore[arg-type]
            singletons=self.singletons,  # type: ignore[arg-type]
        )
        if self.title is None:
            self.title = self.package_path
        return self

    def find_path(self, path: str) -> "Site | Section | Subject | Story | None":
        """Given a dotted path, traverse to the object."""

        current: Site | Section | Subject | Story | None = self
        segments = path.split(".")[1:]
        for segment in segments:
            if current is not None:
                current = current.items.get(segment)  # type: ignore[attr-defined, assignment]
        return current


def make_site(package_location: str) -> Site:
    """Create a site with a populated tree.

    This is called from the CLI with a package-name path such
    as ``examples.minimal`` which is the root of a Storytime tree.

    Args:
        package_location: The top-level dotted-package-name of the root.

    Returns:
        A populated site.
    """
    from storytime.story import Section, Subject, TreeNode

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
    site: Site | None = None
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
