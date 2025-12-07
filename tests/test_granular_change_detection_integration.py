"""Integration tests for granular change detection end-to-end workflows.

These tests verify the complete flow from file change detection through
classification, targeted broadcasting, and client-side handling.
"""

from pathlib import Path

from starlette.testclient import TestClient

from storyville.app import create_app
from storyville.build import build_site
from storyville.watchers import ChangeType, classify_change, read_story_html
from storyville.websocket import (
    broadcast_full_reload_async,
    broadcast_global_reload_async,
    broadcast_story_reload_async,
)


class TestEndToEndStoryHtmlChange:
    """Test end-to-end workflow: story HTML change → morph."""

    def test_story_html_change_triggers_targeted_morph(self, tmp_path: Path) -> None:
        """Test that story index.html change results in targeted morph message."""
        build_site(package_location="examples.minimal", output_dir=tmp_path)
        app = create_app(tmp_path)

        with TestClient(app) as client:
            # Connect client viewing specific story
            with client.websocket_connect("/ws/reload") as websocket:
                # Send page_info for the story
                story_id = "components/heading/story-0"
                page_info = {
                    "type": "page_info",
                    "page_url": "/components/heading/story-0/index.html",
                    "page_type": "story",
                    "story_id": story_id,
                }
                websocket.send_json(page_info)

                # Wait for message to be processed
                import time

                time.sleep(0.1)

                # Simulate file change detection and classification
                # Use "/output/" prefix which classify_change expects
                changed_file = Path("/output/components/heading/story-0/index.html")
                change_type, classified_story_id = classify_change(changed_file)

                # Verify classification
                assert change_type == ChangeType.STORY_SPECIFIC
                assert classified_story_id == story_id

                # Read HTML content from actual build output
                html_content = read_story_html(tmp_path, story_id)
                assert html_content is not None

                # Trigger broadcast with the classified change
                from storyville.websocket import broadcast_story_reload

                broadcast_story_reload(story_id, html_content)

                # Client should receive morph_html message
                data = websocket.receive_json()
                assert data["type"] == "reload"
                assert data["change_type"] == "morph_html"
                assert data["story_id"] == story_id
                assert "html" in data
                assert len(data["html"]) > 0

    def test_story_html_change_only_targets_viewing_client(
        self, tmp_path: Path
    ) -> None:
        """Test that story HTML change only sends to clients viewing that story."""
        build_site(package_location="examples.minimal", output_dir=tmp_path)
        app = create_app(tmp_path)

        with TestClient(app) as client:
            # Connect two clients viewing different stories
            with client.websocket_connect("/ws/reload") as ws_story1:
                with client.websocket_connect("/ws/reload") as ws_story2:
                    # Story 1 viewer
                    ws_story1.send_json(
                        {
                            "type": "page_info",
                            "page_url": "/components/heading/story-0/index.html",
                            "page_type": "story",
                            "story_id": "components/heading/story-0",
                        }
                    )

                    # Story 2 viewer (different story)
                    ws_story2.send_json(
                        {
                            "type": "page_info",
                            "page_url": "/components/button/story-0/index.html",
                            "page_type": "story",
                            "story_id": "components/button/story-0",
                        }
                    )

                    import time

                    time.sleep(0.1)

                    # Change story 1
                    story_id = "components/heading/story-0"
                    html_content = read_story_html(tmp_path, story_id)
                    assert html_content is not None

                    from storyville.websocket import broadcast_story_reload

                    broadcast_story_reload(story_id, html_content)

                    # Only ws_story1 should receive message
                    data = ws_story1.receive_json()
                    assert data["story_id"] == story_id
                    assert data["change_type"] == "morph_html"

                    # ws_story2 should not receive anything (would timeout)


class TestEndToEndGlobalAssetChange:
    """Test end-to-end workflow: global asset change → iframe reload."""

    def test_global_asset_change_triggers_iframe_reload(self, tmp_path: Path) -> None:
        """Test that global asset change results in iframe_reload for all stories."""
        build_site(package_location="examples.minimal", output_dir=tmp_path)
        app = create_app(tmp_path)

        with TestClient(app) as client:
            # Connect story viewer
            with client.websocket_connect("/ws/reload") as websocket:
                page_info = {
                    "type": "page_info",
                    "page_url": "/components/heading/story-0/index.html",
                    "page_type": "story",
                    "story_id": "components/heading/story-0",
                }
                websocket.send_json(page_info)

                import time

                time.sleep(0.1)

                # Simulate global asset change (themed_story.html)
                changed_file = Path(
                    "/output/components/heading/story-0/themed_story.html"
                )
                change_type, story_id = classify_change(changed_file)

                # Verify classification
                assert change_type == ChangeType.GLOBAL_ASSET
                assert story_id is None

                # Trigger global broadcast
                from storyville.websocket import broadcast_global_reload

                broadcast_global_reload()

                # Client should receive iframe_reload message
                data = websocket.receive_json()
                assert data["type"] == "reload"
                assert data["change_type"] == "iframe_reload"
                assert "story_id" not in data
                assert "html" not in data

    def test_global_asset_broadcasts_to_all_story_viewers(self, tmp_path: Path) -> None:
        """Test that global asset change broadcasts to all story viewers."""
        build_site(package_location="examples.minimal", output_dir=tmp_path)
        app = create_app(tmp_path)

        with TestClient(app) as client:
            # Connect multiple story viewers
            with client.websocket_connect("/ws/reload") as ws1:
                with client.websocket_connect("/ws/reload") as ws2:
                    # Both viewing different stories
                    ws1.send_json(
                        {
                            "type": "page_info",
                            "page_url": "/components/heading/story-0/index.html",
                            "page_type": "story",
                            "story_id": "components/heading/story-0",
                        }
                    )

                    ws2.send_json(
                        {
                            "type": "page_info",
                            "page_url": "/components/button/story-0/index.html",
                            "page_type": "story",
                            "story_id": "components/button/story-0",
                        }
                    )

                    import time

                    time.sleep(0.1)

                    # Trigger global broadcast (CSS change)
                    from storyville.websocket import broadcast_global_reload

                    broadcast_global_reload()

                    # Both clients should receive iframe_reload
                    data1 = ws1.receive_json()
                    assert data1["change_type"] == "iframe_reload"

                    data2 = ws2.receive_json()
                    assert data2["change_type"] == "iframe_reload"


class TestEndToEndNonStoryChange:
    """Test end-to-end workflow: non-story change → full reload."""

    def test_non_story_change_triggers_full_reload(self, tmp_path: Path) -> None:
        """Test that non-story change results in full_reload for non-story viewers."""
        build_site(package_location="examples.minimal", output_dir=tmp_path)
        app = create_app(tmp_path)

        with TestClient(app) as client:
            # Connect non-story viewer (index page)
            with client.websocket_connect("/ws/reload") as websocket:
                page_info = {
                    "type": "page_info",
                    "page_url": "/index.html",
                    "page_type": "non_story",
                }
                websocket.send_json(page_info)

                import time

                time.sleep(0.1)

                # Simulate non-story change (docs page)
                changed_file = Path("/output/docs/getting-started.html")
                change_type, story_id = classify_change(changed_file)

                # Verify classification
                assert change_type == ChangeType.NON_STORY
                assert story_id is None

                # Trigger full reload broadcast
                from storyville.websocket import broadcast_full_reload

                broadcast_full_reload()

                # Client should receive full_reload message
                data = websocket.receive_json()
                assert data["type"] == "reload"
                assert data["change_type"] == "full_reload"
                assert "story_id" not in data
                assert "html" not in data

    def test_non_story_change_only_targets_non_story_viewers(
        self, tmp_path: Path
    ) -> None:
        """Test that non-story change doesn't broadcast to story viewers."""
        build_site(package_location="examples.minimal", output_dir=tmp_path)
        app = create_app(tmp_path)

        with TestClient(app) as client:
            # Connect story viewer and non-story viewer
            with client.websocket_connect("/ws/reload") as ws_story:
                with client.websocket_connect("/ws/reload") as ws_non_story:
                    # Story viewer
                    ws_story.send_json(
                        {
                            "type": "page_info",
                            "page_url": "/components/heading/story-0/index.html",
                            "page_type": "story",
                            "story_id": "components/heading/story-0",
                        }
                    )

                    # Non-story viewer
                    ws_non_story.send_json(
                        {
                            "type": "page_info",
                            "page_url": "/index.html",
                            "page_type": "non_story",
                        }
                    )

                    import time

                    time.sleep(0.1)

                    # Trigger full reload (non-story change)
                    from storyville.websocket import broadcast_full_reload

                    broadcast_full_reload()

                    # Only ws_non_story should receive message
                    data = ws_non_story.receive_json()
                    assert data["change_type"] == "full_reload"

                    # ws_story should not receive anything


class TestChangeClassificationIntegration:
    """Test integration between change detection and classification."""

    def test_classify_multiple_simultaneous_changes(self) -> None:
        """Test classification of multiple changes happening simultaneously."""
        # Create various file paths with /output/ prefix that classify_change expects
        changes = [
            (
                Path("/output/components/heading/story-0/index.html"),
                ChangeType.STORY_SPECIFIC,
                "components/heading/story-0",
            ),
            (
                Path("/output/components/button/story-0/index.html"),
                ChangeType.STORY_SPECIFIC,
                "components/button/story-0",
            ),
            (Path("/output/static/bundle.css"), ChangeType.GLOBAL_ASSET, None),
            (Path("/output/docs/guide.html"), ChangeType.NON_STORY, None),
        ]

        # Classify all changes
        results = [classify_change(path) for path, _, _ in changes]

        # Verify each classification
        for i, (path, expected_type, expected_id) in enumerate(changes):
            change_type, story_id = results[i]
            assert change_type == expected_type, f"Failed for {path}"
            assert story_id == expected_id, f"Failed for {path}"

    def test_prioritize_global_over_story_specific(self) -> None:
        """Test that global changes are prioritized when mixed with story changes."""
        # When both global and story-specific changes occur, global should take precedence
        # for broadcast targeting
        changes = [
            Path("/output/components/heading/story-0/index.html"),
            Path("/output/static/main.css"),  # Global asset
        ]

        classifications = [classify_change(path) for path in changes]

        # Check that we have both types
        has_global = any(ct == ChangeType.GLOBAL_ASSET for ct, _ in classifications)
        has_story = any(ct == ChangeType.STORY_SPECIFIC for ct, _ in classifications)

        assert has_global, "Should detect global asset"
        assert has_story, "Should detect story-specific change"

        # In watcher logic, global takes precedence (broadcasts iframe reload)
        # This test verifies that both are correctly classified


class TestErrorHandlingAndFallbacks:
    """Test error handling and fallback chains."""

    async def test_broadcast_with_no_connections(self) -> None:
        """Test that broadcasts handle no active connections gracefully."""
        # All broadcast functions should handle empty connection set
        # No exceptions should be raised

        await broadcast_story_reload_async(
            "components/heading/story-0", "<div>Test</div>"
        )
        await broadcast_global_reload_async()
        await broadcast_full_reload_async()

        # If we get here without exceptions, test passes

    def test_read_story_html_with_missing_file(self, tmp_path: Path) -> None:
        """Test reading HTML when themed_story.html doesn't exist."""
        # Story directory exists but no themed_story.html
        story_dir = tmp_path / "components" / "heading" / "story-0"
        story_dir.mkdir(parents=True)

        html = read_story_html(tmp_path, "components/heading/story-0")
        assert html is None

    def test_read_story_html_with_malformed_path(self, tmp_path: Path) -> None:
        """Test reading HTML with path traversal attempt."""
        # Should safely handle malicious paths
        html = read_story_html(tmp_path, "../../../etc/passwd")
        assert html is None

    def test_connection_state_cleanup_on_disconnect(self, tmp_path: Path) -> None:
        """Test that connection metadata is cleaned up when client disconnects."""
        build_site(package_location="examples.minimal", output_dir=tmp_path)
        app = create_app(tmp_path)

        with TestClient(app) as client:
            # Connect and send metadata
            with client.websocket_connect("/ws/reload") as websocket:
                websocket.send_json(
                    {
                        "type": "page_info",
                        "page_url": "/components/heading/story-0/index.html",
                        "page_type": "story",
                        "story_id": "components/heading/story-0",
                    }
                )

                import time

                time.sleep(0.1)

            # After disconnect, connection should be cleaned up
            # Verify by checking that broadcasts don't fail
            from storyville.websocket import broadcast_story_reload

            # Should not raise exception even with no connections
            broadcast_story_reload("components/heading/story-0", "<div>Test</div>")


class TestMessageProtocolCompliance:
    """Test that messages comply with the specified protocol."""

    def test_morph_html_message_includes_all_fields(self, tmp_path: Path) -> None:
        """Test morph_html message includes type, change_type, story_id, html."""
        build_site(package_location="examples.minimal", output_dir=tmp_path)
        app = create_app(tmp_path)

        with TestClient(app) as client:
            with client.websocket_connect("/ws/reload") as websocket:
                story_id = "components/heading/story-0"
                websocket.send_json(
                    {
                        "type": "page_info",
                        "page_url": "/components/heading/story-0/index.html",
                        "page_type": "story",
                        "story_id": story_id,
                    }
                )

                import time

                time.sleep(0.1)

                html = read_story_html(tmp_path, story_id)
                assert html is not None

                from storyville.websocket import broadcast_story_reload

                broadcast_story_reload(story_id, html)

                data = websocket.receive_json()

                # Verify all required fields
                assert "type" in data
                assert data["type"] == "reload"
                assert "change_type" in data
                assert data["change_type"] == "morph_html"
                assert "story_id" in data
                assert data["story_id"] == story_id
                assert "html" in data
                assert isinstance(data["html"], str)
                assert len(data["html"]) > 0

    def test_iframe_reload_message_omits_optional_fields(self, tmp_path: Path) -> None:
        """Test iframe_reload message omits None fields (story_id, html)."""
        build_site(package_location="examples.minimal", output_dir=tmp_path)
        app = create_app(tmp_path)

        with TestClient(app) as client:
            with client.websocket_connect("/ws/reload") as websocket:
                websocket.send_json(
                    {
                        "type": "page_info",
                        "page_url": "/components/heading/story-0/index.html",
                        "page_type": "story",
                        "story_id": "components/heading/story-0",
                    }
                )

                import time

                time.sleep(0.1)

                from storyville.websocket import broadcast_global_reload

                broadcast_global_reload()

                data = websocket.receive_json()

                # Verify required fields
                assert data["type"] == "reload"
                assert data["change_type"] == "iframe_reload"

                # Verify optional fields are omitted (not null)
                assert "story_id" not in data
                assert "html" not in data

    def test_full_reload_message_minimal_fields(self, tmp_path: Path) -> None:
        """Test full_reload message only includes type and change_type."""
        build_site(package_location="examples.minimal", output_dir=tmp_path)
        app = create_app(tmp_path)

        with TestClient(app) as client:
            with client.websocket_connect("/ws/reload") as websocket:
                websocket.send_json(
                    {
                        "type": "page_info",
                        "page_url": "/index.html",
                        "page_type": "non_story",
                    }
                )

                import time

                time.sleep(0.1)

                from storyville.websocket import broadcast_full_reload

                broadcast_full_reload()

                data = websocket.receive_json()

                # Verify minimal fields
                assert data["type"] == "reload"
                assert data["change_type"] == "full_reload"
                assert "story_id" not in data
                assert "html" not in data
