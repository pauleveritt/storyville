"""Tests for static folder discovery."""

from pathlib import Path


from storyville.static_assets.discovery import discover_static_folders


def test_discover_static_folders_finds_single_folder(tmp_path: Path) -> None:
    """Test discovery finds a single static folder."""
    # Create a test directory structure
    component_dir = tmp_path / "components" / "nav"
    static_dir = component_dir / "static"
    static_dir.mkdir(parents=True)

    # Create a file in the static directory
    (static_dir / "style.css").write_text("body { }")

    # Discover static folders
    folders = discover_static_folders(tmp_path, "storyville")

    # Verify results
    assert len(folders) == 1
    assert folders[0].source_path == static_dir
    assert folders[0].source_type == "storyville"
    assert folders[0].relative_path == Path("components/nav")


def test_discover_static_folders_finds_multiple_folders(tmp_path: Path) -> None:
    """Test discovery finds multiple static folders."""
    # Create multiple static directories
    nav_static = tmp_path / "components" / "nav" / "static"
    nav_static.mkdir(parents=True)

    button_static = tmp_path / "components" / "button" / "static"
    button_static.mkdir(parents=True)

    layout_static = tmp_path / "layouts" / "default" / "static"
    layout_static.mkdir(parents=True)

    # Discover static folders
    folders = discover_static_folders(tmp_path, "input_dir")

    # Verify results
    assert len(folders) == 3
    folder_paths = {f.relative_path for f in folders}
    assert Path("components/nav") in folder_paths
    assert Path("components/button") in folder_paths
    assert Path("layouts/default") in folder_paths

    # Verify all have correct source type
    for folder in folders:
        assert folder.source_type == "input_dir"


def test_discover_static_folders_empty_directory(tmp_path: Path) -> None:
    """Test discovery returns empty list for directory with no static folders."""
    # Create directory without static folders
    component_dir = tmp_path / "components" / "nav"
    component_dir.mkdir(parents=True)

    # Discover static folders
    folders = discover_static_folders(tmp_path, "storyville")

    # Verify no folders found
    assert len(folders) == 0


def test_discover_static_folders_nonexistent_directory() -> None:
    """Test discovery handles nonexistent directory gracefully."""
    nonexistent = Path("/nonexistent/path")

    # Discover static folders
    folders = discover_static_folders(nonexistent, "storyville")

    # Verify empty list returned
    assert len(folders) == 0


def test_discover_static_folders_ignores_static_files(tmp_path: Path) -> None:
    """Test discovery ignores files named 'static'."""
    # Create a file named "static"
    component_dir = tmp_path / "components" / "nav"
    component_dir.mkdir(parents=True)
    (component_dir / "static").write_text("not a directory")

    # Create an actual static directory
    real_static = tmp_path / "components" / "button" / "static"
    real_static.mkdir(parents=True)

    # Discover static folders
    folders = discover_static_folders(tmp_path, "storyville")

    # Verify only directory found
    assert len(folders) == 1
    assert folders[0].relative_path == Path("components/button")


def test_discover_static_folders_nested_structure(tmp_path: Path) -> None:
    """Test discovery handles deeply nested static folders."""
    # Create deeply nested structure
    deep_static = tmp_path / "a" / "b" / "c" / "d" / "static"
    deep_static.mkdir(parents=True)

    # Discover static folders
    folders = discover_static_folders(tmp_path, "storyville")

    # Verify correct relative path
    assert len(folders) == 1
    assert folders[0].relative_path == Path("a/b/c/d")
    assert folders[0].source_path == deep_static


def test_discover_static_folders_preserves_full_path(tmp_path: Path) -> None:
    """Test discovery preserves complete directory structure for collision prevention."""
    # Create two components with similar structure
    nav_static = tmp_path / "components" / "navigation" / "tree" / "static"
    nav_static.mkdir(parents=True)

    nav2_static = tmp_path / "components" / "navigation" / "breadcrumb" / "static"
    nav2_static.mkdir(parents=True)

    # Discover static folders
    folders = discover_static_folders(tmp_path, "storyville")

    # Verify full paths preserved
    assert len(folders) == 2
    relative_paths = {f.relative_path for f in folders}
    assert Path("components/navigation/tree") in relative_paths
    assert Path("components/navigation/breadcrumb") in relative_paths
