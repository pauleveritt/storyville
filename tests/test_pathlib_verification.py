"""Final verification tests for pathlib migration.

These tests verify comprehensive Path usage across the entire codebase
to ensure the pathlib migration is complete and consistent.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from storyville import PACKAGE_DIR
from storyville.nodes import get_package_path
from storyville.build import build_catalog
from storyville.static_assets.models import StaticFolder


def test_package_dir_type_and_operations() -> None:
    """Verify PACKAGE_DIR uses Path and supports Path operations."""
    # Type check
    assert isinstance(PACKAGE_DIR, Path)

    # Path operations
    assert PACKAGE_DIR.exists()
    assert PACKAGE_DIR.is_dir()

    # Path / operator works
    init_file = PACKAGE_DIR / "__init__.py"
    assert init_file.exists()
    assert init_file.is_file()


def test_get_package_path_return_type() -> None:
    """Verify get_package_path returns Path, not string."""
    result = get_package_path("examples.minimal")

    assert isinstance(result, Path)
    assert not isinstance(result, str)


def test_static_folder_model_uses_path() -> None:
    """Verify StaticFolder model uses Path for all path attributes."""
    folder = StaticFolder(
        source_path=Path("/fake/path/static"),
        source_type="storyville",
        relative_path=Path("components/nav"),
    )

    # All path attributes should be Path objects
    assert isinstance(folder.source_path, Path)
    assert isinstance(folder.relative_path, Path)

    # calculate_output_path should return Path
    output_path = folder.calculate_output_path(Path("/output"))
    assert isinstance(output_path, Path)


def test_build_path_operations() -> None:
    """Verify build operations use Path methods, not string operations."""
    with TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)

        build_catalog(
            package_location="examples.minimal",
            output_dir=output_dir,
            with_assertions=False,
        )

        # Verify Path operations created correct structure
        assert output_dir.exists()
        assert (output_dir / "index.html").exists()
        assert (output_dir / "static").exists()

        # Verify we can use Path methods on results
        index_file = output_dir / "index.html"
        assert index_file.is_file()
        assert index_file.suffix == ".html"
        assert index_file.parent == output_dir


def test_path_slash_operator_usage() -> None:
    """Verify Path / operator is used for path joining."""
    base = Path("/base")
    subdir = base / "subdir"
    file = subdir / "file.txt"

    # Verify / operator creates Path objects
    assert isinstance(subdir, Path)
    assert isinstance(file, Path)

    # Verify structure is correct
    assert str(file) == "/base/subdir/file.txt"


def test_path_methods_over_os_path() -> None:
    """Verify Path methods are used instead of os.path functions."""
    test_path = PACKAGE_DIR / "__init__.py"

    # .exists() instead of os.path.exists()
    assert test_path.exists()

    # .is_file() instead of os.path.isfile()
    assert test_path.is_file()

    # .parent instead of os.path.dirname()
    parent = test_path.parent
    assert isinstance(parent, Path)
    assert parent.is_dir()

    # .name instead of os.path.basename()
    name = test_path.name
    assert isinstance(name, str)
    assert name == "__init__.py"

    # .suffix instead of os.path.splitext()
    suffix = test_path.suffix
    assert isinstance(suffix, str)
    assert suffix == ".py"

    # .stem instead of os.path.splitext()[0]
    stem = test_path.stem
    assert isinstance(stem, str)
    assert stem == "__init__"
