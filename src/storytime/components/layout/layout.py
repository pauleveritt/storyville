"""Layout component providing HTML structure for all views."""

from dataclasses import dataclass

from tdom import Element, Fragment, Node, html

from storytime.components.sections_listing import SectionsListing
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

        # Get sections for sidebar
        sections = self.site.items.values()

        return html(t'''\
<html lang="EN">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title_text}</title>
    <link rel="stylesheet" href="../static/bulma.css" />
</head>
<body>
<nav class="navbar is-info" role="navigation" aria-label="main navigation">
  <div class="navbar-brand">
    <a class="navbar-item" href="/">
        Storytime
    </a>
  </div>

  <div id="navbarBasicExample" class="navbar-menu">
    <div class="navbar-start">
      <a class="navbar-item" href="/">
        Home
      </a>

      <a class="navbar-item" href="/">
        Components
      </a>
    </div>
  </div>
</nav>
<section class="section">
  <div class="columns">
      <div class="column is-one-quarter">
        <aside class="menu">
          <p class="menu-label">
            Sections
          </p>
          <{SectionsListing} sections={sections} />
        </aside>

      </div>
      <div class="column">
        <main>
          {self.children}
        </main>
      </div>
  </div>
</section>
</body>
</html>
''')
