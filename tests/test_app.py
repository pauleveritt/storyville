"""Tests for the Starlette application factory."""

import asyncio
from pathlib import Path
from unittest.mock import patch

from starlette.applications import Starlette
from starlette.testclient import TestClient

from storytime.app import create_app
from storytime.build import build_site


# Task Group 1 Tests: Application Factory


def test_create_app_accepts_path_parameter(tmp_path: Path) -> None:
    """Test that create_app accepts Path parameter."""
    build_site(package_location="storytime", output_dir=tmp_path)
    app = create_app(tmp_path)
    assert app is not None


def test_create_app_returns_starlette_instance(tmp_path: Path) -> None:
    """Test that create_app returns Starlette instance."""
    build_site(package_location="storytime", output_dir=tmp_path)
    app = create_app(tmp_path)
    assert isinstance(app, Starlette)


def test_create_app_sets_debug_true(tmp_path: Path) -> None:
    """Test that app has debug=True."""
    build_site(package_location="storytime", output_dir=tmp_path)
    app = create_app(tmp_path)
    assert app.debug is True


def test_create_app_serves_from_provided_path(tmp_path: Path) -> None:
    """Test that app serves from provided path."""
    build_site(package_location="storytime", output_dir=tmp_path)
    app = create_app(tmp_path)
    client = TestClient(app)
    # Simple check that we can make a request
    response = client.get("/")
    assert response.status_code == 200


# Task Group 2 Tests: Static File Serving


def test_serve_index_at_root(tmp_path: Path) -> None:
    """Test serving index.html at root path /."""
    build_site(package_location="storytime", output_dir=tmp_path)
    app = create_app(tmp_path)
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200
    assert "Storytime UI" in response.text
    assert "<html" in response.text


def test_serve_section_page(tmp_path: Path) -> None:
    """Test serving section index at /section/components/."""
    build_site(package_location="storytime", output_dir=tmp_path)
    app = create_app(tmp_path)
    client = TestClient(app)

    response = client.get("/section/components/")
    assert response.status_code == 200
    assert "Components" in response.text


def test_serve_static_asset(tmp_path: Path) -> None:
    """Test serving static asset at /static/pico-main.css."""
    build_site(package_location="storytime", output_dir=tmp_path)
    app = create_app(tmp_path)
    client = TestClient(app)

    response = client.get("/static/pico-main.css")
    assert response.status_code == 200
    assert "pico" in response.text


def test_404_for_nonexistent_path(tmp_path: Path) -> None:
    """Test 404 for non-existent path."""
    build_site(package_location="storytime", output_dir=tmp_path)
    app = create_app(tmp_path)
    client = TestClient(app)

    response = client.get("/this/path/does/not/exist/")
    assert response.status_code == 404


def test_directory_request_resolves_to_index_html(tmp_path: Path) -> None:
    """Test that directory requests resolve to index.html via html=True."""
    build_site(package_location="storytime", output_dir=tmp_path)
    app = create_app(tmp_path)
    client = TestClient(app)

    # Request a section directory - should resolve to index.html
    response = client.get("/section/components/")
    assert response.status_code == 200
    assert "<html" in response.text


# Task Group 3 Tests: Additional Coverage


def test_serve_subject_page(tmp_path: Path) -> None:
    """Test serving subject page at deeper path."""
    build_site(package_location="storytime", output_dir=tmp_path)
    app = create_app(tmp_path)
    client = TestClient(app)

    response = client.get("/section/components/component_view/")
    assert response.status_code == 200
    assert "Component View" in response.text


def test_serve_story_page(tmp_path: Path) -> None:
    """Test serving individual story page."""
    build_site(package_location="storytime", output_dir=tmp_path)
    app = create_app(tmp_path)
    client = TestClient(app)

    response = client.get("/section/components/component_view/story-0/")
    assert response.status_code == 200
    assert "Default Story" in response.text or "Story" in response.text


# Task Group 5 Tests: Lifespan Integration


def test_app_starts_without_watchers_when_params_not_provided(tmp_path: Path) -> None:
    """Test that app starts cleanly without watchers when optional params not provided."""
    build_site(package_location="storytime", output_dir=tmp_path)
    app = create_app(tmp_path)  # No watcher params

    # Should be able to use TestClient which triggers lifespan
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200


def test_app_starts_with_watchers_when_all_params_provided(tmp_path: Path) -> None:
    """Test that app starts with watchers when all required params provided."""
    build_site(package_location="storytime", output_dir=tmp_path)

    with patch("storytime.app.watch_input_directory") as mock_input_watch, \
         patch("storytime.app.watch_output_directory") as mock_output_watch:
        # Make the mock watchers run forever until cancelled
        async def mock_watcher(*args, **kwargs):
            try:
                while True:
                    await asyncio.sleep(0.1)
            except asyncio.CancelledError:
                pass

        mock_input_watch.return_value = mock_watcher()
        mock_output_watch.return_value = mock_watcher()

        app = create_app(
            path=tmp_path,
            input_path="storytime",
            package_location="storytime",
            output_dir=tmp_path,
        )

        # TestClient triggers lifespan startup and shutdown
        with TestClient(app) as client:
            response = client.get("/")
            assert response.status_code == 200

        # Verify watchers were started
        assert mock_input_watch.called
        assert mock_output_watch.called


def test_watchers_receive_correct_parameters(tmp_path: Path) -> None:
    """Test that watchers receive correct paths and callbacks."""
    build_site(package_location="storytime", output_dir=tmp_path)

    with patch("storytime.app.watch_input_directory") as mock_input_watch, \
         patch("storytime.app.watch_output_directory") as mock_output_watch, \
         patch("storytime.app.build_site") as mock_build, \
         patch("storytime.app.broadcast_reload") as mock_broadcast:

        # Make the mock watchers run forever until cancelled
        async def mock_watcher(*args, **kwargs):
            try:
                while True:
                    await asyncio.sleep(0.1)
            except asyncio.CancelledError:
                pass

        mock_input_watch.return_value = mock_watcher()
        mock_output_watch.return_value = mock_watcher()

        app = create_app(
            path=tmp_path,
            input_path="storytime",
            package_location="storytime",
            output_dir=tmp_path,
        )

        with TestClient(app):
            pass  # Just trigger lifespan

        # Verify INPUT watcher was called with correct parameters
        mock_input_watch.assert_called_once()
        call_kwargs = mock_input_watch.call_args[1]
        assert call_kwargs["package_location"] == "storytime"
        assert call_kwargs["output_dir"] == tmp_path
        assert call_kwargs["rebuild_callback"] == mock_build

        # Verify OUTPUT watcher was called with correct parameters
        mock_output_watch.assert_called_once()
        call_kwargs = mock_output_watch.call_args[1]
        assert call_kwargs["output_dir"] == tmp_path
        assert call_kwargs["broadcast_callback"] == mock_broadcast


def test_watchers_are_cancelled_on_shutdown(tmp_path: Path) -> None:
    """Test that watcher tasks are cancelled during app shutdown."""
    build_site(package_location="storytime", output_dir=tmp_path)

    input_cancelled = False
    output_cancelled = False

    async def mock_input_watcher(*args, **kwargs):
        nonlocal input_cancelled
        try:
            while True:
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            input_cancelled = True
            raise

    async def mock_output_watcher(*args, **kwargs):
        nonlocal output_cancelled
        try:
            while True:
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            output_cancelled = True
            raise

    with patch("storytime.app.watch_input_directory", side_effect=mock_input_watcher), \
         patch("storytime.app.watch_output_directory", side_effect=mock_output_watcher):

        app = create_app(
            path=tmp_path,
            input_path="storytime",
            package_location="storytime",
            output_dir=tmp_path,
        )

        # TestClient will start and stop the app
        with TestClient(app):
            pass

        # Verify both watchers were cancelled
        assert input_cancelled
        assert output_cancelled


def test_backward_compatibility_with_existing_tests(tmp_path: Path) -> None:
    """Test that existing tests not passing watcher params still work."""
    build_site(package_location="storytime", output_dir=tmp_path)

    # Old-style call without watcher parameters
    app = create_app(tmp_path)

    # Should work fine
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "Storytime UI" in response.text


def test_app_handles_partial_watcher_params_gracefully(tmp_path: Path) -> None:
    """Test that app doesn't start watchers if only some params are provided."""
    build_site(package_location="storytime", output_dir=tmp_path)

    with patch("storytime.app.watch_input_directory") as mock_input_watch, \
         patch("storytime.app.watch_output_directory") as mock_output_watch:

        # Only provide some params (not all required)
        app = create_app(
            path=tmp_path,
            input_path="storytime",
            # Missing package_location and output_dir
        )

        with TestClient(app) as client:
            response = client.get("/")
            assert response.status_code == 200

        # Watchers should NOT have been started
        assert not mock_input_watch.called
        assert not mock_output_watch.called
