"""Layout component providing HTML structure for all views."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from tdom import Element, Fragment, Node, html

from storyville.components.aside.aside import LayoutAside
from storyville.components.footer.footer import LayoutFooter
from storyville.components.header.header import LayoutHeader
from storyville.components.main.main import LayoutMain
from storyville.utils import rewrite_static_paths

if TYPE_CHECKING:
    from storyville.catalog.models import Catalog


@dataclass
class Layout:
    """Layout component wrapping view content with HTML structure.

    Provides consistent HTML boilerplate (html, head, body) for all views,
    with configurable page titles and content insertion via a main element.

    FontAwesome Integration:
    - FontAwesome Free v6.7.1 is vendored directly in src/storyville/vendor/fontawesome/static/
    - The static asset system automatically copies these files to the output directory
    - FontAwesome CSS is loaded after Pico CSS to ensure proper icon rendering

    Sidebar Toggle:
    - sidebar.js provides collapse/expand functionality with localStorage persistence
    - Loaded after ws.js to ensure proper initialization order

    Tree Expansion:
    - tree-expand.js automatically expands navigation tree based on current URL
    - Loaded after sidebar.js to ensure proper initialization order
    """

    view_title: str | None
    site: Catalog
    children: Element | Fragment | Node | None
    depth: int = 0
    resource_path: str = ""
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
        result = html(t"""\
<!DOCTYPE html>
<html lang="EN">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title_text}</title>
    <link rel="icon" type="image/svg+xml" href="static/components/layout/static/favicon.svg" />
    <link rel="stylesheet" href="static/components/layout/static/pico-main.css" />
    <link rel="stylesheet" href="static/components/layout/static/pico-docs.css" />
    <link rel="stylesheet" href="static/components/layout/static/storyville.css" />
    <link rel="stylesheet" href="static/vendor/fontawesome/static/all.min.css" />
    <script type="module" src="static/components/layout/static/ws.mjs"></script>
    <script type="module" src="static/components/layout/static/sidebar.mjs"></script>
    <script type="module" src="static/components/layout/static/tree-expand.mjs"></script>
</head>
<body>
<{LayoutHeader} site_title={self.site.title} depth={self.depth} />
<{LayoutAside} sections={self.site.items} resource_path={self.resource_path} cached_navigation={self.cached_navigation} />
<{LayoutMain} resource_path={self.resource_path}>{self.children}</{LayoutMain}>
<{LayoutFooter} year={2025} text={"Storyville"} />
</body>
</html>
""")

        # Rewrite static/ paths to be relative to page location
        return rewrite_static_paths(result, depth=self.depth)
