"""The index page for the Storytime UI."""
from viewdom import html

from storytime import Story
from storytime import Subject


def this_subject() -> Subject:
    """Let's make a Storytime subject for this Index component."""
    return Subject(
        title="Index Page",
        stories=[
            Story(
                template=html("<div>Index Page, bazinga</div>")
            ),
        ],
    )
