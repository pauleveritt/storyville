"""The index page for the Storytime UI."""

from storytime import Story
from storytime import Subject
from tdom import html


def this_subject() -> Subject:
    """Let's make a Storytime subject for this Index component."""
    return Subject(
        title="Index Page",
        items=[
            Story(template=lambda: html(t"<div>Index Page, bazinga</div>")),
        ],
    )
