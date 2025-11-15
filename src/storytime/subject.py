"""Subject class for representing components with stories."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from storytime.nodes import BaseNode

if TYPE_CHECKING:
    from storytime.models import Target
    from storytime.section import Section
    from storytime.story import Story


@dataclass()
class Subject(BaseNode["Subject"]):
    """The component that a group of stories or variants is about."""

    parent: Section | None = None
    target: Target | None = None
    stories: list[Story] = field(default_factory=list)
