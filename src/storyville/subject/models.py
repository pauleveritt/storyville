"""Subject class for representing components with stories."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from storyville.nodes import BaseNode

if TYPE_CHECKING:
    from storyville.models import Target
    from storyville.section import Section
    from storyville.story import Story


@dataclass
class Subject(BaseNode["Subject"]):
    """The component that a group of stories or variants is about."""

    parent: Section | None = None
    description: str | None = None
    target: Target | None = None
    items: list[Story] = field(default_factory=list)
