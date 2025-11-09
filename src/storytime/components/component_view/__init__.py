from dataclasses import dataclass

from tdom import html, Node

from ..layout import Layout  # noqa
from ... import Story


@dataclass
class ComponentView:
    story: Story

    def __call__(self) -> Node:
        description = "self.component_info.description"
        return html(t"""\n
<{Layout} title="Components">
<h2 class="component-title has-text-weight-bold is-size-3">{self.story.title}</h2>
<p class="subtitle">{description}</p>
</>
""")
