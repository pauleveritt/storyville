"""Final strategic gap-filling tests for full static paths feature.

This test module addresses critical gaps in test coverage:
1. End-to-end workflows with both storytime and input_dir sources
2. Opt-in utility function behavior validation
3. Error handling for missing assets
4. Hot reload functionality verification
5. Performance validation with multiple assets

Maximum 10 strategic tests to complement existing coverage from Task Groups 1-3.
"""

from pathlib import Path

import pytest
from storytime.static_assets import (
    build_discovered_assets_map,
    copy_all_static_assets,
    rewrite_static_paths,
)
from storytime.watchers import STATIC_EXTENSIONS
from tdom import html


@pytest.fixture
def mock_storytime_static(tmp_path: Path) -> Path:
    """Create mock storytime static assets structure."""
    storytime_base = tmp_path / "src" / "storytime"
    layout_static = storytime_base / "components" / "layout" / "static"
    layout_static.mkdir(parents=True)
    (layout_static / "style.css").write_text("/* layout styles */")
    (layout_static / "app.js").write_text("// layout script")
    return storytime_base


@pytest.fixture
def mock_input_static(tmp_path: Path) -> Path:
    """Create mock input_dir static assets structure."""
    input_dir = tmp_path / "input"
    button_static = input_dir / "components" / "button" / "static"
    button_static.mkdir(parents=True)
    (button_static / "button.css").write_text("/* button styles */")
    (button_static / "icon.svg").write_text("<svg></svg>")
    return input_dir


def test_end_to_end_both_sources_copied(
    mock_storytime_static: Path, mock_input_static: Path, tmp_path: Path
) -> None:
    """Test end-to-end: both storytime and input_dir assets are discovered and copied.

    Critical gap: Validates complete workflow with both asset sources.
    """
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Copy all static assets from both sources
    output_paths = copy_all_static_assets(
        storytime_base=mock_storytime_static,
        input_dir=mock_input_static,
        output_dir=output_dir,
    )

    # Verify both sources were processed
    assert len(output_paths) == 2

    # Verify storytime assets in storytime_static/
    storytime_output = (
        output_dir / "storytime_static" / "components" / "layout" / "static"
    )
    assert storytime_output.exists()
    assert (storytime_output / "style.css").exists()
    assert (storytime_output / "app.js").exists()

    # Verify input_dir assets in static/
    input_output = output_dir / "static" / "components" / "button" / "static"
    assert input_output.exists()
    assert (input_output / "button.css").exists()
    assert (input_output / "icon.svg").exists()


def test_rewrite_static_paths_with_mixed_references(
    mock_storytime_static: Path, mock_input_static: Path, tmp_path: Path
) -> None:
    """Test path rewriting handles references to both storytime and input_dir assets.

    Critical gap: Validates rewriting works with both asset source types.
    """
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Setup assets
    copy_all_static_assets(
        storytime_base=mock_storytime_static,
        input_dir=mock_input_static,
        output_dir=output_dir,
    )

    # Build asset map
    asset_map = build_discovered_assets_map(
        mock_storytime_static, mock_input_static, output_dir
    )

    # Create HTML with references to both sources
    node = html(t'''
<html>
<head>
    <link rel="stylesheet" href="storytime_static/components/layout/static/style.css" />
    <link rel="stylesheet" href="static/components/button/static/button.css" />
</head>
<body>
    <script src="storytime_static/components/layout/static/app.js"></script>
    <img src="static/components/button/static/icon.svg" />
</body>
</html>
''')

    # Rewrite paths at depth 1
    rewritten = rewrite_static_paths(node, page_depth=1, discovered_assets=asset_map)
    html_str = str(rewritten)

    # Verify both types of references were rewritten with correct relative paths
    assert "../../storytime_static/components/layout/static/style.css" in html_str
    assert "../../static/components/button/static/button.css" in html_str
    assert "../../storytime_static/components/layout/static/app.js" in html_str
    assert "../../static/components/button/static/icon.svg" in html_str


def test_opt_in_behavior_without_calling_rewrite(tmp_path: Path) -> None:
    """Test that components NOT calling rewrite_static_paths keep original paths.

    Critical gap: Validates opt-in behavior - paths unchanged without explicit call.
    """
    # Create HTML with static references
    original_html = html(t'''
<html>
<head>
    <link rel="stylesheet" href="storytime_static/style.css" />
</head>
<body>
    <img src="static/icon.svg" />
</body>
</html>
''')

    # Convert to string WITHOUT calling rewrite_static_paths
    html_str = str(original_html)

    # Verify paths are unchanged (no relative path prefix)
    assert 'href="storytime_static/style.css"' in html_str
    assert 'src="static/icon.svg"' in html_str
    assert "../" not in html_str


def test_rewrite_preserves_non_static_references(
    mock_storytime_static: Path, mock_input_static: Path, tmp_path: Path
) -> None:
    """Test that rewriting preserves external URLs and absolute paths.

    Critical gap: Validates that only static/ and storytime_static/ prefixes are rewritten.
    """
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    copy_all_static_assets(
        mock_storytime_static, mock_input_static, output_dir
    )
    asset_map = build_discovered_assets_map(
        mock_storytime_static, mock_input_static, output_dir
    )

    # Create HTML with mixed reference types
    node = html(t'''
<html>
<head>
    <link rel="stylesheet" href="https://cdn.example.com/style.css" />
    <link rel="stylesheet" href="/absolute/path/style.css" />
    <link rel="stylesheet" href="storytime_static/components/layout/static/style.css" />
</head>
<body>
    <img src="https://example.com/image.png" />
    <img src="/images/logo.png" />
    <img src="data:image/png;base64,ABC123" />
</body>
</html>
''')

    # Rewrite paths
    rewritten = rewrite_static_paths(node, page_depth=0, discovered_assets=asset_map)
    html_str = str(rewritten)

    # Verify external URLs and absolute paths are unchanged
    assert 'href="https://cdn.example.com/style.css"' in html_str
    assert 'href="/absolute/path/style.css"' in html_str
    assert 'src="https://example.com/image.png"' in html_str
    assert 'src="/images/logo.png"' in html_str
    assert 'src="data:image/png;base64,ABC123"' in html_str

    # Verify only static references were rewritten
    assert "../storytime_static/components/layout/static/style.css" in html_str


def test_rewrite_handles_missing_asset_gracefully(tmp_path: Path) -> None:
    """Test that rewriting handles references to non-existent assets gracefully.

    Critical gap: Validates error handling for missing assets.
    """
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Empty asset map (no assets discovered)
    asset_map: dict[str, Path] = {}

    # Create HTML with reference to non-existent asset
    node = html(t'''
<html>
<head>
    <link rel="stylesheet" href="storytime_static/nonexistent.css" />
</head>
</html>
''')

    # Rewrite should not crash, but leave path unchanged
    rewritten = rewrite_static_paths(node, page_depth=0, discovered_assets=asset_map)
    html_str = str(rewritten)

    # Path should remain unchanged (not found in asset_map)
    assert 'href="storytime_static/nonexistent.css"' in html_str


def test_static_extensions_include_common_types() -> None:
    """Test that STATIC_EXTENSIONS includes all common web asset types.

    Critical gap: Validates watcher monitors all necessary file types.
    """
    # Verify common static file extensions are included
    assert ".css" in STATIC_EXTENSIONS
    assert ".js" in STATIC_EXTENSIONS
    assert ".png" in STATIC_EXTENSIONS
    assert ".jpg" in STATIC_EXTENSIONS
    assert ".jpeg" in STATIC_EXTENSIONS
    assert ".svg" in STATIC_EXTENSIONS
    assert ".ico" in STATIC_EXTENSIONS
    assert ".gif" in STATIC_EXTENSIONS

    # Verify we're watching at least 8 types
    assert len(STATIC_EXTENSIONS) >= 8


def test_copy_multiple_static_folders_performance(tmp_path: Path) -> None:
    """Test that copying many static folders performs acceptably.

    Critical gap: Validates performance with realistic number of static assets.
    """
    import time

    storytime_base = tmp_path / "storytime"
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Create 10 components each with 5 static assets
    for i in range(10):
        for source_dir, source_type in [
            (storytime_base, "storytime"),
            (input_dir, "input"),
        ]:
            component_static = (
                source_dir / "components" / f"component_{i}" / "static"
            )
            component_static.mkdir(parents=True)
            for j in range(5):
                (component_static / f"asset_{j}.css").write_text(f"/* asset {j} */")

    # Measure copy time
    start = time.perf_counter()
    output_paths = copy_all_static_assets(
        storytime_base=storytime_base,
        input_dir=input_dir,
        output_dir=output_dir,
    )
    duration = time.perf_counter() - start

    # Verify all folders were copied
    assert len(output_paths) == 20  # 10 components * 2 sources

    # Performance assertion: should complete in under 1 second for 20 folders
    assert duration < 1.0, f"Copying took {duration:.2f}s, expected < 1.0s"


def test_rewrite_depth_calculation_comprehensive(
    mock_storytime_static: Path, mock_input_static: Path, tmp_path: Path
) -> None:
    """Test path rewriting at all depth levels (0, 1, 2, 3+).

    Critical gap: Comprehensive validation of depth-based relative path calculation.
    """
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    copy_all_static_assets(
        mock_storytime_static, mock_input_static, output_dir
    )
    asset_map = build_discovered_assets_map(
        mock_storytime_static, mock_input_static, output_dir
    )

    # Test at each depth level
    depth_expectations = {
        0: "../storytime_static/components/layout/static/style.css",
        1: "../../storytime_static/components/layout/static/style.css",
        2: "../../../storytime_static/components/layout/static/style.css",
        3: "../../../../storytime_static/components/layout/static/style.css",
    }

    for depth, expected_path in depth_expectations.items():
        # Create fresh node for each depth test (rewrite modifies in place)
        node = html(t'''
<html>
<head>
    <link rel="stylesheet" href="storytime_static/components/layout/static/style.css" />
</head>
</html>
''')
        rewritten = rewrite_static_paths(node, page_depth=depth, discovered_assets=asset_map)
        html_str = str(rewritten)
        assert (
            f'href="{expected_path}"' in html_str
        ), f"Depth {depth} failed: expected {expected_path}"


def test_build_asset_map_handles_empty_directories(tmp_path: Path) -> None:
    """Test that building asset map handles directories with no static folders.

    Critical gap: Validates graceful handling of empty/missing static directories.
    """
    storytime_base = tmp_path / "storytime"
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"

    # Create directories but no static folders
    storytime_base.mkdir(parents=True)
    input_dir.mkdir(parents=True)
    output_dir.mkdir(parents=True)

    # Should not crash with empty directories
    asset_map = build_discovered_assets_map(
        storytime_base, input_dir, output_dir
    )

    # Should return empty map
    assert isinstance(asset_map, dict)
    assert len(asset_map) == 0


def test_node_rewriting_preserves_structure(
    mock_storytime_static: Path, mock_input_static: Path, tmp_path: Path
) -> None:
    """Test that Node tree rewriting preserves all non-href/src attributes.

    Critical gap: Validates that rewriting doesn't corrupt HTML structure.
    """
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    copy_all_static_assets(
        mock_storytime_static, mock_input_static, output_dir
    )
    asset_map = build_discovered_assets_map(
        mock_storytime_static, mock_input_static, output_dir
    )

    # Create HTML with multiple attributes
    node = html(t'''
<html>
<head>
    <link
        rel="stylesheet"
        href="storytime_static/components/layout/static/style.css"
        type="text/css"
        media="screen"
    />
</head>
<body>
    <img
        src="static/components/button/static/icon.svg"
        alt="Button icon"
        width="32"
        height="32"
        class="icon"
    />
</body>
</html>
''')

    # Rewrite paths
    rewritten = rewrite_static_paths(node, page_depth=0, discovered_assets=asset_map)
    html_str = str(rewritten)

    # Verify other attributes are preserved
    assert 'rel="stylesheet"' in html_str
    assert 'type="text/css"' in html_str
    assert 'media="screen"' in html_str
    assert 'alt="Button icon"' in html_str
    assert 'width="32"' in html_str
    assert 'height="32"' in html_str
    assert 'class="icon"' in html_str

    # Verify paths were rewritten
    assert "../storytime_static/components/layout/static/style.css" in html_str
    assert "../static/components/button/static/icon.svg" in html_str
