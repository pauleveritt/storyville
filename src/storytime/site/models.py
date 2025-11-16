"""Site class for top-level catalog organization."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from storytime.nodes import BaseNode

if TYPE_CHECKING:
    from storytime.section import Section


@dataclass()
class Site(BaseNode["Site"]):
    """The top of a Storytime catalog.

    The site contains the organized collections of stories, with
    logic to render to disk.
    """

    parent: None = None
    items: dict[str, Section] = field(default_factory=dict)
    static_dir: Path | None = None

    def __post_init__(self) -> None:
        """Look for a static dir and assign it if present."""
        from storytime import PACKAGE_DIR

        sd = PACKAGE_DIR / "static"
        if sd.exists():
            self.static_dir = sd

    def post_update(
        self,
        parent: BaseNode["Site"] | None,
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

        self.parent = parent  # type: ignore[assignment]
        self.name = tree_node.name  # type: ignore[attr-defined]
        self.package_path = tree_node.this_package_location  # type: ignore[attr-defined]
        if self.title is None:
            self.title = self.package_path
        return self
