"""Catalog helper functions."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from storyville.section import Section
    from storyville.story import Story
    from storyville.subject import Subject

from storyville.catalog.models import Catalog


def make_catalog(package_location: str) -> Catalog:
    """Create a catalog with a populated tree.

    This is called from the CLI with a package-name path such
    as ``examples.minimal`` which is the root of a Storyville tree.

    Args:
        package_location: The top-level dotted-package-name of the root.

    Returns:
        A populated catalog.
    """
    from storyville.nodes import TreeNode, get_package_path
    from storyville.section import Section
    from storyville.subject import Subject

    # Resolve the filesystem path to the package directory
    root_dir = get_package_path(package_location)

    # Get all the stories.py under here
    tree_nodes: list[TreeNode] = [
        TreeNode(
            package_location=package_location,
            stories_path=stories_path,
        )
        for stories_path in root_dir.rglob("stories.py")
    ]
    # First get the Catalog
    catalog: Catalog | None = None
    for tree_node in tree_nodes:
        match tree_node.called_instance:
            case Catalog() as found_catalog:
                catalog = found_catalog
                catalog.post_update(
                    parent=None,
                    tree_node=tree_node,
                )
    if catalog is None:
        raise ValueError(
            f"No Catalog instance was found under package '{package_location}'. "
            "Ensure a callable returning Catalog is defined in a stories.py at the package root."
        )

    # Now the sections
    for tree_node in tree_nodes:
        match tree_node.called_instance:
            case Section() as section:
                section.post_update(parent=catalog, tree_node=tree_node)
                catalog.items[section.name] = section

    # Now the subjects
    for tree_node in tree_nodes:
        match tree_node.called_instance:
            case Subject() as subject:
                parent = find_path(catalog, tree_node.parent_path)
                match parent:
                    case Section():
                        subject.post_update(parent=parent, tree_node=tree_node)
                        parent.items[subject.name] = subject
                        for story in subject.items:
                            story.post_update(subject)

    return catalog


def find_path(
    catalog: Catalog, path: str
) -> Catalog | Section | Subject | Story | None:
    """Given a dotted path, traverse to the object.

    Args:
        catalog: The Catalog to traverse from.
        path: A dotted path like "." or ".section" or ".section.subject".

    Returns:
        The found node, or None if not found.
    """

    current: Catalog | Section | Subject | Story | None = catalog
    segments = path.split(".")[1:]
    for segment in segments:
        if current is not None:
            current = current.items.get(segment)  # type: ignore[attr-defined, assignment]
    return current
