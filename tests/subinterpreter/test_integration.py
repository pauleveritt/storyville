"""Tests for dual-mode integration of subinterpreters with the app."""

from pathlib import Path

import pytest
from starlette.testclient import TestClient

from storyville.app import create_app
from storyville.subinterpreter_pool import create_pool, shutdown_pool


def test_create_app_with_subinterpreters_disabled(tmp_path: Path) -> None:
    """Test create_app() with use_subinterpreters=False (explicit disable)."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Create index.html so StaticFiles has something to serve
    (output_dir / "index.html").write_text("<html><body>Test</body></html>")

    app = create_app(
        path=output_dir,
        use_subinterpreters=False,
    )

    # App should be created successfully
    assert app is not None

    # Verify app doesn't have pool in state (since we're not starting the lifespan)
    assert not hasattr(app.state, "pool")


def test_create_app_with_subinterpreters_enabled(tmp_path: Path) -> None:
    """Test create_app() with use_subinterpreters=True."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Create index.html so StaticFiles has something to serve
    (output_dir / "index.html").write_text("<html><body>Test</body></html>")

    app = create_app(
        path=output_dir,
        input_path="examples.minimal",
        package_location="examples.minimal",
        output_dir=output_dir,
        use_subinterpreters=True,
    )

    # App should be created successfully
    assert app is not None


@pytest.mark.slow
async def test_lifespan_creates_pool_when_enabled(tmp_path: Path) -> None:
    """Test that lifespan creates pool on startup when use_subinterpreters=True."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Create index.html
    (output_dir / "index.html").write_text("<html><body>Test</body></html>")

    app = create_app(
        path=output_dir,
        input_path="examples.minimal",
        package_location="examples.minimal",
        output_dir=output_dir,
        use_subinterpreters=True,
    )

    # Use TestClient to trigger lifespan
    with TestClient(app):
        # During lifespan, pool should be created and stored in app.state
        assert hasattr(app.state, "pool")
        assert app.state.pool is not None

    # After lifespan ends, pool should be shutdown


async def test_lifespan_skips_pool_when_disabled(tmp_path: Path) -> None:
    """Test that lifespan does not create pool when use_subinterpreters=False."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Create index.html
    (output_dir / "index.html").write_text("<html><body>Test</body></html>")

    app = create_app(
        path=output_dir,
        input_path="examples.minimal",
        package_location="examples.minimal",
        output_dir=output_dir,
        use_subinterpreters=False,
    )

    # Use TestClient to trigger lifespan
    with TestClient(app):
        # Pool should NOT be created when disabled
        assert not hasattr(app.state, "pool")


@pytest.mark.slow
async def test_async_callback_for_subinterpreter_builds(tmp_path: Path) -> None:
    """Test that async callback for subinterpreter builds works correctly."""
    from storyville.subinterpreter_pool import rebuild_callback_subinterpreter

    pool = create_pool()
    output_dir = tmp_path / "output"

    try:
        # Call the async callback
        await rebuild_callback_subinterpreter(
            package_location="examples.minimal",
            output_dir=output_dir,
            pool=pool,
        )

        # Verify build completed successfully
        assert output_dir.exists()
        assert (output_dir / "index.html").exists()

    finally:
        shutdown_pool(pool)


@pytest.mark.slow
async def test_watcher_with_subinterpreter_callback(tmp_path: Path) -> None:
    """Test that watcher integration works with subinterpreter callback."""
    from storyville.subinterpreter_pool import rebuild_callback_subinterpreter

    pool = create_pool()
    output_dir = tmp_path / "output"

    try:
        # Create a partial callback with pool bound
        async def rebuild_with_pool(package_location: str, output_dir: Path) -> None:
            await rebuild_callback_subinterpreter(package_location, output_dir, pool)

        # Test that callback works
        await rebuild_with_pool("examples.minimal", output_dir)

        # Verify output
        assert (output_dir / "index.html").exists()

    finally:
        shutdown_pool(pool)
