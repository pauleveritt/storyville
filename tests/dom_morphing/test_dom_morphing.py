"""Tests for DOM morphing functionality with idiomorph integration."""

from pathlib import Path
from storyville.watchers import read_story_html


class TestIdiomorphBundling:
    """Test that idiomorph library is bundled and accessible."""

    def test_idiomorph_file_exists(self):
        """Test that idiomorph.js exists in static directory."""
        idiomorph_path = Path("src/storyville/components/layout/static/idiomorph.js")
        assert idiomorph_path.exists(), "idiomorph.js should be bundled locally"
        assert idiomorph_path.stat().st_size > 0, "idiomorph.js should not be empty"


class TestReadStoryHTML:
    """Test reading HTML content for story-specific morphing."""

    def test_read_existing_story_html(self, tmp_path: Path):
        """Test reading HTML content from an existing story."""
        # Create a mock story directory structure
        story_dir = tmp_path / "components" / "heading" / "story-0"
        story_dir.mkdir(parents=True)

        # Create themed_story.html with sample content
        html_content = """<!DOCTYPE html>
<html>
<head><title>Test Story</title></head>
<body>
<h1>Test Heading</h1>
<p>Story content</p>
</body>
</html>"""
        (story_dir / "themed_story.html").write_text(html_content, encoding="utf-8")

        # Read the HTML
        result = read_story_html(tmp_path, "components/heading/story-0")

        assert result is not None
        assert "Test Story" in result
        assert "Test Heading" in result
        assert "Story content" in result

    def test_read_nonexistent_story_html(self, tmp_path: Path):
        """Test reading HTML from a non-existent story returns None."""
        result = read_story_html(tmp_path, "nonexistent/story-0")
        assert result is None

    def test_read_story_html_invalid_path(self, tmp_path: Path):
        """Test reading HTML with invalid story ID returns None."""
        result = read_story_html(tmp_path, "../../../etc/passwd")
        assert result is None


class TestStoryHTMLReading:
    """Test the read_story_html function."""

    def test_read_html_with_special_characters(self, tmp_path: Path):
        """Test reading HTML content with special characters."""
        story_dir = tmp_path / "components" / "test" / "story-0"
        story_dir.mkdir(parents=True)

        # Create HTML with special characters
        html_content = """<!DOCTYPE html>
<html>
<head><title>Test & "Quotes" <Tags></title></head>
<body>
<p>Content with & < > " ' special chars</p>
</body>
</html>"""
        (story_dir / "themed_story.html").write_text(html_content, encoding="utf-8")

        result = read_story_html(tmp_path, "components/test/story-0")

        assert result is not None
        assert "&" in result
        assert "<" in result
        assert '"' in result

    def test_read_html_large_file(self, tmp_path: Path):
        """Test reading large HTML file."""
        story_dir = tmp_path / "components" / "large" / "story-0"
        story_dir.mkdir(parents=True)

        # Create a large HTML file (> 100KB)
        large_content = "<!DOCTYPE html><html><body>"
        large_content += "<p>Content paragraph</p>" * 5000
        large_content += "</body></html>"

        (story_dir / "themed_story.html").write_text(large_content, encoding="utf-8")

        result = read_story_html(tmp_path, "components/large/story-0")

        assert result is not None
        assert len(result) > 100000
        assert "Content paragraph" in result


class TestFallbackChain:
    """Test fallback behavior when morphing fails."""

    def test_fallback_documented(self):
        """Test that fallback chain is documented in ws.mjs.

        The fallback chain should be:
        1. Try DOM morphing with idiomorph
        2. If morphing fails, fall back to iframe reload
        3. If iframe reload fails, fall back to full page reload
        """
        ws_mjs_path = Path("src/storyville/components/layout/static/ws.mjs")
        assert ws_mjs_path.exists()

        content = ws_mjs_path.read_text()

        # Check for fallback chain implementation
        assert "morphDOM" in content, "morphDOM function should exist"
        assert "reloadIframe" in content, "reloadIframe function should exist"
        assert "window.location.reload" in content, "Full reload fallback should exist"

        # Check for error handling
        assert "catch" in content or "try" in content, (
            "Error handling should be present"
        )


class TestLogging:
    """Test logging for morphing operations."""

    def test_logging_messages_present(self):
        """Test that appropriate logging messages are present in ws.mjs."""
        ws_mjs_path = Path("src/storyville/components/layout/static/ws.mjs")
        content = ws_mjs_path.read_text()

        # Check for logging statements
        assert "console.log" in content, "Console logging should be present"
        assert "console.error" in content, "Error logging should be present"

        # Check for specific log messages
        assert "DOM morphing" in content or "DOM morph" in content
        assert "fallback" in content.lower() or "Fallback" in content


class TestLayoutIntegration:
    """Test that idiomorph is properly loaded in Layout component."""

    def test_layout_loads_idiomorph(self):
        """Test that Layout component includes idiomorph script tag."""
        layout_path = Path("src/storyville/components/layout/layout.py")
        assert layout_path.exists()

        content = layout_path.read_text()

        # Check for idiomorph script tag
        assert "idiomorph.js" in content, "Layout should load idiomorph.js"
        assert "<script" in content, "Layout should have script tags"
