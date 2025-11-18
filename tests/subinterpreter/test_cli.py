"""Tests for CLI integration with subinterpreters."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from storytime.__main__ import app as cli_app


@pytest.fixture
def runner() -> CliRunner:
    """Create a CLI runner for testing."""
    return CliRunner()


def test_serve_command_without_flag(runner: CliRunner, tmp_path: Path) -> None:
    """Test serve command without --use-subinterpreters flag (default behavior)."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Mock uvicorn.run and build_site to avoid actually starting server
    with (
        patch("storytime.__main__.uvicorn.run"),
        patch("storytime.__main__.build_site"),
        patch("storytime.__main__.create_app") as mock_create_app,
    ):
        mock_create_app.return_value = MagicMock()

        # Run serve command without flag
        result = runner.invoke(
            cli_app,
            ["serve", "examples.minimal", str(output_dir)],
        )

        # Should succeed
        assert result.exit_code == 0

        # create_app should be called with use_subinterpreters=False (default)
        mock_create_app.assert_called_once()
        call_kwargs = mock_create_app.call_args.kwargs
        assert call_kwargs.get("use_subinterpreters", False) is False


def test_serve_command_with_flag_enabled(runner: CliRunner, tmp_path: Path) -> None:
    """Test serve command with --use-subinterpreters flag."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Mock uvicorn.run and build_site to avoid actually starting server
    with (
        patch("storytime.__main__.uvicorn.run"),
        patch("storytime.__main__.build_site"),
        patch("storytime.__main__.create_app") as mock_create_app,
    ):
        mock_create_app.return_value = MagicMock()

        # Run serve command with flag
        result = runner.invoke(
            cli_app,
            ["serve", "--use-subinterpreters", "examples.minimal", str(output_dir)],
        )

        # Should succeed
        assert result.exit_code == 0

        # create_app should be called with use_subinterpreters=True
        mock_create_app.assert_called_once()
        call_kwargs = mock_create_app.call_args.kwargs
        assert call_kwargs.get("use_subinterpreters") is True


def test_build_command_uses_direct_build(runner: CliRunner, tmp_path: Path) -> None:
    """Test build command always uses direct build_site (no subinterpreters)."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Mock build_site to avoid actual build
    with patch("storytime.__main__.build_site") as mock_build:
        # Run build command
        result = runner.invoke(
            cli_app,
            ["build", "examples.minimal", str(output_dir)],
        )

        # Should succeed
        assert result.exit_code == 0

        # build_site should be called directly (not through subinterpreter)
        mock_build.assert_called_once()
        assert mock_build.call_args.kwargs["package_location"] == "examples.minimal"
        assert mock_build.call_args.kwargs["output_dir"] == Path(output_dir).resolve()
