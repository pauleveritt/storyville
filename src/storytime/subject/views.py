"""SubjectView for rendering Subject instances."""


from dataclasses import dataclass

from tdom import Node, html

from storytime.subject.models import Subject
from storytime.site.models import Site
from storytime.components.layout import Layout


@dataclass
class SubjectView:
    """View for rendering a Subject with metadata and story cards.

    The view renders:
    - Subject title in h1
    - Target information if present
    - Parent navigation link
    - List of story cards (title + link) or empty state message

    The view satisfies the View Protocol by implementing __call__() -> Node.
    Tests use type guards to verify the result is an Element.
    """

    subject: Subject
    site: Site

    def __call__(self) -> Node:
        """Render the subject to a tdom Node.

        Returns:
            A tdom Node representing the rendered subject.
        """
        # Prepare target display
        target_name = "None"
        if self.subject.target is not None:
            target_name = getattr(self.subject.target, "__name__", str(type(self.subject.target).__name__))

        # Render stories or empty state
        if not self.subject.items:
            # Empty state - wrapped with Layout (depth=1 for subject pages)
            view_content = html(t"""\
<{Layout} view_title={self.subject.title} site={self.site} depth={1}>
<div>
<h1>{self.subject.title}</h1>
<p>Target: {target_name}</p>
<p>No stories defined for this component</p>
<a href="..">Parent</a>
</div>
</{Layout}>""")
        else:
            # Build story cards as a list - create individual li elements
            story_items = []
            for idx, story in enumerate(self.subject.items):
                # Use story title for link text and simple URL
                story_url = f"story-{idx}"
                story_items.append(html(t"<li><a href=\"{story_url}\">{story.title}</a></li>"))

            # Create the main content wrapped with Layout (depth=1 for subject pages)
            view_content = html(t"""\
<{Layout} view_title={self.subject.title} site={self.site} depth={1}>
<div>
<h1>{self.subject.title}</h1>
<p>Target: {target_name}</p>
<ul>
{story_items}
</ul>
<a href="..">Parent</a>
</div>
</{Layout}>""")

        return view_content
