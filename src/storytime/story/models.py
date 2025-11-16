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
            import inspect

            # Check if the target accepts a 'story' parameter
            sig = inspect.signature(self.target)
            if 'story' in sig.parameters:
                instance = self.target(story=self, **self.props)
            else:
                instance = self.target(**self.props)

            # If the instance is callable (has __call__), invoke it to get the Node
            if callable(instance):
                return instance()
            return instance

        return None
