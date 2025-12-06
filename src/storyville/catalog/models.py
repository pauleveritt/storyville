"""Catalog class for top-level catalog organization."""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from tdom import Node

from storyville.nodes import BaseNode

if TYPE_CHECKING:
    from storyville.section import Section


@dataclass
class Catalog(BaseNode["Catalog"]):
    """The top of a Storyville catalog.

    The catalog contains the organized collections of stories, with
    logic to render to disk.
    """

    parent: None = None
    items: dict[str, Section] = field(default_factory=dict)
    themed_layout: Callable[..., Node] | None = None
