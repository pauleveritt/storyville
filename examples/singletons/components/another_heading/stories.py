"""The subject for this Another Heading component."""
from dataclasses import dataclass

from viewdom import VDOM
from viewdom.render import html

from storytime import Story
from storytime import Subject


@dataclass()
class Config:
    """A configuration service."""

    punctuation: str = "..."


def Heading(config: Config) -> VDOM:
    """Make a heading that has punctuation from the config."""
    return html("<div>Howdy {config.punctuation}</div>")


def this_subject() -> Subject:
    """Let's make a Storytime subject for this Heading component."""
    assert Heading
    return Subject(
        title="Heading",
        stories=[
            Story(
                component=Heading,
                singletons=[Config()],
            )
        ],
    )
