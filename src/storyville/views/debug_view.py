"""DebugView for rendering the Debug page."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from tdom import Node, html

from storyville.components.layout import Layout

if TYPE_CHECKING:
    from storyville.catalog.models import Catalog


@dataclass
class DebugView:
    """View for rendering the Debug page.

    The view renders:
    - Debug heading
    - Static HTML content showing debug information
    - Wrapped in Layout component with view_title="Debug"

    Uses depth=0 for root-level view.
    The view satisfies the View Protocol by implementing __call__() -> Node.
    """

    site: Catalog
    cached_navigation: str | None = None

    def __call__(self) -> Node:
        """Render the debug page to a tdom Node.

        Returns:
            A tdom Node representing the rendered debug page.
        """
        # Create the main content for this view
        content = html(t"""\
<div>
  <h1>Debug Information</h1>
  <p>
    This page provides debug information about the catalog structure.
  </p>
  <h2>Catalog Details</h2>
  <ul>
    <li><strong>Title:</strong> {self.site.title}</li>
    <li><strong>Sections:</strong> {len(self.site.items)}</li>
  </ul>
</div>""")

        # Wrap content in Layout with Debug title
        return html(t"""\
<{Layout} view_title="Debug" site={self.site} depth={0} cached_navigation={self.cached_navigation}>
{content}
</{Layout}>""")
