"""LayoutHeader component for site branding and navigation."""

from dataclasses import dataclass

from tdom import Node, html


@dataclass
class LayoutHeader:
    """Header component with site branding and main navigation.

    Renders header element with container, site title in hgroup,
    and navigation links (Home, About, Debug).
    """

    site_title: str
    depth: int = 0

    def __call__(self) -> Node:
        """Render the header to a tdom Node.

        Returns:
            A tdom Node representing the header element.
        """
        return html(t"""\
<header>
  <div class="container">
    <hgroup>
      <p><strong>{self.site_title}</strong></p>
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
""")
