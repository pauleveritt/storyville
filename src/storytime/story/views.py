"""StoryView for rendering Story instances with dual modes."""

from dataclasses import dataclass

from tdom import Node, html

from storytime.components.layout import Layout
from storytime.site.models import Site
from storytime.story.models import Story


@dataclass
class StoryView:
    """View for rendering a Story with custom template or default layout.

    This view implements dual rendering modes:
    - Mode A (Custom Template): When story.template is not None, uses it for ALL rendering
    - Mode B (Default Layout): When story.template is None, renders a complete default layout

    The view satisfies the View Protocol by implementing __call__() -> Node.
    Tests use type guards to verify the result is an Element.
    """

    story: Story
    site: Site

    def __call__(self) -> Node:
        """Render the story to a tdom Node.

        Returns:
            A tdom Node representing the rendered story.
        """
        # Mode A: Custom template rendering
        if self.story.template is not None:
            return self.story.template()

        # Mode B: Default layout rendering wrapped with Layout (depth=2 for story pages)
        return html(t"""\
<{Layout} view_title={self.story.title} site={self.site} depth={2}>
<div>
<h1>{self.story.title}</h1>
<p>Props: <code>{str(self.story.props)}</code></p>
<div>
{self.story.instance}
</div>
<a href="..">Parent</a>
</div>
</{Layout}>""")
