from dataclasses import dataclass

from storytime.components.layout import Layout
from tdom import html, Node


@dataclass
class IndexView:
    def __call__(self) -> Node:
        return html(t"""\
<{Layout} title="Components">
<main>
<p>Welcome to Storytime. Choose a component on the left.</p>
</main>
<//>
""")


#         return html('''\n
# <{Layout} title="Components">
# <main>
# <p>Welcome to Storytime. Choose a component on the left.</p>
# </main>
# </>
# ''')
