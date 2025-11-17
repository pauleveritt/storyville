"""Integration tests for Pico Layout using pytest-playwright.

These tests verify DOM interactions that require a real browser environment,
such as clicking to expand/collapse navigation sections.
All tests are marked as @pytest.mark.slow.

Note: Tests requiring navigation between pages are limited due to file:// URL
constraints. The layout uses absolute paths (/) which don't work with file://
URLs. This is acceptable for a static site that will be served via HTTP.
"""

import re
import pytest
from pathlib import Path
from playwright.sync_api import Page, expect
from storytime.build import build_site


@pytest.fixture
def built_site(tmp_path: Path) -> Path:
    """Build a test site with hierarchical structure.

    Creates a minimal site structure with:
    - One section with one subject containing one story
    - About and Debug pages

    Returns:
        Path to the output directory containing built HTML files.
    """
    output_dir = tmp_path / "output"
    output_dir.mkdir(exist_ok=True)

    # Build the examples.minimal site for testing
    build_site(package_location="examples.minimal", output_dir=output_dir)

    return output_dir


@pytest.fixture
def site_url(built_site: Path) -> str:
    """Return file:// URL to the built site.

    Args:
        built_site: Path to built site directory.

    Returns:
        file:// URL to index.html
    """
    return f"file://{built_site.absolute()}/index.html"


@pytest.mark.slow
@pytest.mark.playwright
def test_header_navigation_links_present(page: Page, site_url: str) -> None:
    """Header should contain Home, About, and Debug navigation links."""
    # Arrange & Act
    page.goto(site_url)

    # Assert - check header nav contains expected links
    header = page.locator("header nav")
    expect(header.get_by_role("link", name="Home")).to_be_visible()
    expect(header.get_by_role("link", name="About")).to_be_visible()
    expect(header.get_by_role("link", name="Debug")).to_be_visible()


@pytest.mark.slow
def test_header_links_have_correct_hrefs(page: Page, site_url: str) -> None:
    """Header navigation links should have correct href attributes."""
    # Arrange & Act
    page.goto(site_url)

    # Assert - verify href attributes
    header = page.locator("header nav")
    expect(header.get_by_role("link", name="Home")).to_have_attribute("href", "/")
    expect(header.get_by_role("link", name="About")).to_have_attribute("href", "/about")
    expect(header.get_by_role("link", name="Debug")).to_have_attribute("href", "/debug")


@pytest.mark.slow
def test_sidebar_navigation_sections_collapsed_by_default(page: Page, site_url: str) -> None:
    """Sidebar sections should be collapsed by default (no open attribute)."""
    # Arrange & Act
    page.goto(site_url)

    # Assert - details elements should not have open attribute
    aside = page.locator("aside")
    sections = aside.locator("details")

    # Check that at least one section exists
    expect(sections.first).to_be_visible()

    # Check that sections are collapsed (no open attribute on first section)
    # We can check this by verifying the details element doesn't have [open]
    collapsed_sections = aside.locator("details:not([open])")
    expect(collapsed_sections.first).to_be_visible()


@pytest.mark.slow
def test_clicking_section_expands_it(page: Page, site_url: str) -> None:
    """Clicking a collapsed section summary should expand it."""
    # Arrange
    page.goto(site_url)
    aside = page.locator("aside")

    # Find first section that's collapsed
    first_section = aside.locator("details").first
    first_summary = first_section.locator("summary").first

    # Act - click the summary to expand
    first_summary.click()

    # Assert - section should now be expanded (has open attribute)
    expect(first_section).to_have_attribute("open", "")


@pytest.mark.slow
def test_clicking_expanded_section_collapses_it(page: Page, site_url: str) -> None:
    """Clicking an expanded section summary should collapse it."""
    # Arrange
    page.goto(site_url)
    aside = page.locator("aside")
    first_section = aside.locator("details").first
    first_summary = first_section.locator("summary").first

    # Expand the section first
    first_summary.click()
    expect(first_section).to_have_attribute("open", "")

    # Act - click again to collapse
    first_summary.click()

    # Assert - section should now be collapsed (no open attribute)
    expect(first_section).not_to_have_attribute("open", "")


@pytest.mark.slow
def test_nested_subject_expands_and_collapses(page: Page, site_url: str) -> None:
    """Clicking a nested subject summary should expand/collapse it independently."""
    # Arrange
    page.goto(site_url)
    aside = page.locator("aside")

    # First expand a section to access nested subjects
    first_section = aside.locator("details").first
    first_section.locator("summary").first.click()
    expect(first_section).to_have_attribute("open", "")

    # Find first nested subject details
    nested_subject = first_section.locator("details").first
    subject_summary = nested_subject.locator("summary").first

    # Act - click subject summary to expand
    subject_summary.click()

    # Assert - subject should be expanded
    expect(nested_subject).to_have_attribute("open", "")

    # Act - click again to collapse
    subject_summary.click()

    # Assert - subject should be collapsed
    expect(nested_subject).not_to_have_attribute("open", "")


@pytest.mark.slow
def test_footer_displays_copyright(page: Page, site_url: str) -> None:
    """Footer should display copyright text."""
    # Arrange & Act
    page.goto(site_url)

    # Assert - footer should contain copyright text
    footer = page.locator("footer")
    expect(footer).to_be_visible()
    expect(footer).to_contain_text("2025 Storytime")


@pytest.mark.slow
def test_sidebar_shows_hierarchical_structure(page: Page, site_url: str) -> None:
    """Sidebar should display three-level hierarchy (sections > subjects > stories)."""
    # Arrange
    page.goto(site_url)
    aside = page.locator("aside")

    # Assert - check structure exists
    # Should have section-level details
    section_details = aside.locator("> nav > details")
    expect(section_details.first).to_be_visible()

    # Expand first section - use > selector to get direct child summary only
    first_section = section_details.first
    first_section.locator("> summary").click()

    # Should have nested subject-level details inside the section
    subject_details = first_section.locator("details")
    expect(subject_details.first).to_be_visible()

    # Expand first subject - use > selector to get direct child summary only
    first_subject = subject_details.first
    first_subject.locator("> summary").click()

    # Should have story links inside the subject (li > a)
    story_links = first_subject.locator("li a")
    expect(story_links.first).to_be_visible()


@pytest.mark.slow
def test_story_links_in_sidebar_have_correct_structure(page: Page, site_url: str) -> None:
    """Story links in sidebar should follow /section/{key}/subject/{key}/story-{idx}.html pattern."""
    # Arrange
    page.goto(site_url)
    aside = page.locator("aside")

    # Expand first section and subject
    first_section = aside.locator("details").first
    first_section.locator("summary").first.click()

    first_subject = first_section.locator("details").first
    first_subject.locator("summary").first.click()

    # Get first story link
    story_link = first_subject.locator("li a").first

    # Assert - href should match expected pattern
    href = story_link.get_attribute("href")
    assert href is not None
    # Pattern: /section/{key}/subject/{key}/story-{idx}.html
    assert re.match(r"^/section/[\w-]+/subject/[\w-]+/story-\d+\.html$", href)
