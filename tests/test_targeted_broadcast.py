"""Tests for targeted broadcast system (Task Group 3)."""

import json
from pathlib import Path

from starlette.testclient import TestClient

from storyville.app import create_app
from storyville.build import build_site
from storyville.websocket import (
    ReloadMessage,
    broadcast_full_reload,
    broadcast_global_reload,
    broadcast_story_reload,
)


def test_reload_message_serialization() -> None:
    """Test ReloadMessage dataclass JSON serialization."""
    # Test morph_html message with all fields
    message = ReloadMessage(
        type="reload",
        change_type="morph_html",
        story_id="components/heading/story-0",
        html="<div>Updated content</div>",
    )
    json_str = message.to_json()
    data = json.loads(json_str)

    assert data["type"] == "reload"
    assert data["change_type"] == "morph_html"
    assert data["story_id"] == "components/heading/story-0"
    assert data["html"] == "<div>Updated content</div>"

    # Test iframe_reload message without story_id or html
    message = ReloadMessage(type="reload", change_type="iframe_reload")
    json_str = message.to_json()
    data = json.loads(json_str)

    assert data["type"] == "reload"
    assert data["change_type"] == "iframe_reload"
    assert "story_id" not in data  # None values should be omitted
    assert "html" not in data

    # Test full_reload message
    message = ReloadMessage(type="reload", change_type="full_reload")
    json_str = message.to_json()
    data = json.loads(json_str)

    assert data["type"] == "reload"
    assert data["change_type"] == "full_reload"
    assert "story_id" not in data
    assert "html" not in data


def test_broadcast_story_reload_filters_to_story_viewers(tmp_path: Path) -> None:
    """Test broadcast_story_reload only sends to connections viewing the specific story."""
    build_site(package_location="examples.minimal", output_dir=tmp_path)
    app = create_app(tmp_path)

    with TestClient(app) as client:
        # Connect three clients with different page metadata
        with client.websocket_connect("/ws/reload") as ws_story1:
            with client.websocket_connect("/ws/reload") as ws_story2:
                with client.websocket_connect("/ws/reload") as ws_non_story:
                    # Send page_info for story 1 viewer
                    ws_story1.send_text(
                        json.dumps(
                            {
                                "type": "page_info",
                                "page_url": "/components/heading/story-0/index.html",
                                "page_type": "story",
                                "story_id": "components/heading/story-0",
                            }
                        )
                    )

                    # Send page_info for story 2 viewer (different story)
                    ws_story2.send_text(
                        json.dumps(
                            {
                                "type": "page_info",
                                "page_url": "/components/button/story-0/index.html",
                                "page_type": "story",
                                "story_id": "components/button/story-0",
                            }
                        )
                    )

                    # Send page_info for non-story viewer
                    ws_non_story.send_text(
                        json.dumps(
                            {
                                "type": "page_info",
                                "page_url": "/index.html",
                                "page_type": "non_story",
                            }
                        )
                    )

                    # Give server time to process messages
                    import time

                    time.sleep(0.1)

                    # Broadcast story reload for story 1
                    html_content = "<div>Updated story 1 content</div>"
                    broadcast_story_reload("components/heading/story-0", html_content)

                    # Only ws_story1 should receive the message
                    data = ws_story1.receive_json()
                    assert data["type"] == "reload"
                    assert data["change_type"] == "morph_html"
                    assert data["story_id"] == "components/heading/story-0"
                    assert data["html"] == html_content

                    # ws_story2 and ws_non_story should not receive anything
                    # (no messages in their queue)


def test_broadcast_global_reload_targets_all_story_viewers(tmp_path: Path) -> None:
    """Test broadcast_global_reload sends iframe_reload to all story page viewers."""
    build_site(package_location="examples.minimal", output_dir=tmp_path)
    app = create_app(tmp_path)

    with TestClient(app) as client:
        # Connect three clients
        with client.websocket_connect("/ws/reload") as ws_story1:
            with client.websocket_connect("/ws/reload") as ws_story2:
                with client.websocket_connect("/ws/reload") as ws_non_story:
                    # Send page_info for story viewers
                    ws_story1.send_text(
                        json.dumps(
                            {
                                "type": "page_info",
                                "page_url": "/components/heading/story-0/index.html",
                                "page_type": "story",
                                "story_id": "components/heading/story-0",
                            }
                        )
                    )

                    ws_story2.send_text(
                        json.dumps(
                            {
                                "type": "page_info",
                                "page_url": "/components/button/story-0/index.html",
                                "page_type": "story",
                                "story_id": "components/button/story-0",
                            }
                        )
                    )

                    # Send page_info for non-story viewer
                    ws_non_story.send_text(
                        json.dumps(
                            {
                                "type": "page_info",
                                "page_url": "/index.html",
                                "page_type": "non_story",
                            }
                        )
                    )

                    # Give server time to process messages
                    import time

                    time.sleep(0.1)

                    # Broadcast global reload (affects all story viewers)
                    broadcast_global_reload()

                    # Both story viewers should receive iframe_reload message
                    data1 = ws_story1.receive_json()
                    assert data1["type"] == "reload"
                    assert data1["change_type"] == "iframe_reload"
                    assert "story_id" not in data1
                    assert "html" not in data1

                    data2 = ws_story2.receive_json()
                    assert data2["type"] == "reload"
                    assert data2["change_type"] == "iframe_reload"
                    assert "story_id" not in data2
                    assert "html" not in data2

                    # ws_non_story should not receive anything


def test_broadcast_full_reload_targets_non_story_viewers(tmp_path: Path) -> None:
    """Test broadcast_full_reload sends full_reload to non-story page viewers."""
    build_site(package_location="examples.minimal", output_dir=tmp_path)
    app = create_app(tmp_path)

    with TestClient(app) as client:
        # Connect three clients
        with client.websocket_connect("/ws/reload") as ws_story:
            with client.websocket_connect("/ws/reload") as ws_non_story1:
                with client.websocket_connect("/ws/reload") as ws_non_story2:
                    # Send page_info for story viewer
                    ws_story.send_text(
                        json.dumps(
                            {
                                "type": "page_info",
                                "page_url": "/components/heading/story-0/index.html",
                                "page_type": "story",
                                "story_id": "components/heading/story-0",
                            }
                        )
                    )

                    # Send page_info for non-story viewers
                    ws_non_story1.send_text(
                        json.dumps(
                            {
                                "type": "page_info",
                                "page_url": "/index.html",
                                "page_type": "non_story",
                            }
                        )
                    )

                    ws_non_story2.send_text(
                        json.dumps(
                            {
                                "type": "page_info",
                                "page_url": "/docs/guide.html",
                                "page_type": "non_story",
                            }
                        )
                    )

                    # Give server time to process messages
                    import time

                    time.sleep(0.1)

                    # Broadcast full reload (affects non-story viewers)
                    broadcast_full_reload()

                    # Both non-story viewers should receive full_reload message
                    data1 = ws_non_story1.receive_json()
                    assert data1["type"] == "reload"
                    assert data1["change_type"] == "full_reload"
                    assert "story_id" not in data1
                    assert "html" not in data1

                    data2 = ws_non_story2.receive_json()
                    assert data2["type"] == "reload"
                    assert data2["change_type"] == "full_reload"
                    assert "story_id" not in data2
                    assert "html" not in data2

                    # ws_story should not receive anything


def test_broadcast_story_reload_with_no_matching_viewers(tmp_path: Path) -> None:
    """Test broadcast_story_reload handles case with no viewers for the target story."""
    build_site(package_location="examples.minimal", output_dir=tmp_path)
    app = create_app(tmp_path)

    with TestClient(app) as client:
        # Connect a client viewing a different story
        with client.websocket_connect("/ws/reload") as websocket:
            # Send page_info for different story
            websocket.send_text(
                json.dumps(
                    {
                        "type": "page_info",
                        "page_url": "/components/button/story-0/index.html",
                        "page_type": "story",
                        "story_id": "components/button/story-0",
                    }
                )
            )

            # Give server time to process messages
            import time

            time.sleep(0.1)

            # Broadcast story reload for different story (no matching viewers)
            # Should not raise exception
            broadcast_story_reload(
                "components/heading/story-0", "<div>Updated content</div>"
            )

            # No message should be sent to this client


def test_broadcast_with_no_connections(tmp_path: Path) -> None:
    """Test broadcast functions handle no active connections gracefully."""
    build_site(package_location="examples.minimal", output_dir=tmp_path)
    _ = create_app(tmp_path)

    # All broadcast functions should handle no connections without raising
    broadcast_story_reload("components/heading/story-0", "<div>Content</div>")
    broadcast_global_reload()
    broadcast_full_reload()


def test_reload_message_format_matches_spec() -> None:
    """Test that ReloadMessage format matches the spec requirements."""
    # Test all three message types match spec format

    # 1. morph_html message
    morph_msg = ReloadMessage(
        type="reload",
        change_type="morph_html",
        story_id="components/heading/story-0",
        html="<div>Content</div>",
    )
    morph_data = json.loads(morph_msg.to_json())
    assert morph_data == {
        "type": "reload",
        "change_type": "morph_html",
        "story_id": "components/heading/story-0",
        "html": "<div>Content</div>",
    }

    # 2. iframe_reload message
    iframe_msg = ReloadMessage(type="reload", change_type="iframe_reload")
    iframe_data = json.loads(iframe_msg.to_json())
    assert iframe_data == {
        "type": "reload",
        "change_type": "iframe_reload",
    }

    # 3. full_reload message
    full_msg = ReloadMessage(type="reload", change_type="full_reload")
    full_data = json.loads(full_msg.to_json())
    assert full_data == {
        "type": "reload",
        "change_type": "full_reload",
    }
