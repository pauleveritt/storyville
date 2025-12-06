"""Promote component-driven-development with a browseable catalog.

Storyville is a system for component-driven-development (CDD.)
You write stories as you develop components, expressing all the variations.
You can then browse them in a web page, as well as use these stories in testing.
"""

from pathlib import Path

from storyville.catalog import Catalog, find_path, make_catalog
from storyville.nodes import BaseNode, TreeNode, get_certain_callable
from storyville.section import Section
from storyville.story import Story
from storyville.subject import Subject

PACKAGE_DIR = Path(__file__).resolve().parent

__all__ = [
    "BaseNode",
    "Catalog",
    "PACKAGE_DIR",
    "Section",
    "Story",
    "Subject",
    "TreeNode",
    "find_path",
    "get_certain_callable",
    "make_catalog",
]
