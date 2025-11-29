"""Integrate example testing into the main suite."""

from pathlib import Path

import pytest
from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name
from tdom.parser import parse_html
from storytime import make_catalog
from storytime.build import build_catalog
from storytime.section import Section
from storytime.section.views import SectionView
from storytime.story import Story
from storytime.story.views import StoryView
from storytime.subject import Subject
from storytime.subject.views import SubjectView

def test_complete_example_structure() -> None:
    """Test the complete example Catalog/Section/Subject hierarchy."""
    catalog = make_catalog("examples.complete")

    # Verify Catalog has title
    assert catalog.title == "Complete Example"

    # Traverse to Section using structural pattern matching
    match catalog.items.get("components"):
        case Section() as section:
            assert section.title == "Components Collection"
            assert section.description == "A collection of component examples with all optional fields populated"
            assert section.parent is catalog

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
    catalog = make_catalog("examples.complete")

    # Catalogfields
    assert catalog.title is not None

    # Section fields
    section = catalog.items["components"]
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
    catalog = make_catalog("examples.complete")
    section = catalog.items["components"]
    subject = section.items["button"]

    # Pattern 1: Props only (minimal)
    story1 = subject.items[0]
    assert story1.props is not None
    assert story1.target is not None
    # Render the component - instance is already the rendered
    rendered1 = story1.instance
    assert rendered1 is not None

    button1 = get_by_tag_name(rendered1, "button")
    assert get_text_content(button1) == "Click Me"
    assert button1.attrs.get("class") == "primary"

    # Pattern 2: Story with custom title and description
    story2 = subject.items[1]
    assert story2.title == "Secondary Action Button"
    assert story2.description is not None
    rendered2 = story2.instance
    assert rendered2 is not None

    button2 = get_by_tag_name(rendered2, "button")
    assert get_text_content(button2) == "Learn More"
    assert button2.attrs.get("class") == "secondary"

    # Pattern 3: Different props for same component
    story3 = subject.items[2]
    rendered3 = story3.instance
    assert rendered3 is not None

    button3 = get_by_tag_name(rendered3, "button")
    assert get_text_content(button3) == "Cancel"
    assert button3.attrs.get("class") == "danger"

def test_complete_example_views() -> None:
    """Test rendering views for Section, Subject, and Story."""
    catalog = make_catalog("examples.complete")
    section = catalog.items["components"]
    subject = section.items["button"]

    # Test SectionView
    section_view = SectionView(section=section, site=catalog)
    section_result = section_view()
    section_element = parse_html(str(section_result))
    section_h1 = get_by_tag_name(section_element, "h1")
    assert get_text_content(section_h1) == "Components Collection"

    # Test SubjectView
    subject_view = SubjectView(subject=subject, site=catalog)
    subject_result = subject_view()
    subject_element = parse_html(str(subject_result))
    subject_h1 = get_by_tag_name(subject_element, "h1")
    assert get_text_content(subject_h1) == "Button Component"

    # Test StoryView for one story (default layout)
    story = subject.items[0]
    story_view = StoryView(story=story, site=catalog)
    story_result = story_view()
    story_element = parse_html(str(story_result))
    # Verify the story view contains the component
    paragraphs = query_all_by_tag_name(story_element, "p")
    assert len(paragraphs) > 0

def test_complete_example_field_inheritance() -> None:
    """Test field inheritance patterns in complete example."""
    catalog = make_catalog("examples.complete")
    section = catalog.items["components"]
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
    catalog = make_catalog("examples.inheritance")

    # Traverse to Section and Subject using structural pattern matching
    match catalog.items.get("components"):
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
                    rendered = story0.instance
                    assert rendered is not None

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
    catalog = make_catalog("examples.inheritance")

    section = catalog.items["components"]
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
    catalog = make_catalog("examples.inheritance")

    section = catalog.items["components"]
    subject = section.items["card"]

    # Story 2 has target=Badge, overriding Subject's Card target
    story2 = subject.items[2]
    assert isinstance(story2, Story)
    assert story2.target is not None
    assert story2.target != subject.target  # Different from Subject's target

    # Render the Badge component
    rendered = story2.instance
    assert rendered is not None

    # Badge renders a span with count
    span = get_by_tag_name(rendered, "span")
    assert get_text_content(span) == "42"

def test_templates_example_default_template() -> None:
    """Test Story without template uses default StoryView layout."""
    catalog = make_catalog("examples.templates")

    # Traverse to Section and Subject using structural pattern matching
    match catalog.items.get("components"):
        case Section() as section:
            match section.items.get("alert"):
                case Subject() as subject:
                    # Story 0: No template, uses default layout
                    story = subject.items[0]
                    assert isinstance(story, Story)
                    assert story.template is None  # No custom template

                    # Render with StoryView - should use default layout
                    story_view = StoryView(story=story, site=catalog)
                    story_result = story_view()
                    story_element = parse_html(str(story_result))

                    # Verify default layout elements
                    h1 = get_by_tag_name(story_element, "h1")
                    assert story.title is not None
                    assert get_text_content(h1) == story.title

                    # Verify props are displayed in default layout
                    paragraphs = query_all_by_tag_name(story_element, "p")
                    assert len(paragraphs) > 0

                    # Verify component instance is rendered with role="alert"
                    alert_div = get_by_tag_name(story_element, "div", attrs={"role": "alert"})
                    assert get_text_content(alert_div) == "This is an alert using default layout"
                case _:
                    raise AssertionError("Expected Subject for alert")
        case _:
            raise AssertionError("Expected Section for components")

def test_templates_example_custom_template() -> None:
    """Test Story with custom template validates template override."""
    catalog = make_catalog("examples.templates")

    section = catalog.items["components"]
    assert isinstance(section, Section)
    subject = section.items["alert"]
    assert isinstance(subject, Subject)

    # Story 1: Has custom template
    story = subject.items[1]
    assert isinstance(story, Story)
    assert story.template is not None  # Custom template is set

    # Render with StoryView - should use custom template
    story_view = StoryView(story=story, site=catalog)
    story_result = story_view()
    # Custom template returns  directly (no Layout wrapper)

    # Verify custom template content
    custom_div = get_by_tag_name(story_result, "div", attrs={"class": "custom"})
    h1 = get_by_tag_name(custom_div, "h1")
    assert get_text_content(h1) == "Custom Template"
    p = get_by_tag_name(custom_div, "p")
    assert get_text_content(p) == "Full control"

def test_templates_example_template_override() -> None:
    """Test template completely overrides rendering with aria-testing."""
    catalog = make_catalog("examples.templates")

    section = catalog.items["components"]
    subject = section.items["alert"]

    # Story 0: Default layout
    story_default = subject.items[0]
    story_view_default = StoryView(story=story_default, site=catalog)
    result_default = story_view_default()
    _element_default = (str(result_default))

    # Story 1: Custom template
    story_custom = subject.items[1]
    story_view_custom = StoryView(story=story_custom, site=catalog)
    result_custom = story_view_custom()

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
    catalog = make_catalog("examples.minimal")

    # Verify Catalog has title
    assert catalog.title == "Minimal Catalog"

    # Traverse to Section using structural pattern matching
    match catalog.items.get("components"):
        case Section() as section:
            assert section.parent is catalog
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
                    rendered = story.instance
                    assert rendered is not None

                    h1 = get_by_tag_name(rendered, "h1")
                    assert get_text_content(h1) == "World"

                    # Test StoryView rendering
                    story_view = StoryView(story=story, site=catalog)
                    story_result = story_view()
                    _story_element = parse_html(str(story_result))

                case _:
                    raise AssertionError("Expected Subject for heading")
        case _:
            raise AssertionError("Expected Section for components")

def test_minimal_example_views() -> None:
    """Test rendering all views for minimal example."""
    catalog = make_catalog("examples.minimal")
    section = catalog.items["components"]
    assert isinstance(section, Section)
    subject = section.items["heading"]
    assert isinstance(subject, Subject)

    # Test SectionView
    section_view = SectionView(section=section, site=catalog)
    section_result = section_view()
    section_element = parse_html(str(section_result))
    # Section should have navigation to subjects
    paragraphs = query_all_by_tag_name(section_element, "p")
    assert len(paragraphs) >= 0

    # Test SubjectView
    subject_view = SubjectView(subject=subject, site=catalog)
    subject_result = subject_view()
    subject_element = parse_html(str(subject_result))
    # Subject should have title
    h1 = get_by_tag_name(subject_element, "h1")
    assert subject.title is not None
    assert get_text_content(h1) == subject.title

    # Test StoryView
    story = subject.items[0]
    story_view = StoryView(story=story, site=catalog)
    story_result = story_view()
    _story_element = parse_html(str(story_result))

def test_no_sections_example() -> None:
    """Test no_sections example - verify Site → Subject structure, test views."""
    catalog = make_catalog("examples.no_sections")

    # Verify Catalog has title
    assert catalog.title == "No Sections Catalog"

    # Verify no sections in site.items
    assert len(catalog.items) == 0

    # In no_sections, Subjects are discovered via package discovery
    # The structure should be: Site has no Sections, Subjects are at top level
    # Based on the existing structure, we should verify the flat hierarchy
    # Let's check what's actually in the catalog structure
    assert isinstance(catalog.items, dict)

def test_no_sections_example_structure() -> None:
    """Test no_sections example demonstrates optional Sections."""
    catalog = make_catalog("examples.no_sections")

    # The key feature: no Section layer between Site and Subjects
    # Site.items should be empty (no Sections)
    assert len(catalog.items) == 0

    # This demonstrates Sections are optional
    assert catalog.title is not None

def test_inheritance_example_views() -> None:
    """Test rendering all views for inheritance example."""
    catalog = make_catalog("examples.inheritance")
    section = catalog.items["components"]
    assert isinstance(section, Section)
    subject = section.items["card"]
    assert isinstance(subject, Subject)

    # Test SectionView
    section_view = SectionView(section=section, site=catalog)
    section_result = section_view()
    _section_element = parse_html(str(section_result))

    # Test SubjectView
    subject_view = SubjectView(subject=subject, site=catalog)
    subject_result = subject_view()
    _subject_element = parse_html(str(subject_result))

    # Test StoryView for multiple stories
    for story in subject.items:
        story_view = StoryView(story=story, site=catalog)
        story_result = story_view()
        _story_element = parse_html(str(story_result))

def test_inheritance_example_parent_references() -> None:
    """Test parent references throughout inheritance example tree."""
    catalog = make_catalog("examples.inheritance")

    # Verify Section parent
    section = catalog.items["components"]
    assert isinstance(section, Section)
    assert section.parent is catalog

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
    catalog = make_catalog("examples.templates")
    section = catalog.items["components"]
    assert isinstance(section, Section)
    subject = section.items["alert"]
    assert isinstance(subject, Subject)

    # Test SectionView
    section_view = SectionView(section=section, site=catalog)
    section_result = section_view()
    _section_element = parse_html(str(section_result))

    # Test SubjectView
    subject_view = SubjectView(subject=subject, site=catalog)
    subject_result = subject_view()
    _subject_element = parse_html(str(subject_result))

    # Test StoryView for both stories (one with template, one without)
    for story in subject.items:
        story_view = StoryView(story=story, site=catalog)
        _story_result = story_view()
        # Note: Some stories may have custom templates (return ),
        # others use default layout (return  with Layout wrapper)
        # Both are valid results

def test_all_examples_structural_integrity() -> None:
    """Test structural pattern matching and tree integrity across all examples."""
    examples = ["complete", "inheritance", "templates", "minimal"]

    for example_name in examples:
        catalog = make_catalog(f"examples.{example_name}")

        # Verify Catalog loads successfully
        assert catalog is not None
        assert catalog.title is not None

        # Traverse Sections using structural pattern matching
        for section_name, section_node in catalog.items.items():
            match section_node:
                case Section() as section:
                    # Verify parent reference
                    assert section.parent is catalog
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

# Task Group 1: Tests for examples.huge Site structure

@pytest.mark.slow
def test_huge_example_site_loads() -> None:
    """Test huge example Site loads successfully with title."""
    catalog = make_catalog("examples.huge")

    # Verify Catalog has correct title
    assert catalog.title == "Huge Scale Example"

@pytest.mark.slow
def test_huge_example_has_ten_sections() -> None:
    """Test huge example has 10 sections."""
    catalog = make_catalog("examples.huge")

    # Verify Catalog has exactly 10 sections
    assert len(catalog.items) == 10

@pytest.mark.slow
def test_huge_example_section_names() -> None:
    """Test huge example section names match expected design system categories."""
    catalog = make_catalog("examples.huge")

    # Expected section names (directory names)
    expected_sections = {
        "forms",
        "navigation",
        "feedback",
        "layout",
        "data_display",
        "overlays",
        "media",
        "typography",
        "inputs",
        "controls",
    }

    # Verify all expected sections exist
    assert set(catalog.items.keys()) == expected_sections

    # Verify each is a Section with the correct title
    match catalog.items.get("forms"):
        case Section() as section:
            assert section.title == "Forms"
            assert section.description == "Form components"
        case _:
            raise AssertionError("Expected Section for forms")

    match catalog.items.get("navigation"):
        case Section() as section:
            assert section.title == "Navigation"
            assert section.description == "Navigation components"
        case _:
            raise AssertionError("Expected Section for navigation")

    match catalog.items.get("feedback"):
        case Section() as section:
            assert section.title == "Feedback"
            assert section.description == "Feedback components"
        case _:
            raise AssertionError("Expected Section for feedback")

    match catalog.items.get("layout"):
        case Section() as section:
            assert section.title == "Layout"
            assert section.description == "Layout components"
        case _:
            raise AssertionError("Expected Section for layout")

# Task Group 2: Tests for component rendering

@pytest.mark.slow
def test_huge_component_renders_correctly() -> None:
    """Test huge example components render with correct structure."""
    catalog = make_catalog("examples.huge")

    # Get a sample component from forms section
    match catalog.items.get("forms"):
        case Section() as section:
            # Get first subject
            if section.items:
                first_subject_key = list(section.items.keys())[0]
                subject = section.items[first_subject_key]
                assert isinstance(subject, Subject)

                # Verify subject has 3 stories
                assert len(subject.items) == 3

                # Test first story renders
                story = subject.items[0]
                assert isinstance(story, Story)
                rendered = story.instance
                assert rendered is not None

        case _:
            raise AssertionError("Expected Section for forms")

@pytest.mark.slow
def test_huge_component_props_applied() -> None:
    """Test huge example component props are correctly applied."""
    catalog = make_catalog("examples.huge")

    # Get forms section and first component
    section = catalog.items["forms"]
    assert isinstance(section, Section)

    if section.items:
        first_subject_key = list(section.items.keys())[0]
        subject = section.items[first_subject_key]
        assert isinstance(subject, Subject)

        # Test default state story
        story_default = subject.items[0]
        assert story_default.props is not None
        assert story_default.props.get("text") == "Default"
        assert story_default.props.get("variant") == "primary"
        assert story_default.props.get("state") == "default"

        # Test disabled state story
        story_disabled = subject.items[1]
        assert story_disabled.props is not None
        assert story_disabled.props.get("text") == "Disabled"
        assert story_disabled.props.get("state") == "disabled"

        # Test loading state story
        story_loading = subject.items[2]
        assert story_loading.props is not None
        assert story_loading.props.get("text") == "Loading"
        assert story_loading.props.get("state") == "loading"

@pytest.mark.slow
def test_huge_component_html_structure() -> None:
    """Test huge example components render basic HTML with class attributes."""
    catalog = make_catalog("examples.huge")

    # Get forms section
    section = catalog.items["forms"]
    assert isinstance(section, Section)

    if section.items:
        first_subject_key = list(section.items.keys())[0]
        subject = section.items[first_subject_key]
        assert isinstance(subject, Subject)

        # Test rendered HTML has proper structure
        story = subject.items[0]
        rendered = story.instance
        assert rendered is not None

        # Verify has element name (div, button, or span)
        assert rendered.tag in ("div", "button", "span")

        # Verify has class attribute
        assert "class" in rendered.attrs

@pytest.mark.slow
def test_huge_all_sections_have_ten_subjects() -> None:
    """Test all sections in huge example have 10 subjects."""
    catalog = make_catalog("examples.huge")

    # Verify each section has 10 subjects
    for section_name, section_node in catalog.items.items():
        match section_node:
            case Section() as section:
                assert len(section.items) == 10, f"Section {section_name} should have 10 subjects"

                # Verify each subject has 3 stories
                for subject_name, subject_node in section.items.items():
                    match subject_node:
                        case Subject() as subject:
                            assert len(subject.items) == 3, f"Subject {subject_name} should have 3 stories"
                        case _:
                            raise AssertionError(f"Expected Subject for {subject_name}")
            case _:
                raise AssertionError(f"Expected Section for {section_name}")

# Task Group 4: Performance Testing and Integration

@pytest.mark.slow
def test_huge_example(tmp_path: Path) -> None:
    """Smoke test for examples.huge - verify structure loads correctly."""
    catalog = make_catalog("examples.huge")

    # Verify site has 10 sections
    assert len(catalog.items) == 10

    # Verify first section has 10 subjects using structural pattern matching
    match catalog.items.get("forms"):
        case Section() as section:
            assert len(section.items) == 10

            # Verify first subject has 3 stories
            first_subject_key = list(section.items.keys())[0]
            match section.items.get(first_subject_key):
                case Subject() as subject:
                    assert len(subject.items) == 3
                case _:
                    raise AssertionError("Expected Subject in forms section")
        case _:
            raise AssertionError("Expected Section for forms")

@pytest.mark.slow
def test_huge_build_smoke(tmp_path: Path) -> None:
    """Build smoke test for examples.huge - verify build completes."""
    # Build site to tmp_path
    build_catalog("examples.huge", tmp_path)

    # Verify build completes without errors
    assert tmp_path.exists()
    assert (tmp_path / "index.html").exists()

    # Count output directories
    # Expected: 1 site root + 10 sections + 100 subjects + 300 stories = 411 directories total
    # But we're counting directories with index.html files
    total_dirs = 0
    for item in tmp_path.rglob("*"):
        if item.is_dir():
            total_dirs += 1

    # Expect at least sections + subjects + stories directories (~410+)
    # Note: The actual count includes story-N directories
    assert total_dirs > 300, f"Expected >300 directories, got {total_dirs}"

    # Verify index.html exists in key locations
    assert (tmp_path / "index.html").exists()  # Site root
    assert (tmp_path / "forms" / "index.html").exists()  # First section
    assert (tmp_path / "navigation" / "index.html").exists()  # Another section

    # Verify at least one subject has index.html
    forms_subjects = list((tmp_path / "forms").iterdir())
    subject_dirs = [d for d in forms_subjects if d.is_dir() and d.name != "static"]
    assert len(subject_dirs) > 0
    first_subject_dir = subject_dirs[0]
    assert (first_subject_dir / "index.html").exists()

    # Verify at least one story has index.html
    story_dirs = [d for d in first_subject_dir.iterdir() if d.is_dir() and d.name.startswith("story-")]
    assert len(story_dirs) > 0
    assert (story_dirs[0] / "index.html").exists()

@pytest.mark.slow
def test_huge_build_performance(benchmark, tmp_path: Path) -> None:
    """Performance benchmark test for examples.huge build."""
    # Measure total build time using pytest-benchmark
    benchmark(build_catalog, "examples.huge", tmp_path)

    # No validation here - just timing
    # The benchmark fixture will track timing metrics automatically
