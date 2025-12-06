"""Tests for StaticFolder dataclass."""

from pathlib import Path

from storyville.static_assets.models import StaticFolder


def test_static_folder_output_prefix_storyville() -> None:
    """Test output_prefix returns 'storyville_static' for storyville source."""
    folder = StaticFolder(
        source_path=Path("src/storyville/components/nav/static"),
        source_type="storyville",
        relative_path=Path("components/nav"),
    )

    assert folder.output_prefix == "storyville_static"


def test_static_folder_output_prefix_input_dir() -> None:
    """Test output_prefix returns 'static' for input_dir source."""
    folder = StaticFolder(
        source_path=Path("examples/minimal/components/button/static"),
        source_type="input_dir",
        relative_path=Path("components/button"),
    )

    assert folder.output_prefix == "static"


def test_static_folder_calculate_output_path_storyville() -> None:
    """Test calculate_output_path for storyville source."""
    folder = StaticFolder(
        source_path=Path("src/storyville/components/nav/static"),
        source_type="storyville",
        relative_path=Path("components/nav"),
    )

    output_path = folder.calculate_output_path(Path("output"))

    assert output_path == Path("output/storyville_static/components/nav/static")


def test_static_folder_calculate_output_path_input_dir() -> None:
    """Test calculate_output_path for input_dir source."""
    folder = StaticFolder(
        source_path=Path("examples/minimal/components/button/static"),
        source_type="input_dir",
        relative_path=Path("components/button"),
    )

    output_path = folder.calculate_output_path(Path("output"))

    assert output_path == Path("output/static/components/button/static")


def test_static_folder_calculate_output_path_preserves_full_structure() -> None:
    """Test calculate_output_path preserves full directory structure."""
    folder = StaticFolder(
        source_path=Path("src/storyville/components/navigation/tree/static"),
        source_type="storyville",
        relative_path=Path("components/navigation/tree"),
    )

    output_path = folder.calculate_output_path(Path("build"))

    assert output_path == Path(
        "build/storyville_static/components/navigation/tree/static"
    )
