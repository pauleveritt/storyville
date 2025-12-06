"""Story class for component-driven development."""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable

from tdom import Element, Fragment, Node

from storyville.models import Target, Template

if TYPE_CHECKING:
    from storyville.subject import Subject

# Type aliases for assertion support
type AssertionCallable = Callable[[Element | Fragment], None]
type AssertionResult = tuple[str, bool, str | None]


@dataclass
class Story:
    """One way to look at a component."""

    target: Target | None = None
    parent: Subject | None = None
    props: dict[str, Any] = field(default_factory=dict)
    title: str | None = None
    description: str | None = None
    template: Template | None = None
    assertions: list[AssertionCallable] = field(default_factory=list)
    assertion_results: list[AssertionResult] = field(default_factory=list)
    name: str = ""
    resource_path: str = ""

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

        # Calculate name (story index in parent's items list)
        if self in parent.items:
            self.name = str(parent.items.index(self))

        # Calculate resource_path from parent
        self.resource_path = f"{parent.resource_path}/{self.name}"

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
            instance = self.target(**self.props)

            # If the instance is callable (has __call__), invoke it to get the Node
            if callable(instance):
                return instance()
            return instance

        return None
