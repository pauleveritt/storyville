"""Test the Subject.items field."""

from dataclasses import dataclass

from storytime.section import Section
from storytime.story import Story
from storytime.subject import Subject


def test_subject_items_is_list_of_stories() -> None:
    """Test Subject.items field is list[Story]."""
    story1 = Story(title="Story 1")
    story2 = Story(title="Story 2")
    subject = Subject(title="Test Subject", items=[story1, story2])

    # Verify items is a list of Story instances
    assert isinstance(subject.items, list)
    assert len(subject.items) == 2
    assert all(isinstance(item, Story) for item in subject.items)


def test_subject_items_defaults_to_empty_list() -> None:
    """Test Subject.items defaults to empty list."""
    subject = Subject(title="Empty Subject")
    assert subject.items == []
    assert isinstance(subject.items, list)


def test_subject_items_can_be_populated() -> None:
    """Test Subject.items can be populated with Story instances."""
    story1 = Story(title="First Story")
    story2 = Story(title="Second Story")
    story3 = Story(title="Third Story")

    subject = Subject(title="Test Subject", items=[story1, story2, story3])

    assert len(subject.items) == 3
    assert subject.items[0] is story1
    assert subject.items[1] is story2
    assert subject.items[2] is story3


def test_subject_items_with_parent() -> None:
    """Test Subject.items works with parent relationship."""
    section = Section(title="Components")
    story = Story(title="Test Story")
    subject = Subject(title="Button", parent=section, items=[story])

    assert subject.parent is section
    assert len(subject.items) == 1
    assert subject.items[0] is story


def test_subject_items_with_target() -> None:
    """Test Subject.items works with target."""

    @dataclass
    class MyComponent:
        name: str = "test"

    story = Story(title="Component Story")
    subject = Subject(title="My Subject", target=MyComponent, items=[story])

    assert subject.target is MyComponent
    assert len(subject.items) == 1
