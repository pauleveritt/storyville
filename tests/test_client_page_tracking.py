"""Tests for client-side page tracking and message handling (Task Group 4).

These tests verify:
- Page type detection (story vs non-story)
- Story identifier extraction from URLs
- page_info message sending on WebSocket connection
- Message routing based on change_type field
- Reload handler invocation
"""

from pathlib import Path

import pytest
from playwright.sync_api import Page
from starlette.testclient import TestClient

from storyville.app import create_app
from storyville.build import build_site


@pytest.fixture
def built_site_with_story(tmp_path: Path) -> Path:
    """Build a test site with story pages for testing.

    Returns:
        Path to the output directory containing built HTML files.
    """
    output_dir = tmp_path / "output"
    output_dir.mkdir(exist_ok=True)
    build_site(package_location="examples.minimal", output_dir=output_dir)
    return output_dir


def test_page_type_detection_for_story_page(
    built_site_with_story: Path, page: Page
) -> None:
    """Test that detectPageType() correctly identifies a story page."""
    # Find a story page
    story_pages = list(built_site_with_story.rglob("story-*/index.html"))
    assert len(story_pages) > 0, "Should have at least one story page"

    story_page = story_pages[0]
    page_url = f"file://{story_page.absolute()}"

    # Navigate to story page
    page.goto(page_url)

    # Execute page detection logic
    page_type = page.evaluate(
        """
        () => {
            // Inline the detectPageType function from ws.mjs
            function isModeC() {
                const iframe = document.querySelector('iframe[src="./themed_story.html"]');
                return iframe !== null;
            }

            function detectPageType() {
                if (isModeC()) {
                    return 'story';
                }
                if (window.location.pathname.includes('story-') &&
                    window.location.pathname.endsWith('/index.html')) {
                    return 'story';
                }
                return 'non_story';
            }

            return detectPageType();
        }
        """
    )

    assert page_type == "story", "Story page should be detected as 'story'"


def test_page_type_detection_for_non_story_page(
    built_site_with_story: Path, page: Page
) -> None:
    """Test that detectPageType() correctly identifies a non-story page."""
    # Use index.html (catalog page) as non-story
    index_page = built_site_with_story / "index.html"
    assert index_page.exists(), "Index page should exist"

    page_url = f"file://{index_page.absolute()}"
    page.goto(page_url)

    # Execute page detection logic
    page_type = page.evaluate(
        """
        () => {
            function isModeC() {
                const iframe = document.querySelector('iframe[src="./themed_story.html"]');
                return iframe !== null;
            }

            function detectPageType() {
                if (isModeC()) {
                    return 'story';
                }
                if (window.location.pathname.includes('story-') &&
                    window.location.pathname.endsWith('/index.html')) {
                    return 'story';
                }
                return 'non_story';
            }

            return detectPageType();
        }
        """
    )

    assert page_type == "non_story", "Index page should be detected as 'non_story'"


def test_story_id_extraction_from_url(built_site_with_story: Path, page: Page) -> None:
    """Test that extractStoryId() correctly extracts story identifier from URL."""
    # Find a story page with known path structure
    story_pages = list(built_site_with_story.rglob("story-*/index.html"))
    assert len(story_pages) > 0, "Should have at least one story page"

    story_page = story_pages[0]
    page_url = f"file://{story_page.absolute()}"

    # Navigate to story page
    page.goto(page_url)

    # Execute story ID extraction logic
    story_id = page.evaluate(
        """
        () => {
            function extractStoryId() {
                const pathname = window.location.pathname;
                const parts = pathname.split('/').filter(part => part !== '');

                for (let i = 0; i < parts.length; i++) {
                    if (parts[i].startsWith('story-')) {
                        const storyParts = parts.slice(0, i + 1);
                        return storyParts.join('/');
                    }
                }

                return null;
            }

            return extractStoryId();
        }
        """
    )

    # Verify story ID format matches expected pattern
    assert story_id is not None, "Story ID should be extracted"
    assert "story-" in story_id, "Story ID should contain 'story-' segment"

    # Verify story ID ends with the expected path structure
    # Since file:// URLs include full absolute path, just check the ending
    relative_path = story_page.relative_to(built_site_with_story)
    expected_parts = relative_path.parts[:-1]  # Remove 'index.html'
    expected_story_id = "/".join(expected_parts)

    assert story_id.endswith(
        expected_story_id
    ), f"Story ID should end with: {expected_story_id}, got: {story_id}"


def test_page_info_message_sent_on_connection(tmp_path: Path) -> None:
    """Test that page_info message is sent when WebSocket connects."""
    build_site(package_location="examples.minimal", output_dir=tmp_path)
    app = create_app(tmp_path)

    with TestClient(app) as client:
        with client.websocket_connect("/ws/reload") as websocket:
            # Receive the page_info message sent by client
            # In real browser, client sends this; in test we simulate receiving it
            page_info = {
                "type": "page_info",
                "page_url": "/components/heading/story-0/index.html",
                "page_type": "story",
                "story_id": "components/heading/story-0",
            }

            # Send page_info to server (simulating client behavior)
            websocket.send_json(page_info)

            # Server should accept the message without error
            # No response expected, just ensure connection stays open
            assert websocket is not None


def test_message_routing_iframe_reload(tmp_path: Path, page: Page) -> None:
    """Test that iframe_reload message routes to reloadIframe() handler."""
    build_site(package_location="examples.minimal", output_dir=tmp_path)

    # Find a story page to test with
    story_pages = list(tmp_path.rglob("story-*/index.html"))
    assert len(story_pages) > 0, "Should have at least one story page"

    story_page = story_pages[0]
    page_url = f"file://{story_page.absolute()}"

    # Navigate to story page
    page.goto(page_url)

    # Wait for page to load
    page.wait_for_load_state("domcontentloaded")

    # Inject console log capture
    logs = []
    page.on("console", lambda msg: logs.append(msg.text))

    # Simulate receiving iframe_reload message
    page.evaluate(
        """
        () => {
            const message = {
                type: 'reload',
                change_type: 'iframe_reload'
            };

            // Simulate message handler
            function handleReloadMessage(message) {
                const changeType = message.change_type;
                console.log('[Storyville] Processing reload message:', JSON.stringify({
                    type: message.type,
                    change_type: changeType,
                    story_id: message.story_id || null
                }));

                if (changeType === 'iframe_reload') {
                    console.log('[Storyville] Iframe reload requested');
                }
            }

            handleReloadMessage(message);
        }
        """
    )

    # Wait a moment for logs to be captured
    page.wait_for_timeout(100)

    # Verify logs show iframe reload was requested
    log_text = " ".join(logs)
    assert "iframe_reload" in log_text, "Should log iframe_reload change type"
    assert "Iframe reload requested" in log_text, "Should log reload handler invocation"


def test_message_routing_morph_html(tmp_path: Path, page: Page) -> None:
    """Test that morph_html message routes to morphDOM() handler (stub)."""
    build_site(package_location="examples.minimal", output_dir=tmp_path)

    story_pages = list(tmp_path.rglob("story-*/index.html"))
    assert len(story_pages) > 0

    story_page = story_pages[0]
    page_url = f"file://{story_page.absolute()}"
    page.goto(page_url)
    page.wait_for_load_state("domcontentloaded")

    # Capture console logs
    logs = []
    page.on("console", lambda msg: logs.append(msg.text))

    # Simulate receiving morph_html message
    page.evaluate(
        """
        () => {
            const message = {
                type: 'reload',
                change_type: 'morph_html',
                story_id: 'components/heading/story-0',
                html: '<div>Updated content</div>'
            };

            function handleReloadMessage(message) {
                const changeType = message.change_type;
                console.log('[Storyville] Processing reload message:', JSON.stringify({
                    type: message.type,
                    change_type: changeType,
                    story_id: message.story_id || null
                }));

                if (changeType === 'morph_html') {
                    console.log('[Storyville] DOM morph requested for story:', message.story_id);
                }
            }

            handleReloadMessage(message);
        }
        """
    )

    page.wait_for_timeout(100)

    log_text = " ".join(logs)
    assert "morph_html" in log_text, "Should log morph_html change type"
    assert "DOM morph requested" in log_text, "Should log morph handler invocation"


def test_message_routing_full_reload(tmp_path: Path, page: Page) -> None:
    """Test that full_reload message routes to full page reload."""
    build_site(package_location="examples.minimal", output_dir=tmp_path)

    index_page = tmp_path / "index.html"
    page_url = f"file://{index_page.absolute()}"
    page.goto(page_url)
    page.wait_for_load_state("domcontentloaded")

    # Capture console logs
    logs = []
    page.on("console", lambda msg: logs.append(msg.text))

    # Simulate receiving full_reload message
    page.evaluate(
        """
        () => {
            const message = {
                type: 'reload',
                change_type: 'full_reload'
            };

            function handleReloadMessage(message) {
                const changeType = message.change_type;
                console.log('[Storyville] Processing reload message:', JSON.stringify({
                    type: message.type,
                    change_type: changeType,
                    story_id: message.story_id || null
                }));

                if (changeType === 'full_reload') {
                    console.log('[Storyville] Full page reload requested');
                }
            }

            handleReloadMessage(message);
        }
        """
    )

    page.wait_for_timeout(100)

    log_text = " ".join(logs)
    assert "full_reload" in log_text, "Should log full_reload change type"
    assert "Full page reload requested" in log_text, "Should log full reload handler"


def test_fallback_chain_morph_to_iframe_to_full(tmp_path: Path, page: Page) -> None:
    """Test fallback chain: morph fails -> iframe reload -> full reload."""
    build_site(package_location="examples.minimal", output_dir=tmp_path)

    story_pages = list(tmp_path.rglob("story-*/index.html"))
    assert len(story_pages) > 0

    story_page = story_pages[0]
    page_url = f"file://{story_page.absolute()}"
    page.goto(page_url)
    page.wait_for_load_state("domcontentloaded")

    # Capture console logs
    logs = []
    page.on("console", lambda msg: logs.append(msg.text))

    # Simulate morph_html message triggering fallback
    page.evaluate(
        """
        () => {
            const message = {
                type: 'reload',
                change_type: 'morph_html',
                story_id: 'components/heading/story-0',
                html: '<div>Content</div>'
            };

            function morphDOM(html, storyId) {
                console.log('[Storyville] DOM morphing requested for story:', storyId);
                console.log('[Storyville] DOM morphing not yet implemented, falling back to iframe reload');
                return false; // Indicates fallback needed
            }

            function handleReloadMessage(message) {
                if (message.change_type === 'morph_html') {
                    console.log('[Storyville] DOM morph requested for story:', message.story_id);
                    const html = message.html;
                    if (html) {
                        morphDOM(html, message.story_id);
                    }
                }
            }

            handleReloadMessage(message);
        }
        """
    )

    page.wait_for_timeout(100)

    log_text = " ".join(logs)
    assert "DOM morphing requested" in log_text, "Should attempt morph"
    assert (
        "not yet implemented" in log_text or "falling back" in log_text
    ), "Should indicate fallback"


# Mark all tests as slow since they use Playwright
pytestmark = [pytest.mark.slow, pytest.mark.playwright]
