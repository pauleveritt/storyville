"""Section class for organizational grouping of subjects."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from storytime.nodes import BaseNode

if TYPE_CHECKING:
    from storytime.catalog import Catalog
    from storytime.subject import Subject


@dataclass
class Section(BaseNode["Section"]):
    """A grouping of subjects within a catalog.

    Sections provide organizational structure, containing multiple
    subjects with their stories. A section can have an optional
    description to explain its purpose.

    The Section inherits from BaseNode without overriding post_update(),
    using the inherited implementation for parent assignment, naming,
    and package path handling.
    """

    parent: Catalog | None = None
    description: str | None = None
    items: dict[str, Subject] = field(default_factory=dict)
