"""Integrate example testing into the main suite."""

from __future__ import annotations

from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name
from tdom import Element

from storytime import make_site
from storytime.section import Section
from storytime.section.views import SectionView
from storytime.story import Story
from storytime.story.views import StoryView
from storytime.subject import Subject
from storytime.subject.views import SubjectView


def test_complete_example_structure() -> None:
    """Test the complete example Site/Section/Subject hierarchy."""
    site = make_site("examples.complete")

    # Verify Site has title
    assert site.title == "Complete Example"

    # Traverse to Section using structural pattern matching
    match site.items.get("components"):
        case Section() as section:
            assert section.title == "Components Collection"
            assert section.description == "A collection of component examples with all optional fields populated"
            assert section.parent is site

            # Traverse to Subject
            match section.items.get("button"):
                case Subject() as subject:
                    assert subject.title == "Button Component"
                    assert subject.description == "A button component demonstrating all optional Story field variations"
                    assert subject.parent is section
                    assert subject.target is not None

                    # Verify 3 stories exist
                    assert len(subject.items) == 3
                case _:
                    raise AssertionError("Expected Subject for button")
        case _:
            raise AssertionError("Expected Section for components")


def test_complete_example_all_fields() -> None:
    """Test that all optional fields are populated on all models."""
    site = make_site("examples.complete")

    # Site fields
    assert site.title is not None

    # Section fields
    section = site.items["components"]
    assert isinstance(section, Section)
    assert section.title is not None
    assert section.description is not None

    # Subject fields
    subject = section.items["button"]
    assert isinstance(subject, Subject)
    assert subject.title is not None
    assert subject.description is not None
    assert subject.target is not None

    # Story fields - check all three stories
    assert len(subject.items) == 3

    # Story 1: Minimal (props only)
    story1 = subject.items[0]
    assert isinstance(story1, Story)
    assert story1.props == {"text": "Click Me", "variant": "primary"}
    assert story1.target is not None  # Inherited from Subject

    # Story 2: Custom title and description
    story2 = subject.items[1]
    assert isinstance(story2, Story)
    assert story2.title == "Secondary Action Button"
    assert story2.description == "A button with secondary styling and custom metadata"
    assert story2.props == {"text": "Learn More", "variant": "secondary"}

    # Story 3: Different props
    story3 = subject.items[2]
    assert isinstance(story3, Story)
    assert story3.props == {"text": "Cancel", "variant": "danger"}


def test_complete_example_story_variations() -> None:
    """Test the 3 Story patterns in complete example."""
    site = make_site("examples.complete")
    section = site.items["components"]
    subject = section.items["button"]

    # Pattern 1: Props only (minimal)
    story1 = subject.items[0]
    assert story1.props is not None
    assert story1.target is not None
    # Render the component - instance is the component, need to call it
    component_instance1 = story1.instance
    assert component_instance1 is not None
    rendered1 = component_instance1()  # type: ignore[call-non-callable]
    assert isinstance(rendered1, Element)
    button1 = get_by_tag_name(rendered1, "button")
    assert get_text_content(button1) == "Click Me"
    assert button1.attrs.get("class") == "primary"

    # Pattern 2: Story with custom title and description
    story2 = subject.items[1]
    assert story2.title == "Secondary Action Button"
    assert story2.description is not None
    component_instance2 = story2.instance
    assert component_instance2 is not None
    rendered2 = component_instance2()  # type: ignore[call-non-callable]
    assert isinstance(rendered2, Element)
    button2 = get_by_tag_name(rendered2, "button")
    assert get_text_content(button2) == "Learn More"
    assert button2.attrs.get("class") == "secondary"

    # Pattern 3: Different props for same component
    story3 = subject.items[2]
    component_instance3 = story3.instance
    assert component_instance3 is not None
    rendered3 = component_instance3()  # type: ignore[call-non-callable]
    assert isinstance(rendered3, Element)
    button3 = get_by_tag_name(rendered3, "button")
    assert get_text_content(button3) == "Cancel"
    assert button3.attrs.get("class") == "danger"


def test_complete_example_views() -> None:
    """Test rendering views for Section, Subject, and Story."""
    site = make_site("examples.complete")
    section = site.items["components"]
    subject = section.items["button"]

    # Test SectionView
    section_view = SectionView(section=section)
    section_result = section_view()
    assert isinstance(section_result, Element)
    section_h1 = get_by_tag_name(section_result, "h1")
    assert get_text_content(section_h1) == "Components Collection"

    # Test SubjectView
    subject_view = SubjectView(subject=subject)
    subject_result = subject_view()
    assert isinstance(subject_result, Element)
    subject_h1 = get_by_tag_name(subject_result, "h1")
    assert get_text_content(subject_h1) == "Button Component"

    # Test StoryView for one story (default layout)
    story = subject.items[0]
    story_view = StoryView(story=story)
    story_result = story_view()
    assert isinstance(story_result, Element)
    # Verify the story view contains the component
    paragraphs = query_all_by_tag_name(story_result, "p")
    assert len(paragraphs) > 0


def test_complete_example_field_inheritance() -> None:
    """Test field inheritance patterns in complete example."""
    site = make_site("examples.complete")
    section = site.items["components"]
    subject = section.items["button"]

    # All stories should have inherited target from Subject
    for story in subject.items:
        assert story.target is not None
        assert story.parent is subject

    # Story 1: No explicit title, should get auto-generated
    story1 = subject.items[0]
    assert story1.title is not None  # Auto-generated from Subject

    # Story 2: Explicit title should be preserved
    story2 = subject.items[1]
    assert story2.title == "Secondary Action Button"

    # Story 3: No explicit title, should get auto-generated
    story3 = subject.items[2]
    assert story3.title is not None  # Auto-generated from Subject
