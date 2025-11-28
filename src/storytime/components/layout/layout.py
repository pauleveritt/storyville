"""Layout component providing HTML structure for all views."""

from dataclasses import dataclass

from tdom import Element, Fragment, Node, html

from storytime.components.aside.aside import LayoutAside
from storytime.components.footer.footer import LayoutFooter
from storytime.components.header.header import LayoutHeader
from storytime.components.main.main import LayoutMain
from storytime.site.models import Site


@dataclass
class Layout:
    """Layout component wrapping view content with HTML structure.

    Provides consistent HTML boilerplate (html, head, body) for all views,
    with configurable page titles and content insertion via a main element.
    """

    view_title: str | None
    site: Site
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

        # Calculate relative path to static assets based on depth
        # Static assets from layout component use storytime_static/ prefix
        # depth=0: site root or section ({section}/index.html) -> ../storytime_static/
        # depth=1: subject ({section}/{subject}/index.html) -> ../../storytime_static/
        # depth=2: story ({section}/{subject}/story-{idx}/index.html) -> ../../../storytime_static/
        static_prefix = "../" * (self.depth + 1)
        stylesheet_path = f"{static_prefix}storytime_static/components/layout/static/pico-main.css"
        pico_docs_path = f"{static_prefix}storytime_static/components/layout/static/pico-docs.css"
        storytime_css_path = f"{static_prefix}storytime_static/components/layout/static/storytime.css"
        ws_script_path = f"{static_prefix}storytime_static/components/layout/static/ws.js"
        favicon_path = f"{static_prefix}storytime_static/components/layout/static/favicon.svg"

        return html(t'''\
<!DOCTYPE html>
<html lang="EN">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title_text}</title>
    <link rel="icon" type="image/svg+xml" href="{favicon_path}" />
    <link rel="stylesheet" href="{stylesheet_path}" />
    <link rel="stylesheet" href="{pico_docs_path}" />
    <link rel="stylesheet" href="{storytime_css_path}" />
    <script src="{ws_script_path}"></script>
</head>
<body>
<{LayoutHeader} site_title={self.site.title} depth={self.depth} />
<{LayoutAside} sections={self.site.items} current_path={self.current_path} cached_navigation={self.cached_navigation} />
<{LayoutMain} current_path={self.current_path}>{self.children}</{LayoutMain}>
<{LayoutFooter} year={2025} text={"Storytime"} />
</body>
</html>
''')
