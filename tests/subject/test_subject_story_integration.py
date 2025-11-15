"""Integration tests for Story.post_update() with Subject."""

from dataclasses import dataclass

from storytime.story import Story
from storytime.subject import Subject


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
