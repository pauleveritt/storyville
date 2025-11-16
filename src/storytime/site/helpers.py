"""Site helper functions."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from storytime.section import Section
    from storytime.story import Story
    from storytime.subject import Subject

from storytime.site.models import Site


def make_site(package_location: str) -> Site:
    """Create a site with a populated tree.

    This is called from the CLI with a package-name path such
    as ``examples.minimal`` which is the root of a Storytime tree.

    Args:
        package_location: The top-level dotted-package-name of the root.

    Returns:
        A populated site.
    """
    from storytime.nodes import TreeNode, get_package_path
    from storytime.section import Section
    from storytime.subject import Subject

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
    # First get the Site
    site: Site | None = None
    for tree_node in tree_nodes:
        match tree_node.called_instance:
            case Site() as found_site:
                site = found_site
                site.post_update(
                    parent=None,
                    tree_node=tree_node,
                )
    if site is None:
        raise ValueError(
            f"No Site instance was found under package '{package_location}'. "
            "Ensure a callable returning Site is defined in a stories.py at the package root."
        )

    # Now the sections
    for tree_node in tree_nodes:
        match tree_node.called_instance:
            case Section() as section:
                section.post_update(parent=site, tree_node=tree_node)
                site.items[section.name] = section

    # Now the subjects
    for tree_node in tree_nodes:
        match tree_node.called_instance:
            case Subject() as subject:
                parent = find_path(site, tree_node.parent_path)
                match parent:
                    case Section():
                        subject.post_update(parent=parent, tree_node=tree_node)
                        parent.items[subject.name] = subject
                        for story in subject.items:
                            story.post_update(subject)

    return site


def find_path(site: Site, path: str) -> Site | Section | Subject | Story | None:
    """Given a dotted path, traverse to the object.

    Args:
        site: The Site to traverse from.
        path: A dotted path like "." or ".section" or ".section.subject".

    Returns:
        The found node, or None if not found.
    """

    current: Site | Section | Subject | Story | None = site
    segments = path.split(".")[1:]
    for segment in segments:
        if current is not None:
            current = current.items.get(segment)  # type: ignore[attr-defined, assignment]
    return current
