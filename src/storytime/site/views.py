"""SiteView for rendering Site instances."""


from dataclasses import dataclass

from tdom import Node, html

from storytime.site.models import Site


@dataclass
class SiteView:
    """View for rendering a Site with title and section cards.

    The view renders:
    - Site title in h1
    - List of section cards (title + link) or empty state message

    The view does NOT render a parent link since Site is the root node.
    The view satisfies the View Protocol by implementing __call__() -> Node.
    Tests use type guards to verify the result is an Element.
    """

    site: Site

    def __call__(self) -> Node:
        """Render the site to a tdom Node.

        Returns:
            A tdom Node representing the rendered site.
        """
        # Conditionally render sections or empty state
        if not self.site.items:
            # Empty state
            content = html(t"<p>No sections defined for this site</p>")
        else:
            # Build section cards as a list - create individual li elements
            section_items = []
            for key, section in self.site.items.items():
                # Use section title for link text and key-based URL
                section_url = key
                section_items.append(html(t"<li><a href=\"{section_url}\">{section.title}</a></li>"))
            content = html(t"<ul>{section_items}</ul>")

        return html(t"""<div>
<h1>{self.site.title}</h1>
{content}
</div>""")
