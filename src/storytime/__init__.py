"""Promote component-driven-development with a browseable catalog.

Storytime is a system for component-driven-development (CDD.)
You write stories as you develop components, expressing all the variations.
You can then browse them in a web page, as well as use these stories in testing.
"""

from importlib.resources import files
from inspect import getmembers, isfunction
from pathlib import Path
from types import ModuleType
from typing import cast, get_type_hints

# Import all node classes from story module
from storytime.story import BaseNode as BaseNode
from storytime.story import Section as Section
from storytime.story import Site as Site
from storytime.story import Story as Story
from storytime.story import Subject as Subject
from storytime.story import TreeNode as TreeNode

PACKAGE_DIR = Path(__file__).resolve().parent


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
