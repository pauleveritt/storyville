"""CatalogView for rendering Catalog instances."""

from dataclasses import dataclass

from tdom import Node, html

from storyville.components.layout import Layout
from storyville.catalog.models import Catalog


@dataclass
class CatalogView:
    """View for rendering a Catalog with title and section cards.

    The view renders:
    - Catalog title in h1
    - List of section cards with:
      - Section title as a link
      - Section description (if present)
      - Subject count
    - Empty state message when no sections

    The view does NOT render a parent link since Catalog is the root node.
    The view satisfies the View Protocol by implementing __call__() -> Node.
    Tests use type guards to verify the result is an Element.
    """

    catalog: Catalog
    cached_navigation: str | None = None

    def __call__(self) -> Node:
        """Render the catalog to a tdom Node.

        Returns:
            A tdom Node representing the rendered catalog.
        """
        # Conditionally render sections or empty state
        if not self.catalog.items:
            # Empty state
            content = html(t"<p>No sections defined for this catalog</p>")
        else:
            # Build section cards as a list - create individual li elements
            section_items = []
            for key, section in self.catalog.items.items():
                # Use section title for link text and /{key} URL pattern
                section_url = f"/{key}"

                # Calculate subject count
                subject_count = len(section.items)
                subject_text = "subject" if subject_count == 1 else "subjects"
                count_display = f"({subject_count} {subject_text})"

                # Build the section item with optional description
                if section.description is not None:
                    section_items.append(
                        html(t"""
<li>
  <a href=\"{section_url}\">{section.title}</a>
  <p>{section.description}</p>
  <span>{count_display}</span>
</li>""")
                    )
                else:
                    section_items.append(
                        html(t"""
<li>
  <a href=\"{section_url}\">{section.title}</a>
  <span>{count_display}</span>
</li>""")
                    )

            content = html(t"<ul>{section_items}</ul>")

        # Create the main content for this view
        # Note: Layout still uses 'site' parameter name for backward compatibility
        view_content = html(t"""\
<{Layout} view_title="Home" site={self.catalog} depth={0} cached_navigation={self.cached_navigation}>
<div>
<h1>{self.catalog.title}</h1>
{content}
</div>
</{Layout}>""")

        return view_content
