"""AboutView for rendering the About page."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from tdom import Node, html

from storytime.components.layout import Layout

if TYPE_CHECKING:
    from storytime.catalog.models import Catalog


@dataclass
class AboutView:
    """View for rendering the About page.

    The view renders:
    - About heading
    - Static HTML content describing the project
    - Wrapped in Layout component with view_title="About"

    Uses depth=0 for root-level view.
    The view satisfies the View Protocol by implementing __call__() -> Node.
    """

    site: Catalog
    cached_navigation: str | None = None

    def __call__(self) -> Node:
        """Render the about page to a tdom Node.

        Returns:
            A tdom Node representing the rendered about page.
        """
        # Create the main content for this view
        content = html(t"""\
<div>
  <h1>About Storytime</h1>
  <p>
    Storytime is a static catalog generator for documentation and storytelling.
    It provides a clean, hierarchical structure for organizing content into
    sections, subjects, and stories.
  </p>
  <p>
    Built with modern Python and leveraging PicoCSS for beautiful,
    semantic HTML styling.
  </p>
</div>""")

        # Wrap content in Layout with About title
        return html(t"""\
<{Layout} view_title="About" site={self.site} depth={0} cached_navigation={self.cached_navigation}>
{content}
</{Layout}>""")
