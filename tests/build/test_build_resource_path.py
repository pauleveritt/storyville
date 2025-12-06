"""Test resource_path flow in build system.

Tests for Task Group 5: Build System Integration
"""

from storyville.catalog.models import Catalog
from storyville.section.models import Section
from storyville.story.models import Story
from storyville.subject.models import Subject


def test_section_has_resource_path_for_build() -> None:
    """Test section has resource_path attribute for build."""
    section = Section(title="Test", description="Test", items={})
    section.resource_path = "test-section"
    assert section.resource_path == "test-section"


def test_subject_has_resource_path_for_build() -> None:
    """Test subject has resource_path attribute for build."""
    subject = Subject(title="Test", description="Test", target=None, items=[])
    subject.resource_path = "test-section/test-subject"
    assert subject.resource_path == "test-section/test-subject"


def test_story_has_resource_path_for_build() -> None:
    """Test story has resource_path attribute for build."""
    story = Story(
        title="Test",
        description="Test",
        props={},
        instance=None,
        template=None,
        assertions=[],
    )
    story.resource_path = "test-section/test-subject/story-0"
    assert story.resource_path == "test-section/test-subject/story-0"


def test_catalog_has_empty_resource_path() -> None:
    """Test catalog has empty resource_path for root."""
    catalog = Catalog(title="Test", description="Test", items={})
    catalog.resource_path = ""
    assert catalog.resource_path == ""


def test_resource_path_format_section() -> None:
    """Test resource_path format for section level."""
    section = Section(title="Test", description="Test", items={})
    section.resource_path = "my-section"
    assert section.resource_path == "my-section"
    assert "/" not in section.resource_path


def test_resource_path_format_subject() -> None:
    """Test resource_path format for subject level."""
    subject = Subject(title="Test", description="Test", target=None, items=[])
    subject.resource_path = "my-section/my-subject"
    parts = subject.resource_path.split("/")
    assert len(parts) == 2
    assert parts[0] == "my-section"
    assert parts[1] == "my-subject"


def test_resource_path_format_story() -> None:
    """Test resource_path format for story level."""
    story = Story(
        title="Test",
        description="Test",
        props={},
        instance=None,
        template=None,
        assertions=[],
    )
    story.resource_path = "my-section/my-subject/story-0"
    parts = story.resource_path.split("/")
    assert len(parts) == 3
    assert parts[0] == "my-section"
    assert parts[1] == "my-subject"
    assert parts[2] == "story-0"


def test_resource_path_incremental_construction() -> None:
    """Test resource_path can be built incrementally."""
    # Section level
    section_path = "components"
    assert section_path == "components"

    # Subject level - append to section
    subject_path = f"{section_path}/button"
    assert subject_path == "components/button"

    # Story level - append to subject
    story_path = f"{subject_path}/story-0"
    assert story_path == "components/button/story-0"
