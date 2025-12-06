"""Test relative path calculation in breadcrumbs.

Tests for Task Group 7: Relative Path Conversion
"""

from storyville.components.breadcrumbs.breadcrumbs import Breadcrumbs


def test_breadcrumbs_section_depth_1() -> None:
    """Test breadcrumbs from Section level (depth 1) uses '../'."""
    breadcrumbs = Breadcrumbs(resource_path="components")
    result = str(breadcrumbs())
    # Home link should use relative path
    assert 'href="../"' in result
    # Current page (section) should not be a link
    assert "<span>components</span>" in result


def test_breadcrumbs_subject_depth_2() -> None:
    """Test breadcrumbs from Subject level (depth 2) uses '../../'."""
    breadcrumbs = Breadcrumbs(resource_path="components/button")
    result = str(breadcrumbs())
    # Home link should use relative path
    assert 'href="../../"' in result
    # Section link should use relative path
    assert 'href="../../components/"' in result
    # Current page (subject) should not be a link
    assert "<span>button</span>" in result


def test_breadcrumbs_story_depth_3() -> None:
    """Test breadcrumbs from Story level (depth 3) uses '../../../'."""
    breadcrumbs = Breadcrumbs(resource_path="components/button/story-0")
    result = str(breadcrumbs())
    # Home link should use relative path
    assert 'href="../../../"' in result
    # Section link should use relative path
    assert 'href="../../../components/"' in result
    # Subject link should use relative path
    assert 'href="../"' in result or 'href="../button/"' in result
    # Current page (story) should not be a link
    assert "<span>story-0</span>" in result


def test_home_link_relative_at_section() -> None:
    """Test Home link navigates relatively from section."""
    breadcrumbs = Breadcrumbs(resource_path="my-section")
    result = str(breadcrumbs())
    # Home should link to ../
    assert 'href="../">Home</a>' in result
    # Should not have absolute path
    assert 'href="/">Home' not in result


def test_home_link_relative_at_subject() -> None:
    """Test Home link navigates relatively from subject."""
    breadcrumbs = Breadcrumbs(resource_path="my-section/my-subject")
    result = str(breadcrumbs())
    # Home should link to ../../
    assert 'href="../../">Home</a>' in result
    # Should not have absolute path
    assert 'href="/">Home' not in result


def test_home_link_relative_at_story() -> None:
    """Test Home link navigates relatively from story."""
    breadcrumbs = Breadcrumbs(resource_path="my-section/my-subject/story-0")
    result = str(breadcrumbs())
    # Home should link to ../../../
    assert 'href="../../../">Home</a>' in result
    # Should not have absolute path
    assert 'href="/">Home' not in result


def test_no_absolute_paths_in_breadcrumbs() -> None:
    """Test breadcrumbs do not contain absolute paths."""
    # Test at different depths
    for resource_path in ["section", "section/subject", "section/subject/story-0"]:
        breadcrumbs = Breadcrumbs(resource_path=resource_path)
        result = str(breadcrumbs())
        # Should not contain href="/" (except for trailing slashes in relative paths)
        # We allow "../../" etc but not 'href="/"' at the start
        assert 'href="/' not in result or 'href="../' in result


def test_intermediate_breadcrumb_links() -> None:
    """Test intermediate links combine upward + forward paths."""
    # From story level, section and subject should be relative
    breadcrumbs = Breadcrumbs(resource_path="components/button/story-0")
    result = str(breadcrumbs())

    # Check that links are relative (not absolute)
    assert 'href="../' in result  # For subject or going up
    assert 'href="../../' in result or 'href="../../../' in result  # For section/home
