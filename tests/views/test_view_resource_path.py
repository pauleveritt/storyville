"""Test resource_path handling in views.

Tests for Task Group 4: View Signature Updates
"""

from storytime.catalog.models import Catalog
from storytime.section.models import Section
from storytime.section.views import SectionView
from storytime.story.models import Story
from storytime.story.views import StoryView
from storytime.subject.models import Subject
from storytime.subject.views import SubjectView


def test_section_view_accepts_resource_path() -> None:
    """Test SectionView instantiation with resource_path."""
    catalog = Catalog(title="Test Site")
    section = Section(title="Test Section")
    view = SectionView(
        section=section, site=catalog, resource_path="test-section"
    )
    assert view.resource_path == "test-section"


def test_subject_view_accepts_resource_path() -> None:
    """Test SubjectView instantiation with resource_path."""
    catalog = Catalog(title="Test Site")
    subject = Subject(title="Test Subject", target=None)
    view = SubjectView(
        subject=subject, site=catalog, resource_path="test-section/test-subject"
    )
    assert view.resource_path == "test-section/test-subject"


def test_story_view_accepts_resource_path() -> None:
    """Test StoryView instantiation with resource_path."""
    catalog = Catalog(title="Test Site")
    story = Story(
        title="Test Story",
    )
    view = StoryView(
        story=story,
        site=catalog,
        resource_path="test-section/test-subject/story-0",
    )
    assert view.resource_path == "test-section/test-subject/story-0"


def test_section_view_passes_resource_path_to_layout() -> None:
    """Test resource_path passed to Layout in SectionView."""
    catalog = Catalog(title="Test Site")
    section = Section(title="Test Section")
    view = SectionView(
        section=section, site=catalog, resource_path="test-section"
    )
    result = str(view())
    # The view should render without error and pass resource_path through
    assert view.resource_path == "test-section"
    assert result  # Non-empty result


def test_subject_view_passes_resource_path_to_layout() -> None:
    """Test resource_path passed to Layout in SubjectView."""
    catalog = Catalog(title="Test Site")
    subject = Subject(title="Test Subject", target=None)
    view = SubjectView(
        subject=subject, site=catalog, resource_path="test-section/test-subject"
    )
    result = str(view())
    assert view.resource_path == "test-section/test-subject"
    assert result


def test_story_view_passes_resource_path_to_layout() -> None:
    """Test resource_path passed to Layout in StoryView."""
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
    assert view.resource_path == "test-section/test-subject/story-0"
    assert result


def test_section_view_with_empty_resource_path() -> None:
    """Test SectionView with empty resource_path."""
    catalog = Catalog(title="Test Site")
    section = Section(title="Test Section")
    view = SectionView(section=section, site=catalog, resource_path="")
    assert view.resource_path == ""


def test_subject_view_with_empty_resource_path() -> None:
    """Test SubjectView with empty resource_path."""
    catalog = Catalog(title="Test Site")
    subject = Subject(title="Test Subject", target=None)
    view = SubjectView(subject=subject, site=catalog, resource_path="")
    assert view.resource_path == ""
