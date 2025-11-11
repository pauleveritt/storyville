"""Promote component-driven-development with a browseable catalog.

Storytime is a system for component-driven-development (CDD.)
You write stories as you develop components, expressing all the variations.
You can then browse them in a web page, as well as use these stories in testing.
"""

from pathlib import Path

from storytime.nodes import BaseNode
from storytime.nodes import TreeNode
from storytime.section import Section
from storytime.site import Site
from storytime.site import make_site
from storytime.story import Story
from storytime.story import Subject
from storytime.utils import get_certain_callable

__all__ = [
    "BaseNode",
    "Section",
    "Site",
    "Story",
    "Subject",
    "TreeNode",
    "get_certain_callable",
    "make_site",
]

PACKAGE_DIR = Path(__file__).resolve().parent
