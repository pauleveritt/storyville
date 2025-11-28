"""Tests for path calculation utilities."""

from pathlib import Path

from storytime.static_assets.models import StaticFolder
from storytime.static_assets.paths import calculate_output_path


def test_calculate_output_path_storytime_source() -> None:
    """Test calculate_output_path with storytime source."""
    folder = StaticFolder(
        source_path=Path("src/storytime/components/nav/static"),
        source_type="storytime",
        relative_path=Path("components/nav"),
    )

    output_path = calculate_output_path(folder, Path("output"))

    assert output_path == Path("output/storytime_static/components/nav/static")


def test_calculate_output_path_input_dir_source() -> None:
    """Test calculate_output_path with input_dir source."""
    folder = StaticFolder(
        source_path=Path("examples/minimal/components/button/static"),
        source_type="input_dir",
        relative_path=Path("components/button"),
    )

    output_path = calculate_output_path(folder, Path("build"))

    assert output_path == Path("build/static/components/button/static")


def test_calculate_output_path_includes_static_suffix() -> None:
    """Test calculate_output_path includes final /static/ directory."""
    folder = StaticFolder(
        source_path=Path("src/storytime/layouts/default/static"),
        source_type="storytime",
        relative_path=Path("layouts/default"),
    )

    output_path = calculate_output_path(folder, Path("output"))

    # Verify path ends with /static
    assert output_path.name == "static"
    assert str(output_path).endswith("/layouts/default/static")


def test_calculate_output_path_delegates_to_static_folder() -> None:
    """Test calculate_output_path correctly delegates to StaticFolder method."""
    folder = StaticFolder(
        source_path=Path("test/static"),
        source_type="storytime",
        relative_path=Path("test"),
    )

    # Call both methods
    utility_result = calculate_output_path(folder, Path("output"))
    method_result = folder.calculate_output_path(Path("output"))

    # Results should be identical
    assert utility_result == method_result
