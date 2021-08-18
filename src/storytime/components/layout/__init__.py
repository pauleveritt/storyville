from dataclasses import dataclass

from hopscotch import injectable
# from storytime.components.components_listing import ComponentsListing
from viewdom.render import VDOM, html


def ComponentsListing() -> VDOM:
    return html("<div>COMPONENTS LISTING 99</div>")


@injectable()
@dataclass
class Layout:
    title: str
    children: VDOM

    def __call__(self) -> VDOM:
        assert ComponentsListing
        return html('''\n
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Hello Bulma!</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.1/css/bulma.min.css" />
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
            Components
          </p>
          <{ComponentsListing} />
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
