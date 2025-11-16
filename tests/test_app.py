"""Tests for the Starlette application factory."""

from pathlib import Path

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
