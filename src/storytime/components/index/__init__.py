from dataclasses import dataclass

from hopscotch import injectable
from viewdom.render import html, VDOM

from ..layout import Layout  # noqa


@injectable()
@dataclass
class IndexView:

    def __call__(self) -> VDOM:
        return html("""\n
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
