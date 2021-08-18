from dataclasses import dataclass

from hopscotch import injectable
from viewdom.render import VDOM, html

from storytime import Section


@injectable()
@dataclass
class StoryListing:
    dotted_path: str
    story_id: str
    story_title: str

    def __call__(self) -> VDOM:
        title = self.dotted_path if self.story_title is None else self.story_title
        return html('<li><a href={f"{self.dotted_path}-{self.story_id}.html"}>{title}</a></li>')


@injectable()
@dataclass
class ComponentListing:
    sections: list[Section]

    def __call__(self) -> VDOM:
        ci = self.component_info
        dotted_path = self.component_info.dotted_path
        stories = self.component_info.stories
        rendered_stories = html('''\n
<ul class="stories">
{[
    html('<{StoryListing} dotted_path={story.dotted_path} story_id={story.story_id} story_title={story.title}  />')
    for story in stories
]}
</ul>
        ''')
        fn = f'{ci.dotted_path}.html'
        return html('''\n
<li><a href={fn}>{ci.dotted_path}</a>{rendered_stories}</li>
        ''')


@injectable()
@dataclass
class ComponentsListing:
    """ Left sidebar when on the components page """

    sections: list[Section]

    def __call__(self) -> VDOM:
        return html('''\n
<ul class="menu-list">
  {[
    html('<{ComponentListing} component_info={ci} />')
    for ci in self.component_infos.items
  ]}
</ul>
        ''')
