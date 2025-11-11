"""Section class for grouping stories."""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from storytime.nodes import BaseNode

if TYPE_CHECKING:
    from storytime.site import Site
    from storytime.subject import Subject


@dataclass()
class Section(BaseNode["Section"]):
    """A grouping of stories, such as ``Views``."""

    parent: "Site | None" = None
    items: dict[str, "Subject"] = field(default_factory=dict)
