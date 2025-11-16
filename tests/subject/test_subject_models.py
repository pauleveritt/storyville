"""Test the Subject model."""

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
    assert subject.items == []


def test_subject_with_parent() -> None:
    """Test Subject with parent section."""
    section = Section(title="Components")
    subject = Subject(title="Heading", parent=section)
    assert subject.parent is section


def test_subject_with_target() -> None:
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
    subject = Subject(title="Heading", items=[story1, story2])

    assert len(subject.items) == 2
    assert subject.items[0] is story1
    assert subject.items[1] is story2


def test_story_inherits_target_from_subject() -> None:
    """Test Story inherits target from Subject via post_update()."""

    @dataclass
    class MyComponent:
        name: str = "test"

    # Create Subject with target
    subject = Subject(title="Heading Component", target=MyComponent)
    subject.package_path = ".components.heading"

    # Create Story without target
    story = Story()
    story.post_update(parent=subject)

    # Verify Story inherited target from Subject
    assert story.target is MyComponent
    assert story.parent is subject


def test_story_generates_title_from_subject() -> None:
    """Test Story generates title from Subject via post_update()."""

    @dataclass
    class AnotherComponent:
        label: str = "default"

    # Create Subject with target and title
    subject = Subject(title="Button Component", target=AnotherComponent)
    subject.package_path = ".components.button"

    # Create Story without title
    story = Story()
    story.post_update(parent=subject)

    # Verify Story generated title from Subject
    assert story.title == "Button Component Story"
    assert story.target is AnotherComponent
    assert story.parent is subject
