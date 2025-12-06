"""Integration tests for Pico Layout using pytest-playwright.

These tests verify DOM interactions that require a real browser environment,
specifically clicking to expand/collapse navigation sections.
All tests are marked as @pytest.mark.slow.

Note: Tests that only check static DOM structure have been moved to
tests/test_layout_structure.py which uses tdom + aria-testing for faster execution.
"""

import pytest
from pathlib import Path
from playwright.sync_api import Page, expect
from storyville.build import build_site


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
@pytest.mark.playwright
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
@pytest.mark.playwright
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
