from dataclasses import dataclass

from tdom import html, Node


@dataclass
class IndexView:
    def __call__(self) -> Node:
        return html(t"""\
<html title="Components">
<main>
<p>Welcome to Storytime. Choose a component on the left.</p>
</main>
</html>
""")


#         return html('''\n
# <{Layout} title="Components">
# <main>
# <p>Welcome to Storytime. Choose a component on the left.</p>
# </main>
# </>
# ''')
