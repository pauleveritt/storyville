"""Layout component providing HTML structure for all views."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from tdom import Element, Fragment, Node, html

from storytime.components.aside.aside import LayoutAside
from storytime.components.footer.footer import LayoutFooter
from storytime.components.header.header import LayoutHeader
from storytime.components.main.main import LayoutMain
from storytime.utils import rewrite_static_paths

if TYPE_CHECKING:
    from storytime.catalog.models import Catalog


@dataclass
class Layout:
    """Layout component wrapping view content with HTML structure.

    Provides consistent HTML boilerplate (html, head, body) for all views,
    with configurable page titles and content insertion via a main element.
    """

    view_title: str | None
    site: Catalog
    children: Element | Fragment | Node | None
    depth: int = 0
    current_path: str | None = None
    cached_navigation: str | None = None

    def __call__(self) -> Node:
        """Render the layout to a tdom Node.

        Returns:
            A tdom Node representing the complete HTML document.
        """
        # Build title with concatenation logic
        if self.view_title is not None:
            title_text = f"{self.view_title} - {self.site.title}"
        else:
            title_text = self.site.title

        # Use paths relative to this component file
        # static/ refers to the static folder in the output, with full nested path
        result = html(t'''\
<!DOCTYPE html>
<html lang="EN">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title_text}</title>
    <link rel="icon" type="image/svg+xml" href="static/components/layout/static/favicon.svg" />
    <link rel="stylesheet" href="static/components/layout/static/pico-main.css" />
    <link rel="stylesheet" href="static/components/layout/static/pico-docs.css" />
    <link rel="stylesheet" href="static/components/layout/static/storytime.css" />
    <script src="static/components/layout/static/ws.js"></script>
</head>
<body>
<{LayoutHeader} site_title={self.site.title} depth={self.depth} />
<{LayoutAside} sections={self.site.items} current_path={self.current_path} cached_navigation={self.cached_navigation} />
<{LayoutMain} current_path={self.current_path}>{self.children}</{LayoutMain}>
<{LayoutFooter} year={2025} text={"Storytime"} />
</body>
</html>
''')

        # Rewrite static/ paths to be relative to page location
        return rewrite_static_paths(result, depth=self.depth)
