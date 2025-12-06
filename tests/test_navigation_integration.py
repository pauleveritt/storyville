"""Slow integration tests for navigation features (tree expansion and sidebar toggle).

These tests build actual sites and verify the JavaScript integration works correctly
across different page types (Section, Subject, and Story pages).
"""

from pathlib import Path

import pytest

from storyville.build import build_site


@pytest.fixture
def built_site(tmp_path: Path) -> Path:
    """Build a test site for navigation integration verification.

    Returns:
        Path to the output directory containing built HTML files.
    """
    output_dir = tmp_path / "output"
    output_dir.mkdir(exist_ok=True)

    # Build the examples.minimal site which has sections, subjects, and stories
    build_site(package_location="examples.minimal", output_dir=output_dir)

    return output_dir


@pytest.mark.slow
def test_tree_expand_script_on_section_page(built_site: Path) -> None:
    """Tree expansion script should be present on section pages."""
    # Section pages are at depth 1 (e.g., /components/index.html)
    section_page = built_site / "components" / "index.html"

    assert section_page.exists(), "Section page should exist"

    html_content = section_page.read_text()

    # Verify tree-expand.mjs is linked with correct path for depth 1
    assert "../static/components/layout/static/tree-expand.mjs" in html_content, (
        "Section page should link tree-expand.mjs with depth-adjusted path"
    )
    assert 'type="module"' in html_content, "Script should be loaded as ES module"


@pytest.mark.slow
def test_tree_expand_script_on_subject_page(built_site: Path) -> None:
    """Tree expansion script should be present on subject pages."""
    # Subject pages are at depth 2 (e.g., /components/heading/index.html)
    subject_page = built_site / "components" / "heading" / "index.html"

    assert subject_page.exists(), "Subject page should exist"

    html_content = subject_page.read_text()

    # Verify tree-expand.mjs is linked with correct path for depth 2
    assert "../../static/components/layout/static/tree-expand.mjs" in html_content, (
        "Subject page should link tree-expand.mjs with depth-adjusted path"
    )
    assert 'type="module"' in html_content, "Script should be loaded as ES module"


@pytest.mark.slow
def test_tree_expand_script_on_story_page(built_site: Path) -> None:
    """Tree expansion script should be present on story pages."""
    # Story pages are at depth 3 (e.g., /components/heading/story-0/index.html)
    story_page = built_site / "components" / "heading" / "story-0" / "index.html"

    assert story_page.exists(), "Story page should exist"

    html_content = story_page.read_text()

    # Verify tree-expand.mjs is linked with correct path for depth 3
    assert "../../../static/components/layout/static/tree-expand.mjs" in html_content, (
        "Story page should link tree-expand.mjs with depth-adjusted path"
    )
    assert 'type="module"' in html_content, "Script should be loaded as ES module"


@pytest.mark.slow
def test_tree_expand_has_navigation_links_on_all_page_types(
    built_site: Path,
) -> None:
    """All page types should have navigation links for tree expansion to work."""
    pages_to_check = [
        ("index.html", "root page"),
        ("components/index.html", "section page"),
        ("components/heading/index.html", "subject page"),
        ("components/heading/story-0/index.html", "story page"),
    ]

    for page_path, page_type in pages_to_check:
        page = built_site / page_path
        assert page.exists(), f"{page_type} should exist"

        html_content = page.read_text()

        # Verify navigation structure exists
        assert "<aside>" in html_content, f"{page_type} should have aside element"
        assert "<nav>" in html_content, f"{page_type} should have nav element"
        assert '<a href="/' in html_content, (
            f"{page_type} should have navigation links with absolute hrefs"
        )
        assert "<details>" in html_content, (
            f"{page_type} should have details elements for collapsible navigation"
        )


@pytest.mark.slow
def test_sidebar_toggle_button_on_section_page(built_site: Path) -> None:
    """Sidebar toggle button should be present on section pages."""
    section_page = built_site / "components" / "index.html"

    assert section_page.exists(), "Section page should exist"

    html_content = section_page.read_text()

    # Verify sidebar toggle button exists
    assert 'id="sidebar-toggle"' in html_content, (
        "Section page should have sidebar toggle button"
    )
    assert 'aria-label="Toggle sidebar"' in html_content, (
        "Toggle button should have aria-label"
    )
    assert 'aria-expanded="true"' in html_content, (
        "Toggle button should have aria-expanded attribute"
    )
    assert '<i class="fas fa-bars"></i>' in html_content, (
        "Toggle button should have FontAwesome icon"
    )


@pytest.mark.slow
def test_sidebar_toggle_button_on_subject_page(built_site: Path) -> None:
    """Sidebar toggle button should be present on subject pages."""
    subject_page = built_site / "components" / "heading" / "index.html"

    assert subject_page.exists(), "Subject page should exist"

    html_content = subject_page.read_text()

    # Verify sidebar toggle button exists
    assert 'id="sidebar-toggle"' in html_content, (
        "Subject page should have sidebar toggle button"
    )
    assert 'aria-label="Toggle sidebar"' in html_content, (
        "Toggle button should have aria-label"
    )
    assert 'aria-expanded="true"' in html_content, (
        "Toggle button should have aria-expanded attribute"
    )
    assert '<i class="fas fa-bars"></i>' in html_content, (
        "Toggle button should have FontAwesome icon"
    )


@pytest.mark.slow
def test_sidebar_toggle_button_on_story_page(built_site: Path) -> None:
    """Sidebar toggle button should be present on story pages."""
    story_page = built_site / "components" / "heading" / "story-0" / "index.html"

    assert story_page.exists(), "Story page should exist"

    html_content = story_page.read_text()

    # Verify sidebar toggle button exists
    assert 'id="sidebar-toggle"' in html_content, (
        "Story page should have sidebar toggle button"
    )
    assert 'aria-label="Toggle sidebar"' in html_content, (
        "Toggle button should have aria-label"
    )
    assert 'aria-expanded="true"' in html_content, (
        "Toggle button should have aria-expanded attribute"
    )
    assert '<i class="fas fa-bars"></i>' in html_content, (
        "Toggle button should have FontAwesome icon"
    )


@pytest.mark.slow
def test_sidebar_script_on_all_page_types(built_site: Path) -> None:
    """Sidebar.mjs should be linked on all page types with correct depth-adjusted paths."""
    pages_and_paths = [
        ("index.html", "static/components/layout/static/sidebar.mjs", "root page"),
        (
            "components/index.html",
            "../static/components/layout/static/sidebar.mjs",
            "section page",
        ),
        (
            "components/heading/index.html",
            "../../static/components/layout/static/sidebar.mjs",
            "subject page",
        ),
        (
            "components/heading/story-0/index.html",
            "../../../static/components/layout/static/sidebar.mjs",
            "story page",
        ),
    ]

    for page_path, expected_script_src, page_type in pages_and_paths:
        page = built_site / page_path
        assert page.exists(), f"{page_type} should exist"

        html_content = page.read_text()

        # Verify sidebar.mjs is linked with correct path
        assert expected_script_src in html_content, (
            f"{page_type} should link sidebar.mjs at {expected_script_src}"
        )
        assert 'type="module"' in html_content, (
            f"{page_type} sidebar script should be loaded as ES module"
        )


@pytest.mark.slow
def test_sidebar_css_on_all_page_types(built_site: Path) -> None:
    """Sidebar CSS classes should be defined and available on all page types."""
    pages_to_check = [
        ("index.html", "static/components/layout/static/storyville.css", "root page"),
        (
            "components/index.html",
            "../static/components/layout/static/storyville.css",
            "section page",
        ),
        (
            "components/heading/index.html",
            "../../static/components/layout/static/storyville.css",
            "subject page",
        ),
        (
            "components/heading/story-0/index.html",
            "../../../static/components/layout/static/storyville.css",
            "story page",
        ),
    ]

    for page_path, expected_css_path, page_type in pages_to_check:
        page = built_site / page_path
        assert page.exists(), f"{page_type} should exist"

        html_content = page.read_text()

        # Verify CSS is linked
        assert expected_css_path in html_content, (
            f"{page_type} should link storyville.css at {expected_css_path}"
        )

    # Check the CSS file itself contains sidebar styles
    css_file = (
        built_site / "static" / "components" / "layout" / "static" / "storyville.css"
    )
    assert css_file.exists(), "storyville.css should exist in output"

    css_content = css_file.read_text()
    assert (
        ".sidebar-collapsed" in css_content or "body.sidebar-collapsed" in css_content
    ), "CSS should define sidebar-collapsed class"
    assert "transition:" in css_content, (
        "CSS should include transitions for smooth sidebar animation"
    )


@pytest.mark.slow
def test_fontawesome_loaded_on_all_page_types(built_site: Path) -> None:
    """FontAwesome CSS should be loaded on all page types for the toggle button icon."""
    pages_and_paths = [
        (
            "index.html",
            "static/vendor/fontawesome/static/all.min.css",
            "root page",
        ),
        (
            "components/index.html",
            "../static/vendor/fontawesome/static/all.min.css",
            "section page",
        ),
        (
            "components/heading/index.html",
            "../../static/vendor/fontawesome/static/all.min.css",
            "subject page",
        ),
        (
            "components/heading/story-0/index.html",
            "../../../static/vendor/fontawesome/static/all.min.css",
            "story page",
        ),
    ]

    for page_path, expected_css_path, page_type in pages_and_paths:
        page = built_site / page_path
        assert page.exists(), f"{page_type} should exist"

        html_content = page.read_text()

        # Verify FontAwesome CSS is linked
        assert expected_css_path in html_content, (
            f"{page_type} should link FontAwesome CSS at {expected_css_path}"
        )

    # Verify webfonts exist
    webfonts_dir = (
        built_site / "static" / "vendor" / "fontawesome" / "webfonts" / "static"
    )
    assert webfonts_dir.exists(), "FontAwesome webfonts directory should exist"
    assert (webfonts_dir / "fa-solid-900.ttf").exists(), (
        "FontAwesome solid font should exist"
    )
    assert (webfonts_dir / "fa-solid-900.woff2").exists(), (
        "FontAwesome solid WOFF2 font should exist"
    )
