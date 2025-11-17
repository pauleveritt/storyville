"""DebugView for rendering the Debug page."""

from dataclasses import dataclass

from tdom import Node, html

from storytime.components.layout import Layout
from storytime.site.models import Site


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

    site: Site

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
    This page provides debug information about the site structure.
  </p>
  <h2>Site Details</h2>
  <ul>
    <li><strong>Title:</strong> {self.site.title}</li>
    <li><strong>Sections:</strong> {len(self.site.items)}</li>
  </ul>
</div>""")

        # Wrap content in Layout with Debug title
        return html(t"""\
<{Layout} view_title="Debug" site={self.site} depth={0}>
{content}
</{Layout}>""")
