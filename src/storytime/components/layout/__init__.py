from dataclasses import dataclass

from tdom import html, Node
from storytime import Site
from storytime.components.sections_listing import SectionsListing


@dataclass
class Layout:
    title: str
    children: list[Node]
    site: Site

    def __call__(self) -> Node:
        sections = self.site.items.values()
        return html(t'''\
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Hello Bulma!</title>
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
        {self.children}
      </div>
  </div>
</section>
</body>
</html>
''')
