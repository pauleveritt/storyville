"""Story class for component-driven development."""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from tdom import Node

from storytime.models import Target, Template

if TYPE_CHECKING:
    from storytime.subject import Subject


@dataclass
class Story:
    """One way to look at a component."""

    target: Target | None = None
    parent: Subject | None = None
    props: dict[str, Any] = field(default_factory=dict)
    title: str | None = None
    description: str | None = None
    template: Template | None = None

    def post_update(self, parent: Subject):
        """The parent calls this after construction.

        We do this as a convenience, so authors don't have to put a bunch
        of attributes in their stories.

        Args:
            parent: The Subject that is the parent in the tree.

        Returns:
            The updated Story.
        """
        self.parent = parent
        if self.target is None and self.parent.target:
            self.target = self.parent.target
        if self.title is None:
            if self.parent.title:
                self.title = self.parent.title + " Story"
            else:
                self.title = self.parent.package_path
        return self

    @property
    def instance(self) -> Node | None:
        """Construct the component instance related to this story.

        Returns:
            Node instance from target, or None if no target exists.
        """
        if self.target:
            return self.target(**self.props)

        return None
