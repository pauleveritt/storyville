from dataclasses import dataclass

from hopscotch import injectable
from viewdom.render import html
from viewdom.render import VDOM

from ..layout import Layout  # noqa
from ... import Story


@injectable()
@dataclass
class ComponentView:
    story: Story

    def __call__(self) -> VDOM:
        description = "self.component_info.description"
        return html('''\n
<{Layout} title="Components">
<h2 class="component-title has-text-weight-bold is-size-3">{self.story.title}</h2>
<p class="subtitle">{description}</p>
</>
''')
