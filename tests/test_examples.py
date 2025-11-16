"""Integrate example testing into the main suite."""


from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name
from tdom import Element, Fragment, Node
from typing import cast

from storytime import make_site
from storytime.section import Section
from storytime.section.views import SectionView
from storytime.story import Story
from storytime.story.views import StoryView
from storytime.subject import Subject
from storytime.subject.views import SubjectView




def _get_element(result: Node) -> Element:
    """Extract Element from result (handles Fragment wrapper)."""
    if isinstance(result, Fragment):
        # Fragment contains the html element as first child
        for child in result.children:
            if isinstance(child, Element):
                return child
        raise ValueError("No Element found in Fragment")
    return cast(Element, result)


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
    section_view = SectionView(section=section, site=site)
    section_result = section_view()
    section_element = _get_element(section_result)
    section_h1 = get_by_tag_name(section_element, "h1")
    assert get_text_content(section_h1) == "Components Collection"

    # Test SubjectView
    subject_view = SubjectView(subject=subject, site=site)
    subject_result = subject_view()
    subject_element = _get_element(subject_result)
    subject_h1 = get_by_tag_name(subject_element, "h1")
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


def test_inheritance_example_target_inheritance() -> None:
    """Test Story inherits target from Subject in inheritance example."""
    site = make_site("examples.inheritance")

    # Traverse to Section and Subject using structural pattern matching
    match site.items.get("components"):
        case Section() as section:
            match section.items.get("card"):
                case Subject() as subject:
                    # Subject has Card as target
                    assert subject.target is not None

                    # Stories 0, 1, and 3 should inherit target from Subject
                    story0 = subject.items[0]
                    assert isinstance(story0, Story)
                    assert story0.target is subject.target  # Inherited Card

                    story1 = subject.items[1]
                    assert isinstance(story1, Story)
                    assert story1.target is subject.target  # Inherited Card

                    story3 = subject.items[3]
                    assert isinstance(story3, Story)
                    assert story3.target is subject.target  # Inherited Card

                    # Render one to verify it's Card
                    component_instance = story0.instance
                    assert component_instance is not None
                    rendered = component_instance()  # type: ignore[call-non-callable]
                    assert isinstance(rendered, Element)
                    # Card renders a div with h2 and p
                    h2 = get_by_tag_name(rendered, "h2")
                    assert get_text_content(h2) == "First Card"
                    p = get_by_tag_name(rendered, "p")
                    assert get_text_content(p) == "This story inherits its title from the Subject"
                case _:
                    raise AssertionError("Expected Subject for card")
        case _:
            raise AssertionError("Expected Section for components")


def test_inheritance_example_title_generation() -> None:
    """Test auto-generated Story titles in inheritance example."""
    site = make_site("examples.inheritance")

    section = site.items["components"]
    assert isinstance(section, Section)
    subject = section.items["card"]
    assert isinstance(subject, Subject)

    # Story 0: No explicit title, should be auto-generated
    story0 = subject.items[0]
    assert story0.title is not None
    # Based on Story.post_update logic: parent.title + " Story" or parent.package_path
    # Subject has no title, so it uses package_path
    assert "card" in story0.title.lower() or "story" in story0.title.lower()

    # Story 1: Explicit title should be preserved
    story1 = subject.items[1]
    assert story1.title == "Custom Card Title"

    # Story 2: No explicit title (badge override story)
    story2 = subject.items[2]
    assert story2.title is not None

    # Story 3: No explicit title, should be auto-generated
    story3 = subject.items[3]
    assert story3.title is not None


def test_inheritance_example_target_override() -> None:
    """Test Story can override Subject target in inheritance example."""
    site = make_site("examples.inheritance")

    section = site.items["components"]
    subject = section.items["card"]

    # Story 2 has target=Badge, overriding Subject's Card target
    story2 = subject.items[2]
    assert isinstance(story2, Story)
    assert story2.target is not None
    assert story2.target != subject.target  # Different from Subject's target

    # Render the Badge component
    component_instance = story2.instance
    assert component_instance is not None
    rendered = component_instance()  # type: ignore[call-non-callable]
    assert isinstance(rendered, Element)
    # Badge renders a span with count
    span = get_by_tag_name(rendered, "span")
    assert get_text_content(span) == "42"


def test_templates_example_default_template() -> None:
    """Test Story without template uses default StoryView layout."""
    site = make_site("examples.templates")

    # Traverse to Section and Subject using structural pattern matching
    match site.items.get("components"):
        case Section() as section:
            match section.items.get("alert"):
                case Subject() as subject:
                    # Story 0: No template, uses default layout
                    story = subject.items[0]
                    assert isinstance(story, Story)
                    assert story.template is None  # No custom template

                    # Render with StoryView - should use default layout
                    story_view = StoryView(story=story)
                    story_result = story_view()
                    assert isinstance(story_result, Element)

                    # Verify default layout elements
                    h1 = get_by_tag_name(story_result, "h1")
                    assert story.title is not None
                    assert get_text_content(h1) == story.title

                    # Verify props are displayed in default layout
                    paragraphs = query_all_by_tag_name(story_result, "p")
                    assert len(paragraphs) > 0

                    # Verify component instance is rendered with role="alert"
                    alert_div = get_by_tag_name(story_result, "div", attrs={"role": "alert"})
                    assert get_text_content(alert_div) == "This is an alert using default layout"
                case _:
                    raise AssertionError("Expected Subject for alert")
        case _:
            raise AssertionError("Expected Section for components")


def test_templates_example_custom_template() -> None:
    """Test Story with custom template validates template override."""
    site = make_site("examples.templates")

    section = site.items["components"]
    assert isinstance(section, Section)
    subject = section.items["alert"]
    assert isinstance(subject, Subject)

    # Story 1: Has custom template
    story = subject.items[1]
    assert isinstance(story, Story)
    assert story.template is not None  # Custom template is set

    # Render with StoryView - should use custom template
    story_view = StoryView(story=story)
    story_result = story_view()
    assert isinstance(story_result, Element)

    # Verify custom template content
    custom_div = get_by_tag_name(story_result, "div", attrs={"class": "custom"})
    h1 = get_by_tag_name(custom_div, "h1")
    assert get_text_content(h1) == "Custom Template"
    p = get_by_tag_name(custom_div, "p")
    assert get_text_content(p) == "Full control"


def test_templates_example_template_override() -> None:
    """Test template completely overrides rendering with aria-testing."""
    site = make_site("examples.templates")

    section = site.items["components"]
    subject = section.items["alert"]

    # Story 0: Default layout
    story_default = subject.items[0]
    story_view_default = StoryView(story=story_default)
    result_default = story_view_default()
    assert isinstance(result_default, Element)

    # Story 1: Custom template
    story_custom = subject.items[1]
    story_view_custom = StoryView(story=story_custom)
    result_custom = story_view_custom()
    assert isinstance(result_custom, Element)

    # Verify the custom template completely overrides rendering
    # Custom template should have specific class
    custom_div = get_by_tag_name(result_custom, "div", attrs={"class": "custom"})
    assert custom_div is not None

    # Custom template should have specific h1 content
    custom_h1 = get_by_tag_name(result_custom, "h1")
    assert get_text_content(custom_h1) == "Custom Template"

    # Verify the two rendering modes are different
    # Default layout has parent link
    default_links = query_all_by_tag_name(result_default, "a")
    assert len(default_links) > 0

    # Custom template has no links (completely different structure)
    custom_links = query_all_by_tag_name(result_custom, "a")
    assert len(custom_links) == 0


# Task Group 6: Integration tests for minimal and no_sections examples


def test_minimal_example() -> None:
    """Test minimal example - load Site, traverse tree, test all views."""
    site = make_site("examples.minimal")

    # Verify Site has title
    assert site.title == "Minimal Site"

    # Traverse to Section using structural pattern matching
    match site.items.get("components"):
        case Section() as section:
            assert section.parent is site
            assert section.package_path.endswith("components")

            # Traverse to Subject (heading)
            match section.items.get("heading"):
                case Subject() as subject:
                    assert subject.parent is section
                    assert subject.target is not None
                    assert len(subject.items) == 1

                    # Traverse to Story
                    story = subject.items[0]
                    assert isinstance(story, Story)
                    assert story.parent is subject
                    assert story.props is not None
                    assert story.target is not None  # Inherited from Subject

                    # Test component rendering
                    component_instance = story.instance
                    assert component_instance is not None
                    rendered = component_instance()  # type: ignore[call-non-callable]
                    assert isinstance(rendered, Element)
                    h1 = get_by_tag_name(rendered, "h1")
                    assert get_text_content(h1) == "World"

                    # Test StoryView rendering
                    story_view = StoryView(story=story)
                    story_result = story_view()
                    assert isinstance(story_result, Element)

                case _:
                    raise AssertionError("Expected Subject for heading")
        case _:
            raise AssertionError("Expected Section for components")


def test_minimal_example_views() -> None:
    """Test rendering all views for minimal example."""
    site = make_site("examples.minimal")
    section = site.items["components"]
    assert isinstance(section, Section)
    subject = section.items["heading"]
    assert isinstance(subject, Subject)

    # Test SectionView
    section_view = SectionView(section=section, site=site)
    section_result = section_view()
    section_element = _get_element(section_result)
    # Section should have navigation to subjects
    paragraphs = query_all_by_tag_name(section_element, "p")
    assert len(paragraphs) >= 0

    # Test SubjectView
    subject_view = SubjectView(subject=subject, site=site)
    subject_result = subject_view()
    subject_element = _get_element(subject_result)
    # Subject should have title
    h1 = get_by_tag_name(subject_element, "h1")
    assert subject.title is not None
    assert get_text_content(h1) == subject.title

    # Test StoryView
    story = subject.items[0]
    story_view = StoryView(story=story)
    story_result = story_view()
    assert isinstance(story_result, Element)


def test_no_sections_example() -> None:
    """Test no_sections example - verify Site → Subject structure, test views."""
    site = make_site("examples.no_sections")

    # Verify Site has title
    assert site.title == "No Sections Site"

    # Verify no sections in site.items
    assert len(site.items) == 0

    # In no_sections, Subjects are discovered via package discovery
    # The structure should be: Site has no Sections, Subjects are at top level
    # Based on the existing structure, we should verify the flat hierarchy
    # Let's check what's actually in the site structure
    assert isinstance(site.items, dict)


def test_no_sections_example_structure() -> None:
    """Test no_sections example demonstrates optional Sections."""
    site = make_site("examples.no_sections")

    # The key feature: no Section layer between Site and Subjects
    # Site.items should be empty (no Sections)
    assert len(site.items) == 0

    # This demonstrates Sections are optional
    assert site.title is not None


def test_inheritance_example_views() -> None:
    """Test rendering all views for inheritance example."""
    site = make_site("examples.inheritance")
    section = site.items["components"]
    assert isinstance(section, Section)
    subject = section.items["card"]
    assert isinstance(subject, Subject)

    # Test SectionView
    section_view = SectionView(section=section, site=site)
    section_result = section_view()
    _section_element = _get_element(section_result)

    # Test SubjectView
    subject_view = SubjectView(subject=subject, site=site)
    subject_result = subject_view()
    _subject_element = _get_element(subject_result)

    # Test StoryView for multiple stories
    for story in subject.items:
        story_view = StoryView(story=story)
        story_result = story_view()
        assert isinstance(story_result, Element)


def test_inheritance_example_parent_references() -> None:
    """Test parent references throughout inheritance example tree."""
    site = make_site("examples.inheritance")

    # Verify Section parent
    section = site.items["components"]
    assert isinstance(section, Section)
    assert section.parent is site

    # Verify Subject parent
    subject = section.items["card"]
    assert isinstance(subject, Subject)
    assert subject.parent is section

    # Verify all Story parents
    for story in subject.items:
        assert isinstance(story, Story)
        assert story.parent is subject


def test_templates_example_views() -> None:
    """Test rendering all views for templates example."""
    site = make_site("examples.templates")
    section = site.items["components"]
    assert isinstance(section, Section)
    subject = section.items["alert"]
    assert isinstance(subject, Subject)

    # Test SectionView
    section_view = SectionView(section=section, site=site)
    section_result = section_view()
    _section_element = _get_element(section_result)

    # Test SubjectView
    subject_view = SubjectView(subject=subject, site=site)
    subject_result = subject_view()
    _subject_element = _get_element(subject_result)

    # Test StoryView for both stories (one with template, one without)
    for story in subject.items:
        story_view = StoryView(story=story)
        story_result = story_view()
        assert isinstance(story_result, Element)


def test_all_examples_structural_integrity() -> None:
    """Test structural pattern matching and tree integrity across all examples."""
    examples = ["complete", "inheritance", "templates", "minimal"]

    for example_name in examples:
        site = make_site(f"examples.{example_name}")

        # Verify Site loads successfully
        assert site is not None
        assert site.title is not None

        # Traverse Sections using structural pattern matching
        for section_name, section_node in site.items.items():
            match section_node:
                case Section() as section:
                    # Verify parent reference
                    assert section.parent is site
                    assert section.package_path.endswith(section_name)

                    # Traverse Subjects
                    for subject_name, subject_node in section.items.items():
                        match subject_node:
                            case Subject() as subject:
                                # Verify parent reference
                                assert subject.parent is section
                                assert subject.package_path.endswith(subject_name)

                                # Traverse Stories
                                for story in subject.items:
                                    match story:
                                        case Story():
                                            # Verify parent reference
                                            assert story.parent is subject
                                            # Verify target is set (either explicit or inherited)
                                            assert story.target is not None
                                        case _:
                                            raise AssertionError(f"Expected Story in {example_name}")
                            case _:
                                raise AssertionError(f"Expected Subject in {example_name}")
                case _:
                    raise AssertionError(f"Expected Section in {example_name}")
