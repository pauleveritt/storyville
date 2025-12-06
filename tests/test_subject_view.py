"""Tests for SubjectView description rendering."""

from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name

from storyville.section.models import Section
from storyville.catalog.models import Catalog
from storyville.subject.models import Subject
from storyville.subject.views import SubjectView


def test_subject_view_description_renders() -> None:
    """Test that subject description renders after title and before Target line."""
    catalog = Catalog(title="Test Catalog")
    section = Section(title="Components", parent=catalog)
    subject = Subject(
        title="Button",
        description="A clickable button component",
        parent=section,
    )

    view = SubjectView(subject=subject, site=catalog)
    result = view()

    # Verify result is not None
    assert result is not None

    # Get the main element (content area) to avoid layout elements
    main = get_by_tag_name(result, "main")

    # Find all paragraph elements within main
    paragraphs = query_all_by_tag_name(main, "p")
    assert len(paragraphs) >= 2  # description + "No stories defined" or Target line

    # First paragraph should be the description
    description_p = paragraphs[0]
    assert get_text_content(description_p) == "A clickable button component"

    # Verify description appears before Target line
    # Check that the second paragraph contains "Target:"
    target_p = paragraphs[1]
    target_text = get_text_content(target_p)
    assert "Target:" in target_text


def test_subject_view_description_skipped_when_none() -> None:
    """Test that description is not rendered when None."""
    catalog = Catalog(title="Test Catalog")
    section = Section(title="Components", parent=catalog)
    subject = Subject(
        title="Button",
        description=None,
        parent=section,
    )

    view = SubjectView(subject=subject, site=catalog)
    result = view()

    # Verify result is not None
    assert result is not None

    # Get the main element (content area) to avoid layout elements
    main = get_by_tag_name(result, "main")

    # Find all paragraph elements within main
    paragraphs = query_all_by_tag_name(main, "p")

    # Should only have "Target:" and "No stories defined" paragraphs
    # Description paragraph should not be present
    assert len(paragraphs) == 2  # Target + "No stories defined"

    # First paragraph should be Target line (description skipped)
    target_p = paragraphs[0]
    target_text = get_text_content(target_p)
    assert "Target:" in target_text


def test_subject_view_description_skipped_when_empty() -> None:
    """Test that description is not rendered when empty string."""
    catalog = Catalog(title="Test Catalog")
    section = Section(title="Components", parent=catalog)
    subject = Subject(
        title="Button",
        description="",
        parent=section,
    )

    view = SubjectView(subject=subject, site=catalog)
    result = view()

    # Verify result is not None
    assert result is not None

    # Get the main element (content area) to avoid layout elements
    main = get_by_tag_name(result, "main")

    # Find all paragraph elements within main
    paragraphs = query_all_by_tag_name(main, "p")

    # Empty string should also be skipped (no empty <p></p> tags)
    # So we should have Target + "No stories defined"
    assert len(paragraphs) == 2

    # First paragraph should be Target line (description skipped)
    target_p = paragraphs[0]
    target_text = get_text_content(target_p)
    assert "Target:" in target_text


def test_subject_view_description_html_escaped() -> None:
    """Test that dangerous HTML characters are automatically escaped."""
    catalog = Catalog(title="Test Catalog")
    section = Section(title="Components", parent=catalog)
    subject = Subject(
        title="Button",
        description="<script>alert('xss')</script>Safe text",
        parent=section,
    )

    view = SubjectView(subject=subject, site=catalog)
    result = view()

    # Verify result is not None
    assert result is not None

    # Get the main element (content area) to avoid layout elements
    main = get_by_tag_name(result, "main")

    # Find all paragraph elements within main
    paragraphs = query_all_by_tag_name(main, "p")

    # First paragraph should be the description
    description_p = paragraphs[0]
    description_text = get_text_content(description_p)

    # Text content should contain the literal script tags (escaped)
    # tdom's automatic escaping converts < to &lt; and > to &gt;
    assert "<script>alert('xss')</script>Safe text" in description_text
