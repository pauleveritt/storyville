from dataclasses import dataclass

from storytime.section.models import Section
from tdom import html, Node


@dataclass
class StoryListing:
    dotted_path: str
    story_id: str
    story_title: str

    def __call__(self) -> Node:
        title = self.dotted_path if self.story_title is None else self.story_title
        return html(
            t"<li><a href={f'{self.dotted_path}-{self.story_id}.html'}>{title}</a></li>"
        )


@dataclass
class SectionListing:
    section: Section

    def __call__(self) -> Node:
        # ci = self.component_info
        # dotted_path = self.component_info.dotted_path
        # stories = self.component_info.stories
        return html(t"""\
<li><a href={"fn"}>{self.section.title}</a>{"rendered_stories"}</li>
        """)


#         rendered_stories = html('''\n
# <ul class="stories">
# {[
#     html('<{StoryListing} dotted_path={story.dotted_path} story_id={story.story_id} story_title={story.title}  />')
#     for story in stories
# ]}
# </ul>
#         ''')
#         fn = f'{ci.dotted_path}.html'
#         return html('''\n
# <li><a href={fn}>{ci.dotted_path}</a>{rendered_stories}</li>
#         ''')


@dataclass
class SectionsListing:
    """Left sidebar when on the components page."""

    sections: list[Section]

    def __call__(self) -> Node:
        """Render the wrapper for the listing of each section."""
        return html(t"""
<ul>
  {[html(t"<{SectionListing} section={section} />") for section in self.sections]}
</ul>
        """)
