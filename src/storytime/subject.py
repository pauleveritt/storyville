"""Subject class for representing components with stories."""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable

from storytime.nodes import BaseNode

if TYPE_CHECKING:
    from storytime.section import Section
    from storytime.story import Story


@dataclass()
class Subject(BaseNode["Subject"]):
    """The component that a group of stories or variants is about."""

    parent: "Section | None" = None
    component: type | Callable | None = None
    stories: list["Story"] = field(default_factory=list)
