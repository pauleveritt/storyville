"""Test the Subject class."""

from dataclasses import dataclass

from storytime.section import Section
from storytime.story import Story
from storytime.subject import Subject


def test_subject_initialization() -> None:
    """Test Subject can be instantiated."""
    subject = Subject(title="Heading")
    assert subject.title == "Heading"
    assert subject.parent is None
    assert subject.target is None
    assert subject.stories == []


def test_subject_with_parent() -> None:
    """Test Subject with parent section."""
    section = Section(title="Components")
    subject = Subject(title="Heading", parent=section)
    assert subject.parent is section


def test_subject_with_component() -> None:
    """Test Subject with a target."""

    @dataclass
    class MyComponent:
        name: str = "test"

    subject = Subject(title="Heading", target=MyComponent)
    assert subject.target is MyComponent


def test_subject_with_stories() -> None:
    """Test Subject with stories."""
    story1 = Story(title="Default")
    story2 = Story(title="With Props")
    subject = Subject(title="Heading", stories=[story1, story2])

    assert len(subject.stories) == 2
    assert subject.stories[0] is story1
    assert subject.stories[1] is story2
