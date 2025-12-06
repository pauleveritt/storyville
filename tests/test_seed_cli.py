"""Tests for the seed CLI command."""

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from storytime.__main__ import app

runner = CliRunner()


def test_seed_command_with_valid_small_size() -> None:
    """Test seed command accepts 'small' size argument."""
    with TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "test_catalog"
        result = runner.invoke(app, ["seed", "small", str(output_dir)])

        # Command should succeed (exit code 0)
        assert result.exit_code == 0
        # Should include feedback message
        assert "Generating small catalog" in result.stdout
        assert "Catalog generation complete!" in result.stdout


def test_seed_command_with_valid_medium_size() -> None:
    """Test seed command accepts 'medium' size argument."""
    with TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "test_catalog"
        result = runner.invoke(app, ["seed", "medium", str(output_dir)])

        assert result.exit_code == 0
        assert "Generating medium catalog" in result.stdout


def test_seed_command_with_valid_large_size() -> None:
    """Test seed command accepts 'large' size argument."""
    with TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "test_catalog"
        result = runner.invoke(app, ["seed", "large", str(output_dir)])

        assert result.exit_code == 0
        assert "Generating large catalog" in result.stdout


def test_seed_command_rejects_invalid_size() -> None:
    """Test seed command fails with invalid size argument."""
    with TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "test_catalog"
        result = runner.invoke(app, ["seed", "invalid", str(output_dir)])

        # Command should fail (non-zero exit code)
        assert result.exit_code != 0
        # Should include error message about invalid size
        assert "invalid" in result.stdout.lower() or "error" in result.stdout.lower()


def test_seed_command_fails_when_output_directory_exists() -> None:
    """Test seed command fails when output directory already exists."""
    with TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "existing_dir"
        # Create the directory first
        output_dir.mkdir()

        result = runner.invoke(app, ["seed", "small", str(output_dir)])

        # Command should fail
        assert result.exit_code != 0
        # Should include error message about existing directory
        assert "already exists" in result.stdout


def test_seed_command_creates_output_directory() -> None:
    """Test seed command creates the output directory structure."""
    with TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "new_catalog"

        # Directory should not exist yet
        assert not output_dir.exists()

        result = runner.invoke(app, ["seed", "small", str(output_dir)])

        # Command should succeed
        assert result.exit_code == 0
        # Directory should now exist
        assert output_dir.exists()
        assert output_dir.is_dir()
