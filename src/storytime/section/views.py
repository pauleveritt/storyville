"""SectionView for rendering Section instances."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from tdom import Node, html

from storytime.components.layout import Layout
from storytime.section.models import Section

if TYPE_CHECKING:
    from storytime.catalog.models import Catalog


@dataclass
class SectionView:
    """View for rendering a Section with title, description, and subject cards.

    The view renders:
    - Section title in h1
    - Description in p element if present
    - List of subject cards (title + link) or empty state message

    The view satisfies the View Protocol by implementing __call__() -> Node.
    Tests use type guards to verify the result is an Element.
    """

    section: Section
    site: Catalog
    resource_path: str = ""
    cached_navigation: str | None = None

    def __call__(self) -> Node:
        """Render the section to a tdom Node.

        Returns:
            A tdom Node representing the rendered section.
        """
        # Conditionally create description paragraph
        description_p = (
            html(t"<p>{self.section.description}</p>")
            if self.section.description
            else ""
        )

        # Conditionally render subjects or empty state
        if not self.section.items:
            # Empty state
            content = html(t"<p>No subjects defined for this section</p>")
        else:
            # Build subject cards as a list - create individual li elements
            subject_items = []
            for key, subject in self.section.items.items():
                # Use subject title for link text and key-based URL
                subject_url = key
                subject_items.append(html(t"<li><a href=\"{subject_url}\">{subject.title}</a></li>"))
            content = html(t"<ul>{subject_items}</ul>")

        # Create the main content for this view wrapped with Layout (depth=1 for section pages in subdirectories)
        view_content = html(t"""\
<{Layout} view_title={self.section.title} site={self.site} depth={1} resource_path={self.resource_path} cached_navigation={self.cached_navigation}>
<div>
<h1>{self.section.title}</h1>
{description_p}
{content}
</div>
</{Layout}>""")

        return view_content
