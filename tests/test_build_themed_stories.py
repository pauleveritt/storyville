"""Test build process generates themed story HTML files."""

from pathlib import Path

from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name
from tdom.parser import parse_html

from storyville.build import build_site


def test_build_generates_both_index_and_themed_story_html(tmp_path: Path) -> None:
    """Test build generates both index.html and themed_story.html per story."""
    build_site(package_location="examples.minimal", output_dir=tmp_path)

    # Check that story directory exists
    story_dir = tmp_path / "components" / "heading" / "story-0"
    assert story_dir.exists()

    # Check that both files exist
    index_html = story_dir / "index.html"
    themed_story_html = story_dir / "themed_story.html"

    assert index_html.exists()
    assert themed_story_html.exists()


def test_index_html_contains_iframe_with_relative_path(tmp_path: Path) -> None:
    """Test index.html contains iframe with src='./themed_story.html'."""
    build_site(package_location="examples.minimal", output_dir=tmp_path)

    index_html = tmp_path / "components" / "heading" / "story-0" / "index.html"
    assert index_html.exists()

    # Read and parse the HTML
    html_content = index_html.read_text()
    page = parse_html(html_content)

    # Find iframe element
    iframes = query_all_by_tag_name(page, "iframe")
    assert len(iframes) == 1

    iframe = iframes[0]
    src = iframe.attrs.get("src", "")
    assert src == "./themed_story.html"


def test_iframe_has_default_styles(tmp_path: Path) -> None:
    """Test iframe element has sensible default styles."""
    build_site(package_location="examples.minimal", output_dir=tmp_path)

    index_html = tmp_path / "components" / "heading" / "story-0" / "index.html"
    assert index_html.exists()

    # Read and parse the HTML
    html_content = index_html.read_text()
    page = parse_html(html_content)

    # Get the iframe element
    iframes = query_all_by_tag_name(page, "iframe")
    assert len(iframes) == 1

    iframe = iframes[0]
    style_attr = iframe.attrs.get("style")

    # Handle None case for type checker
    if style_attr is None:
        style = ""
    else:
        style = style_attr

    # Verify sensible default styles are present
    assert "width: 100%" in style
    assert "min-height: 600px" in style
    assert "border: 1px solid #ccc" in style


def test_themed_story_html_contains_themed_story_rendering(tmp_path: Path) -> None:
    """Test themed_story.html contains ThemedStory rendering."""
    build_site(package_location="examples.minimal", output_dir=tmp_path)

    themed_story_page = tmp_path / "components" / "heading" / "story-0" / "themed_story.html"
    assert themed_story_page.exists()

    # Read and verify it's a full HTML document
    html_content = themed_story_page.read_text()
    assert "<!DOCTYPE html>" in html_content
    assert "<html" in html_content

    # Parse and verify structure
    page = parse_html(html_content)
    html_elem = get_by_tag_name(page, "html")
    assert html_elem is not None

    # Verify has head and body
    head = get_by_tag_name(html_elem, "head")
    assert head is not None

    body = get_by_tag_name(html_elem, "body")
    assert body is not None


def test_three_phase_architecture_maintained(tmp_path: Path) -> None:
    """Test that three-phase architecture is maintained (Reading, Rendering, Writing)."""
    # This is a smoke test - if build completes without error, the architecture is maintained
    build_site(package_location="examples.minimal", output_dir=tmp_path)

    # Verify output structure exists
    assert tmp_path.exists()
    components_dir = tmp_path / "components"
    assert components_dir.exists()


def test_backward_compatibility_without_themed_layout(tmp_path: Path) -> None:
    """Test builds work WITHOUT themed_layout (existing behavior unchanged)."""
    # Build example that has no themed_layout (complete example)
    build_site(package_location="examples.complete", output_dir=tmp_path)

    # Verify build completes successfully
    assert tmp_path.exists()

    # Find a story directory in the complete example
    # complete example has: components/button/story-0, components/button/story-1, etc.
    story_dir = tmp_path / "components" / "button" / "story-0"
    assert story_dir.exists()

    # Verify index.html exists
    index_html = story_dir / "index.html"
    assert index_html.exists()

    # Verify themed_story.html does NOT exist (backward compatibility)
    themed_story_html = story_dir / "themed_story.html"
    assert not themed_story_html.exists()

    # Verify index.html does NOT contain iframe
    html_content = index_html.read_text()
    page = parse_html(html_content)
    iframes = query_all_by_tag_name(page, "iframe")
    assert len(iframes) == 0


def test_custom_themed_layout_used_in_build(tmp_path: Path) -> None:
    """Test custom ThemedLayout is used correctly during build process."""
    # Build with minimal example that has custom ThemedLayout
    build_site(package_location="examples.minimal", output_dir=tmp_path)

    themed_story_page = tmp_path / "components" / "heading" / "story-0" / "themed_story.html"
    assert themed_story_page.exists()

    # Read and parse themed story HTML
    html_content = themed_story_page.read_text()
    page = parse_html(html_content)

    # Verify custom ThemedLayout styling is present (theme-wrapper class from minimal example)
    html_elem = get_by_tag_name(page, "html")
    body = get_by_tag_name(html_elem, "body")

    # Check for theme-wrapper div from minimal ThemedLayout
    theme_wrapper_divs = query_all_by_tag_name(body, "div")
    theme_wrapper_found = False
    for div in theme_wrapper_divs:
        class_attr = div.attrs.get("class")
        # Handle None case for type checker
        if class_attr is not None and "theme-wrapper" in class_attr:
            theme_wrapper_found = True
            break

    assert theme_wrapper_found, "Custom ThemedLayout theme-wrapper not found in rendered output"


def test_end_to_end_workflow_with_themed_layout(tmp_path: Path) -> None:
    """Test full workflow from Site with themed_layout -> build -> verify both files."""
    # This is an end-to-end integration test
    build_site(package_location="examples.minimal", output_dir=tmp_path)

    # Verify story directory structure
    story_dir = tmp_path / "components" / "heading" / "story-0"
    assert story_dir.exists()

    # Verify both files exist
    index_html = story_dir / "index.html"
    themed_story_html = story_dir / "themed_story.html"
    assert index_html.exists()
    assert themed_story_html.exists()

    # Verify index.html has iframe pointing to themed_story.html
    index_content = index_html.read_text()
    index_page = parse_html(index_content)
    iframes = query_all_by_tag_name(index_page, "iframe")
    assert len(iframes) == 1
    assert iframes[0].attrs.get("src") == "./themed_story.html"

    # Verify themed_story.html contains full HTML document
    themed_content = themed_story_html.read_text()
    assert "<!DOCTYPE html>" in themed_content
    themed_page = parse_html(themed_content)
    html_elem = get_by_tag_name(themed_page, "html")
    assert html_elem is not None

    # Verify story title is present in themed version
    head = get_by_tag_name(html_elem, "head")
    title_elem = get_by_tag_name(head, "title")
    title_text = get_text_content(title_elem)
    assert len(title_text) > 0  # Has some title content

    # Verify story content is present
    body = get_by_tag_name(html_elem, "body")
    body_text = get_text_content(body)
    assert len(body_text) > 0  # Has some body content


def test_themed_story_with_story_content(tmp_path: Path) -> None:
    """Test themed_story.html contains actual story component content."""
    build_site(package_location="examples.minimal", output_dir=tmp_path)

    themed_story_page = tmp_path / "components" / "heading" / "story-0" / "themed_story.html"
    assert themed_story_page.exists()

    # Read and parse themed story HTML
    html_content = themed_story_page.read_text()
    page = parse_html(html_content)

    # Verify the story component (heading) is rendered in the themed version
    html_elem = get_by_tag_name(page, "html")
    body = get_by_tag_name(html_elem, "body")

    # The minimal heading example renders an h1 element
    headings = query_all_by_tag_name(body, "h1")
    assert len(headings) > 0, "Story component content (h1) not found in themed_story.html"

    # Verify the heading has content
    heading_text = get_text_content(headings[0])
    assert len(heading_text) > 0, "Story component heading has no content"
