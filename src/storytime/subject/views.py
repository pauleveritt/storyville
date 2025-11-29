"""SubjectView for rendering Subject instances."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from tdom import Node, html

from storytime.components.layout import Layout
from storytime.subject.models import Subject

if TYPE_CHECKING:
    from storytime.catalog.models import Catalog


@dataclass
class SubjectView:
    """View for rendering a Subject with metadata and story cards.

    The view renders:
    - Subject title in h1
    - Description in p element if present
    - Target information if present
    - Parent navigation link
    - List of story cards (title + link) or empty state message

    The view satisfies the View Protocol by implementing __call__() -> Node.
    Tests use type guards to verify the result is an Element.
    """

    subject: Subject
    site: Catalog
    cached_navigation: str | None = None

    def __call__(self) -> Node:
        """Render the subject to a tdom Node.

        Returns:
            A tdom Node representing the rendered subject.
        """
        # Conditionally create description paragraph
        description_p = (
            html(t"<p>{self.subject.description}</p>")
            if self.subject.description
            else ""
        )

        # Prepare target display
        target_name = "None"
        if self.subject.target is not None:
            target_name = getattr(self.subject.target, "__name__", str(type(self.subject.target).__name__))

        # Render stories or empty state
        if not self.subject.items:
            # Empty state - wrapped with Layout (depth=2 for subject pages)
            view_content = html(t"""\
<{Layout} view_title={self.subject.title} site={self.site} depth={2} cached_navigation={self.cached_navigation}>
<div>
<h1>{self.subject.title}</h1>
{description_p}
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

            # Create the main content wrapped with Layout (depth=2 for subject pages)
            view_content = html(t"""\
<{Layout} view_title={self.subject.title} site={self.site} depth={2} cached_navigation={self.cached_navigation}>
<div>
<h1>{self.subject.title}</h1>
{description_p}
<p>Target: {target_name}</p>
<ul>
{story_items}
</ul>
<a href="..">Parent</a>
</div>
</{Layout}>""")

        return view_content
