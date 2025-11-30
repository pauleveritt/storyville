"""Tests for make_catalog resource_path population."""

from storytime.catalog.helpers import make_catalog


def test_catalog_has_empty_resource_path_after_construction():
    """Test Catalog has resource_path='' after make_catalog construction."""
    catalog = make_catalog("examples.minimal")

    assert hasattr(catalog, "resource_path")
    assert catalog.resource_path == ""
    assert catalog.name == ""


def test_sections_have_correct_resource_path_format():
    """Test Sections have resource_path as section name."""
    catalog = make_catalog("examples.minimal")

    # Check each section has resource_path equal to its name
    for section_name, section in catalog.items.items():
        assert hasattr(section, "resource_path")
        assert section.resource_path == section_name
        assert section.resource_path == section.name


def test_subjects_have_correct_nested_resource_path_format():
    """Test Subjects have resource_path in section/subject format."""
    catalog = make_catalog("examples.minimal")

    # Check subjects under each section
    for section_name, section in catalog.items.items():
        for subject_name, subject in section.items.items():
            expected_path = f"{section_name}/{subject_name}"
            assert hasattr(subject, "resource_path")
            assert subject.resource_path == expected_path


def test_stories_have_correct_nested_resource_path_format():
    """Test Stories have resource_path in section/subject/story format."""
    catalog = make_catalog("examples.minimal")

    # Check stories under each subject
    for section_name, section in catalog.items.items():
        for subject_name, subject in section.items.items():
            for story_idx, story in enumerate(subject.items):
                expected_path = f"{section_name}/{subject_name}/{story_idx}"
                assert hasattr(story, "resource_path")
                assert story.resource_path == expected_path


def test_resource_path_flows_through_entire_tree_hierarchy():
    """Test resource_path flows correctly through Catalog -> Section -> Subject -> Story."""
    catalog = make_catalog("examples.minimal")

    # Verify catalog (root)
    assert catalog.resource_path == ""

    # Verify at least one complete path exists
    found_complete_path = False
    for section_name, section in catalog.items.items():
        # Verify section
        assert section.resource_path == section_name

        for subject_name, subject in section.items.items():
            # Verify subject
            assert subject.resource_path == f"{section_name}/{subject_name}"

            for story_idx, story in enumerate(subject.items):
                # Verify story
                assert story.resource_path == f"{section_name}/{subject_name}/{story_idx}"
                found_complete_path = True
                break

            if found_complete_path:
                break

        if found_complete_path:
            break

    # Ensure we actually tested a complete path
    assert found_complete_path, "No complete Catalog->Section->Subject->Story path found in examples.minimal"


def test_resource_path_type_is_str_not_optional():
    """Test that resource_path is typed as str (non-optional) throughout tree."""
    catalog = make_catalog("examples.minimal")

    # Catalog
    assert isinstance(catalog.resource_path, str)
    assert catalog.resource_path is not None

    # Sections
    for section in catalog.items.values():
        assert isinstance(section.resource_path, str)
        assert section.resource_path is not None

    # Subjects
    for section in catalog.items.values():
        for subject in section.items.values():
            assert isinstance(subject.resource_path, str)
            assert subject.resource_path is not None

    # Stories
    for section in catalog.items.values():
        for subject in section.items.values():
            for story in subject.items:
                assert isinstance(story.resource_path, str)
                assert story.resource_path is not None


def test_multiple_sections_have_independent_resource_paths():
    """Test that multiple sections have independent resource_path values."""
    catalog = make_catalog("examples.minimal")

    # Get all section resource_paths
    section_paths = [section.resource_path for section in catalog.items.values()]

    # Each section should have unique path equal to its name
    assert len(section_paths) == len(set(section_paths)), "Section resource_paths should be unique"

    # Each path should equal the section name
    for section_name, section in catalog.items.items():
        assert section.resource_path == section_name
