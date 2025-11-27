"""Site class for top-level catalog organization."""

from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from tdom import Node

from storytime.nodes import BaseNode

if TYPE_CHECKING:
    from storytime.section import Section


@dataclass
class Site(BaseNode["Site"]):
    """The top of a Storytime catalog.

    The site contains the organized collections of stories, with
    logic to render to disk.
    """

    parent: None = None
    items: dict[str, Section] = field(default_factory=dict)
    static_dir: Path | None = None
    themed_layout: Callable[..., Node] | None = None

    def __post_init__(self) -> None:
        """Look for a static dir and assign it if present."""
        from storytime import PACKAGE_DIR

        sd = PACKAGE_DIR / "components" / "layout" / "static"
        if sd.exists():
            self.static_dir = sd
