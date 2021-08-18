from storytime import Subject
from . import ComponentView  # noqa
from ... import Story


def these_stories() -> Subject:
    return Subject(
        title="Component View",
        stories=[
            Story(
                component=ComponentView,
            )
        ]
    )
