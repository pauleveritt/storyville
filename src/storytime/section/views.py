"""SectionView for rendering Section instances."""


from dataclasses import dataclass

from tdom import Node, html

from storytime.section.models import Section
from storytime.site.models import Site
from storytime.components.layout import Layout


@dataclass
class SectionView:
    """View for rendering a Section with title, description, and subject cards.

    The view renders:
    - Section title in h1
    - Description in p element if present
    - Parent navigation link
    - List of subject cards (title + link) or empty state message

    The view satisfies the View Protocol by implementing __call__() -> Node.
    Tests use type guards to verify the result is an Element.
    """

    section: Section
    site: Site

    def __call__(self) -> Node:
        """Render the section to a tdom Node.

        Returns:
            A tdom Node representing the rendered section.
        """
        # Conditionally create description paragraph
        description_p = (
            html(t"<p>{self.section.description}</p>")
            if self.section.description is not None
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

        # Create the main content for this view
        view_content = html(t"""<div>
<h1>{self.section.title}</h1>
{description_p}
{content}
<a href="..">Parent</a>
</div>""")

        # Wrap with Layout (depth=1 for section pages)
        layout = Layout(view_title=self.section.title, site=self.site, children=view_content, depth=1)
        return layout()
