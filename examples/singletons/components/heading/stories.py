"""The subject for this Heading component."""
from dataclasses import dataclass

from viewdom import VDOM
from viewdom import html

from storytime import Story
from storytime import Subject


@dataclass()
class Config:
    """A configuration service."""

    punctuation: str = "!"


def Heading(config: Config) -> VDOM:
    """Make a heading that has punctuation from the config."""
    return html("<div>Hello {config.punctuation}</div>")


def this_subject() -> Subject:
    """Let's make a Storytime subject for this Heading component."""
    assert Heading
    return Subject(
        title="Heading",
        singletons=[Config()],
        stories=[
            Story(
                component=Heading,
            )
        ],
    )
