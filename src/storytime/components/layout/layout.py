"""Layout component providing HTML structure for all views."""

from dataclasses import dataclass

from tdom import Element, Fragment, Node, html

from storytime.components.breadcrumbs import Breadcrumbs
from storytime.components.navigation_tree import NavigationTree
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
        # depth=0: site root or section ({section}/index.html) -> ../static/
        # depth=1: subject ({section}/{subject}/index.html) -> ../../static/
        # depth=2: story ({section}/{subject}/story-{idx}/index.html) -> ../../../static/
        static_prefix = "../" * (self.depth + 1)
        stylesheet_path = f"{static_prefix}static/pico-main.css"
        pico_docs_path = f"{static_prefix}static/pico-docs.css"
        storytime_css_path = f"{static_prefix}static/storytime.css"
        ws_script_path = f"{static_prefix}static/ws.js"

        return html(t'''\
<html lang="EN">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title_text}</title>
    <link rel="stylesheet" href="{stylesheet_path}" />
    <link rel="stylesheet" href="{pico_docs_path}" />
    <link rel="stylesheet" href="{storytime_css_path}" />
    <script src="{ws_script_path}"></script>
</head>
<body>
<header class="fixed">
  <div class="container">
    <hgroup>
      <p><strong>Storytime</strong></p>
    </hgroup>
    <nav>
      <ul>
        <li><a href="/" class="contrast">Home</a></li>
        <li><a href="/about" class="contrast">About</a></li>
        <li><a href="/debug" class="contrast">Debug</a></li>
      </ul>
    </nav>
  </div>
</header>
<div class="grid">
  <aside>
    <strong>Sections</strong>
    <{NavigationTree} sections={self.site.items} current_path={self.current_path} />
  </aside>
  <main>
    <{Breadcrumbs} current_path={self.current_path} />
    {self.children}
  </main>
</div>
<footer>
  <p style="text-align: center;">2025 Storytime</p>
</footer>
</body>
</html>
''')
