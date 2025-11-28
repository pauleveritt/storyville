"""Tests for HTML path rewriting utilities using tree walker approach."""

from pathlib import Path

from tdom import html

from storytime.static_assets.rewriting import (
    build_discovered_assets_map,
    calculate_relative_static_path,
    resolve_static_asset_path,
    rewrite_static_paths,
    validate_static_reference,
)


# Task 2.1: Tests for relative path calculation
class TestCalculateRelativeStaticPath:
    """Tests for calculate_relative_static_path function."""

    def test_depth_0_input_dir_source(self) -> None:
        """Test relative path calculation at depth 0 for input_dir source."""
        result = calculate_relative_static_path(
            "static/components/nav/static/nav.css", 0, "input_dir"
        )
        assert result == "../static/components/nav/static/nav.css"

    def test_depth_1_input_dir_source(self) -> None:
        """Test relative path calculation at depth 1 for input_dir source."""
        result = calculate_relative_static_path(
            "static/components/nav/static/nav.css", 1, "input_dir"
        )
        assert result == "../../static/components/nav/static/nav.css"

    def test_depth_2_input_dir_source(self) -> None:
        """Test relative path calculation at depth 2 for input_dir source."""
        result = calculate_relative_static_path(
            "static/components/nav/static/nav.css", 2, "input_dir"
        )
        assert result == "../../../static/components/nav/static/nav.css"

    def test_depth_3_input_dir_source(self) -> None:
        """Test relative path calculation at depth 3 for input_dir source."""
        result = calculate_relative_static_path(
            "static/components/nav/static/nav.css", 3, "input_dir"
        )
        assert result == "../../../../static/components/nav/static/nav.css"

    def test_depth_0_storytime_source(self) -> None:
        """Test relative path calculation at depth 0 for storytime source."""
        result = calculate_relative_static_path(
            "storytime_static/layout/static/style.css", 0, "storytime"
        )
        assert result == "../storytime_static/layout/static/style.css"

    def test_depth_1_storytime_source(self) -> None:
        """Test relative path calculation at depth 1 for storytime source."""
        result = calculate_relative_static_path(
            "storytime_static/layout/static/style.css", 1, "storytime"
        )
        assert result == "../../storytime_static/layout/static/style.css"

    def test_depth_2_storytime_source(self) -> None:
        """Test relative path calculation at depth 2 for storytime source."""
        result = calculate_relative_static_path(
            "storytime_static/layout/static/style.css", 2, "storytime"
        )
        assert result == "../../../storytime_static/layout/static/style.css"


# Task 2.2-2.4: Tests for tree walker-based path rewriting
class TestRewriteStaticPaths:
    """Tests for rewrite_static_paths function using tree walker."""

    def test_rewrite_script_src(self) -> None:
        """Test rewriting script src attributes."""
        node = html(t'<div><script src="static/app.js"></script></div>')
        assets = {"static/app.js": Path("static/components/app/static/app.js")}
        result = rewrite_static_paths(node, page_depth=2, discovered_assets=assets)
        assert "../../../static/components/app/static/app.js" in str(result)

    def test_rewrite_link_href(self) -> None:
        """Test rewriting link href attributes."""
        node = html(t'<div><link href="static/style.css" /></div>')
        assets = {"static/style.css": Path("static/components/nav/static/style.css")}
        result = rewrite_static_paths(node, page_depth=1, discovered_assets=assets)
        assert "../../static/components/nav/static/style.css" in str(result)

    def test_rewrite_img_src(self) -> None:
        """Test rewriting img src attributes."""
        node = html(t'<div><img src="static/logo.png" /></div>')
        assets = {"static/logo.png": Path("static/components/brand/static/logo.png")}
        result = rewrite_static_paths(node, page_depth=0, discovered_assets=assets)
        assert "../static/components/brand/static/logo.png" in str(result)

    def test_rewrite_storytime_static(self) -> None:
        """Test rewriting storytime_static prefixed paths."""
        node = html(t'<div><script src="storytime_static/app.js"></script></div>')
        assets = {
            "storytime_static/app.js": Path(
                "storytime_static/components/app/static/app.js"
            )
        }
        result = rewrite_static_paths(node, page_depth=2, discovered_assets=assets)
        assert "../../../storytime_static/components/app/static/app.js" in str(result)

    def test_rewrite_multiple_references(self) -> None:
        """Test rewriting multiple static references."""
        node = html(t'''
        <div>
            <link href="static/style.css" />
            <script src="storytime_static/app.js"></script>
            <img src="static/logo.png" />
        </div>
        ''')
        assets = {
            "static/style.css": Path("static/components/nav/static/style.css"),
            "storytime_static/app.js": Path(
                "storytime_static/components/app/static/app.js"
            ),
            "static/logo.png": Path("static/components/brand/static/logo.png"),
        }
        result = rewrite_static_paths(node, page_depth=2, discovered_assets=assets)
        result_str = str(result)
        assert "../../../static/components/nav/static/style.css" in result_str
        assert "../../../storytime_static/components/app/static/app.js" in result_str
        assert "../../../static/components/brand/static/logo.png" in result_str

    def test_ignore_external_urls(self) -> None:
        """Test that external URLs are not rewritten."""
        node = html(t'<div><script src="https://cdn.example.com/app.js"></script></div>')
        assets = {}
        result = rewrite_static_paths(node, page_depth=2, discovered_assets=assets)
        assert "https://cdn.example.com/app.js" in str(result)

    def test_ignore_absolute_paths(self) -> None:
        """Test that absolute paths are not rewritten."""
        node = html(t'<div><link href="/assets/style.css" /></div>')
        assets = {}
        result = rewrite_static_paths(node, page_depth=2, discovered_assets=assets)
        assert "/assets/style.css" in str(result)

    def test_nested_elements(self) -> None:
        """Test rewriting in deeply nested elements."""
        node = html(t'''
        <div>
            <div>
                <div>
                    <link href="static/nested.css" />
                </div>
            </div>
        </div>
        ''')
        assets = {"static/nested.css": Path("static/components/deep/static/nested.css")}
        result = rewrite_static_paths(node, page_depth=2, discovered_assets=assets)
        assert "../../../static/components/deep/static/nested.css" in str(result)

    def test_preserves_other_attributes(self) -> None:
        """Test that other attributes are preserved."""
        node = html(t'<div><link rel="stylesheet" href="static/style.css" type="text/css" /></div>')
        assets = {"static/style.css": Path("static/components/nav/static/style.css")}
        result = rewrite_static_paths(node, page_depth=1, discovered_assets=assets)
        result_str = str(result)
        assert 'rel="stylesheet"' in result_str
        assert 'type="text/css"' in result_str

    def test_missing_asset_not_rewritten(self) -> None:
        """Test that missing assets are not rewritten."""
        node = html(t'<div><link href="static/missing.css" /></div>')
        assets = {}
        result = rewrite_static_paths(node, page_depth=2, discovered_assets=assets)
        # Should remain unchanged since asset not found
        assert "static/missing.css" in str(result)


# Task 2.5: Tests for asset path resolution
class TestResolveStaticAssetPath:
    """Tests for resolve_static_asset_path function."""

    def test_resolve_direct_match(self) -> None:
        """Test resolving a direct match in discovered assets."""
        assets = {
            "static/nav.css": Path("output/static/components/nav/static/nav.css")
        }
        result = resolve_static_asset_path("static/nav.css", assets)
        assert result == "output/static/components/nav/static/nav.css"

    def test_resolve_by_filename(self) -> None:
        """Test resolving by filename when exact match not found."""
        assets = {
            "static/components/nav/static/nav.css": Path(
                "output/static/components/nav/static/nav.css"
            )
        }
        result = resolve_static_asset_path("static/nav.css", assets)
        assert result == "output/static/components/nav/static/nav.css"

    def test_resolve_storytime_static(self) -> None:
        """Test resolving storytime_static prefixed assets."""
        assets = {
            "storytime_static/app.js": Path(
                "output/storytime_static/components/app/static/app.js"
            )
        }
        result = resolve_static_asset_path("storytime_static/app.js", assets)
        assert result == "output/storytime_static/components/app/static/app.js"

    def test_resolve_not_found(self) -> None:
        """Test resolving when asset is not found."""
        assets = {"static/nav.css": Path("output/static/nav.css")}
        result = resolve_static_asset_path("static/missing.css", assets)
        assert result is None


# Task 2.7: Tests for validation
class TestValidateStaticReference:
    """Tests for validate_static_reference function."""

    def test_validate_found_asset(self) -> None:
        """Test validation of a found asset."""
        assets = {"static/nav.css": Path("output/static/nav.css")}
        is_valid, result = validate_static_reference("static/nav.css", assets)
        assert is_valid is True
        assert result == "output/static/nav.css"

    def test_validate_missing_asset(self) -> None:
        """Test validation of a missing asset."""
        assets = {"static/nav.css": Path("output/static/nav.css")}
        is_valid, error = validate_static_reference("static/missing.css", assets)
        assert is_valid is False
        assert error is not None
        assert "Asset not found" in error


# Task 2.4: Tests for main rewrite function
# Task 2.6: Tests for building discovered assets map
class TestBuildDiscoveredAssetsMap:
    """Tests for build_discovered_assets_map function."""

    def test_build_assets_map_from_discovery(self, tmp_path: Path) -> None:
        """Test building assets map from discovered static folders."""
        # Create test directory structure
        storytime_base = tmp_path / "src" / "storytime"
        input_dir = tmp_path / "input"
        output_dir = tmp_path / "output"

        # Create a storytime static folder with a file
        st_static = storytime_base / "components" / "nav" / "static"
        st_static.mkdir(parents=True)
        (st_static / "nav.css").write_text("/* nav styles */")

        # Create an input_dir static folder with a file
        input_static = input_dir / "components" / "button" / "static"
        input_static.mkdir(parents=True)
        (input_static / "button.css").write_text("/* button styles */")

        # Build the assets map
        assets = build_discovered_assets_map(storytime_base, input_dir, output_dir)

        # Verify storytime asset is in map
        assert "storytime_static/nav.css" in assets

        # Verify input_dir asset is in map
        assert "static/button.css" in assets

    def test_empty_directories(self, tmp_path: Path) -> None:
        """Test building assets map with no static folders."""
        storytime_base = tmp_path / "src" / "storytime"
        input_dir = tmp_path / "input"
        output_dir = tmp_path / "output"

        # Create empty directories
        storytime_base.mkdir(parents=True)
        input_dir.mkdir(parents=True)

        # Build the assets map
        assets = build_discovered_assets_map(storytime_base, input_dir, output_dir)

        # Should return empty dict
        assert len(assets) == 0

    def test_nonexistent_directories(self, tmp_path: Path) -> None:
        """Test building assets map with nonexistent directories."""
        storytime_base = tmp_path / "nonexistent_storytime"
        input_dir = tmp_path / "nonexistent_input"
        output_dir = tmp_path / "output"

        # Build the assets map (should not crash)
        assets = build_discovered_assets_map(storytime_base, input_dir, output_dir)

        # Should return empty dict
        assert len(assets) == 0


# Integration tests
class TestRewritingIntegration:
    """Integration tests for the complete rewriting workflow."""

    def test_end_to_end_rewriting(self, tmp_path: Path) -> None:
        """Test complete workflow from discovery to rewriting."""
        # Setup: Create test directory structure
        storytime_base = tmp_path / "src" / "storytime"
        input_dir = tmp_path / "input"
        output_dir = tmp_path / "output"

        # Create static folders with files
        st_static = storytime_base / "components" / "nav" / "static"
        st_static.mkdir(parents=True)
        (st_static / "nav.css").write_text("/* nav */")

        # Build assets map
        assets = build_discovered_assets_map(storytime_base, input_dir, output_dir)

        # Create HTML referencing the asset (using tdom node)
        node = html(t'<div><link rel="stylesheet" href="storytime_static/nav.css" /></div>')

        # Rewrite paths
        result = rewrite_static_paths(node, 2, assets)

        # Verify the path was rewritten correctly
        assert "../../../storytime_static/components/nav/static/nav.css" in str(result)

    def test_complex_html_document(self, tmp_path: Path) -> None:
        """Test rewriting in a complex HTML document."""
        # Setup
        storytime_base = tmp_path / "src" / "storytime"
        input_dir = tmp_path / "input"
        output_dir = tmp_path / "output"

        # Create multiple static files
        st_static = storytime_base / "layout" / "static"
        st_static.mkdir(parents=True)
        (st_static / "style.css").write_text("/* style */")
        (st_static / "app.js").write_text("// app")

        in_static = input_dir / "components" / "button" / "static"
        in_static.mkdir(parents=True)
        (in_static / "button.css").write_text("/* button */")

        # Build assets map
        assets = build_discovered_assets_map(storytime_base, input_dir, output_dir)

        # Complex HTML (using tdom node)
        node = html(t"""
        <html>
        <head>
            <link rel="stylesheet" href="storytime_static/style.css" />
            <link rel="stylesheet" href="static/button.css" />
            <script src="storytime_static/app.js"></script>
        </head>
        <body>
            <h1>Test</h1>
        </body>
        </html>
        """)

        # Rewrite paths at depth 1
        result = rewrite_static_paths(node, 1, assets)

        # Verify all paths were rewritten
        result_str = str(result)
        assert "../../storytime_static/layout/static/style.css" in result_str
        assert "../../static/components/button/static/button.css" in result_str
        assert "../../storytime_static/layout/static/app.js" in result_str
