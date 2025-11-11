"""Story class for component-driven development."""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from storytime.subject import Subject


@dataclass()
class Story:
    """One way to look at a component."""

    component: type | Callable | None = None
    kind: type | None = None
    parent: "Subject" = field(init=False)
    props: dict[str, Any] = field(default_factory=dict)
    title: str | None = None
    template: object | None = None

    def post_update(self, parent: "Subject"):
        """The parent calls this after construction.

        We do this as a convenience, so authors don't have to put a bunch
        of attributes in their stories.

        Args:
            parent: The Section that is the parent in the tree.

        Returns:
            The updated Story.
        """
        self.parent = parent
        if self.component is None and self.parent.component:
            self.component = self.parent.component
        if self.title is None:
            if self.parent.title:
                self.title = self.parent.title + " Story"
            else:
                self.title = self.parent.package_path
        return self

    @property
    def instance(self) -> object | None:
        """Construct the component instance related to this story."""
        if self.component:
            return self.component(**self.props)

        return None

    @property
    def vdom(self) -> object:
        """Generate a VDOM for the usage in this story."""
        if self.component:
            # We ignore the template if we are given a component and
            # instead construct a template.
            return self.instance
        elif self.template:
            return self.template
        else:
            raise ValueError("Could not generate VDOM for story.")
