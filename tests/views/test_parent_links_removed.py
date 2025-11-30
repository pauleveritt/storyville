"""Test Parent links removed from view templates.

Tests for Task Group 6: Template Cleanup (Remove Parent Links)
"""

from storytime.catalog.models import Catalog
from storytime.section.models import Section
from storytime.section.views import SectionView
from storytime.story.models import Story
from storytime.story.views import StoryView
from storytime.subject.models import Subject
from storytime.subject.views import SubjectView


def test_section_view_no_parent_link() -> None:
    """Test SectionView output does not contain 'href=".."'."""
    catalog = Catalog(title="Test Site")
    section = Section(title="Test Section")
    view = SectionView(
        section=section, site=catalog, resource_path="test-section"
    )
    result = str(view())
    assert 'href=".."' not in result
    assert ">Parent<" not in result


def test_subject_view_no_parent_link() -> None:
    """Test SubjectView output does not contain 'href=".."'."""
    catalog = Catalog(title="Test Site")
    subject = Subject(title="Test Subject", target=None)
    view = SubjectView(
        subject=subject, site=catalog, resource_path="test-section/test-subject"
    )
    result = str(view())
    assert 'href=".."' not in result
    assert ">Parent<" not in result


def test_story_view_no_parent_link() -> None:
    """Test StoryView output does not contain 'href=".."'."""
    catalog = Catalog(title="Test Site")
    story = Story(
        title="Test Story",
    )
    view = StoryView(
        story=story,
        site=catalog,
        resource_path="test-section/test-subject/story-0",
    )
    result = str(view())
    assert 'href=".."' not in result
    assert ">Parent<" not in result


def test_section_view_has_breadcrumbs_instead() -> None:
    """Test section view has breadcrumbs navigation instead of Parent link."""
    catalog = Catalog(title="Test Site")
    section = Section(title="Test Section")
    view = SectionView(
        section=section, site=catalog, resource_path="test-section"
    )
    result = str(view())
    # Should have breadcrumb navigation
    assert 'aria-label="Breadcrumb"' in result


def test_subject_view_has_breadcrumbs_instead() -> None:
    """Test subject view has breadcrumbs navigation instead of Parent link."""
    catalog = Catalog(title="Test Site")
    subject = Subject(title="Test Subject", target=None)
    view = SubjectView(
        subject=subject, site=catalog, resource_path="test-section/test-subject"
    )
    result = str(view())
    # Should have breadcrumb navigation
    assert 'aria-label="Breadcrumb"' in result


def test_story_view_has_breadcrumbs_instead() -> None:
    """Test story view has breadcrumbs navigation instead of Parent link."""
    catalog = Catalog(title="Test Site")
    story = Story(
        title="Test Story",
    )
    view = StoryView(
        story=story,
        site=catalog,
        resource_path="test-section/test-subject/story-0",
    )
    result = str(view())
    # Should have breadcrumb navigation
    assert 'aria-label="Breadcrumb"' in result


def test_subject_view_empty_state_no_parent_link() -> None:
    """Test SubjectView empty state does not have Parent link."""
    catalog = Catalog(title="Test Site")
    subject = Subject(title="Test Subject", target=None)
    view = SubjectView(
        subject=subject, site=catalog, resource_path="test-section/test-subject"
    )
    result = str(view())
    assert "No stories defined" in result
    assert 'href=".."' not in result
    assert ">Parent<" not in result
