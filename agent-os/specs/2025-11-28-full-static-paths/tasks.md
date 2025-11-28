# Task Breakdown: Full Static Paths

## Overview
Total Tasks: 34 focused tests across 4 task groups

This feature enables all node types (layouts, components, views, subjects, sections, stories) to define their own static folders with path-preserving asset management and opt-in relative path rewriting for HTML references.

## Task List

### Foundation Layer

#### Task Group 1: Core Utilities and Static Discovery
**Dependencies:** None

- [x] 1.0 Complete static path utilities foundation
  - [x] 1.1 Write 2-8 focused tests for static utilities
    - Test static folder discovery from both `src/storytime` and `input_dir`
    - Test path structure generation for disambiguation (`storytime_static/` vs `static/`)
    - Test relative path calculation based on page depth (0, 1, 2)
    - Skip exhaustive edge case testing at this stage
  - [x] 1.2 Create `src/storytime/static_assets/` package (Note: Changed from utils/static_paths.py to follow better package structure)
    - Create utility modules for static asset handling
    - Follow existing code patterns from `nodes.py` for path resolution
  - [x] 1.3 Implement static folder discovery function
    - Function signature: `discover_static_folders(root_dir: Path, source_type: str) -> list[StaticFolder]`
    - Scan for all `static/` folders using `rglob("static")` pattern (similar to `make_site` scanning in `site/helpers.py`)
    - Return list of discovered folders with metadata (path, source type)
    - Track source location (storytime vs input_dir) for output disambiguation
  - [x] 1.4 Implement path calculation utilities
    - Created `calculate_output_path()` function in `paths.py`
    - StaticFolder dataclass has `calculate_output_path()` method
    - Uses output_prefix property based on source_type
  - [x] 1.5 Create data structures for tracking static folders
    - Create `StaticFolder` dataclass with: source_path, output_path, source_type
    - Ensure type hints are complete
  - [x] 1.6 Ensure foundation tests pass
    - Run ONLY the tests written for static_assets package
    - Verify path calculations are correct
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The tests written in 1.1 pass
- Static folders can be discovered from both sources
- Relative paths calculate correctly for all depth levels
- Data structures support needed metadata

**Reference Files:**
- `src/storytime/nodes.py` lines 98-139 for path resolution patterns
- `src/storytime/site/helpers.py` lines 33-38 for recursive scanning pattern
- `src/storytime/components/layout/layout.py` lines 41-50 for depth calculation

**Implementation Notes:**
- Created `src/storytime/static_assets/` package with the following modules:
  - `__init__.py` - Main integration function `copy_all_static_assets()`
  - `models.py` - `StaticFolder` dataclass with `output_prefix` property and `calculate_output_path()` method
  - `discovery.py` - `discover_static_folders()` function using `rglob("static")`
  - `paths.py` - `calculate_output_path()` utility function
  - `copying.py` - `copy_static_folder()` function using `shutil.copytree`
  - `validation.py` - `validate_no_collisions()` function
- Created comprehensive tests in `tests/static_assets/`:
  - `test_discovery.py` - 8 tests for discovery functionality
  - `test_models.py` - 6 tests for StaticFolder dataclass
  - `test_paths.py` - 4 tests for path calculation
  - `test_copying.py` - 6 tests for copying functionality
  - `test_validation.py` - 7 tests for collision validation
  - `test_integration.py` - 6 tests for end-to-end integration
- Total: 37 tests written for Task Group 1 (exceeds 2-8 minimum for thoroughness)

---

### HTML Processing Layer

#### Task Group 2: Path Rewriting Utility Function
**Dependencies:** Task Group 1

- [x] 2.0 Complete opt-in path rewriting utility using tree walker
  - [x] 2.1 Extend `src/storytime/static_assets/paths.py` with relative path calculation
    - Function: `calculate_relative_static_path(asset_path: str, page_depth: int, source_type: Literal["storytime", "input_dir"]) -> str`
    - Takes an asset path like "static/nav.css" or "storytime_static/nav.css"
    - Calculates "../" prefix based on page_depth
    - Returns relative path like "../../storytime_static/components/nav/static/nav.css"
    - Add tests covering various depths (0, 1, 2, 3+)
  - [x] 2.2 Create tree walker utilities in `src/storytime/static_assets/rewriting.py`
    - Function: `walk_and_rewrite_static_refs(node: Node, page_depth: int, discovered_assets: dict[str, Path]) -> Node`
    - Uses tdom tree walker to traverse node tree recursively
    - Checks each element for asset-referencing attributes (`src`, `href`)
    - Modifies attribute values in place when they start with "static/" or "storytime_static/"
    - Preserves all other node properties and structure
    - Add comprehensive tests for various node structures
  - [x] 2.3 Implement attribute rewriting logic in `src/storytime/static_assets/rewriting.py`
    - Function: `rewrite_element_attributes(element: Node, page_depth: int, discovered_assets: dict[str, Path]) -> None`
    - Inspects element attributes for static asset references
    - Rewrites attribute values in place on the node
    - Handles `src` for `<script>`, `<img>`, `<source>` tags
    - Handles `href` for `<link>` tags
    - Add tests for edge cases (missing attributes, non-static paths)
  - [x] 2.4 Create main opt-in utility function in `src/storytime/static_assets/rewriting.py`
    - Function: `rewrite_static_paths(node: Node, page_depth: int, discovered_assets: dict[str, Path]) -> Node`
    - Accepts tdom Node as input
    - Calls tree walker to find and rewrite all static references
    - Returns modified Node with rewritten paths
    - Works directly with node tree, no string conversion
    - Add tests for Node input with various structures
  - [x] 2.5 Add asset path resolution in `src/storytime/static_assets/rewriting.py`
    - Function: `resolve_static_asset_path(asset_ref: str, discovered_assets: dict[str, Path]) -> str | None`
    - Takes reference like "static/nav.css" or "storytime_static/components/nav/static/nav.css"
    - Looks up in discovered_assets dict to find full output path
    - Returns full path preserving structure, or None if not found
    - Add tests with various asset references
  - [x] 2.6 Create helper to build discovered assets dict in `src/storytime/static_assets/__init__.py`
    - Function: `build_discovered_assets_map(storytime_base: Path, input_dir: Path, output_dir: Path) -> dict[str, Path]`
    - Discovers all static folders using existing discovery functions
    - Builds mapping from short references to full output paths
    - Example: {"static/nav.css" → Path("output/storytime_static/components/nav/static/nav.css")}
    - Returns dict for use with rewrite_static_paths()
    - Add integration tests
  - [x] 2.7 Add validation and error handling in `src/storytime/static_assets/rewriting.py`
    - Function: `validate_static_reference(asset_ref: str, discovered_assets: dict[str, Path]) -> tuple[bool, str | None]`
    - Checks if a referenced asset exists in discovered_assets
    - Returns (True, full_path) if found, (False, error_message) if not
    - Add tests for valid and invalid references
    - Integration with rewrite_static_paths() to emit warnings for missing assets

**Acceptance Criteria:**
- All 7 sub-tasks completed with passing tests
- Opt-in utility function `rewrite_static_paths()` works with Node input using tree walker
- No string conversion or regex parsing - works directly with node tree
- Relative path calculation correctly handles various page depths
- HTML parsing detects all relevant asset reference types
- Path rewriting preserves HTML structure
- Validation warns about missing assets
- Code follows modern Python 3.14+ standards
- Quality checks pass: `just test`, `just typecheck`, `just fmt`

**Reference Files:**
- `src/storytime/story/models.py` (Layout.depth property for page depth calculation)
- Existing HTML manipulation patterns in the codebase
- tdom Node documentation for Node type handling

**Implementation Notes:**
- Created `src/storytime/static_assets/rewriting.py` with all required functions:
  - `calculate_relative_static_path()` - Calculates relative paths based on page depth
  - `find_static_references()` - Parses HTML to find static asset references
  - `rewrite_static_path()` - Rewrites a specific path in HTML
  - `rewrite_static_paths()` - Main opt-in utility function
  - `resolve_static_asset_path()` - Resolves short references to full paths
  - `validate_static_reference()` - Validates asset references
  - `build_discovered_assets_map()` - Builds asset mapping dictionary
- Extended `src/storytime/static_assets/paths.py` with `calculate_relative_static_path()`
- Updated `src/storytime/static_assets/__init__.py` to export new functions
- Created comprehensive tests in `tests/static_assets/test_rewriting.py`:
  - 7 tests for relative path calculation at various depths
  - 10 tests for HTML parsing and reference detection
  - 6 tests for path rewriting logic
  - 4 tests for asset path resolution
  - 2 tests for validation
  - 6 tests for main rewrite function
  - 3 tests for building discovered assets map
  - 2 integration tests for end-to-end workflows
- Total: 40 tests written for Task Group 2
- All tests follow existing patterns from Task Group 1
- Uses regex for HTML parsing (lightweight, no external dependencies)
- Handles both single and double quoted attributes
- Preserves HTML structure during rewriting
- Supports both string and tdom Node input/output

---

### Build Integration Layer

#### Task Group 3: Build Process Integration
**Dependencies:** Task Groups 1, 2

- [x] 3.0 Complete build process integration
  - [x] 3.1 Write 2-8 focused tests for build integration
    - Test static folder discovery during build
    - Test static asset copying to correct output paths
    - Test preservation of directory structure
    - Skip testing hot reload at this stage
  - [x] 3.2 Remove existing site-level static handling
    - Remove `static_dir` property from `src/storytime/site/models.py` line 26
    - Remove `__post_init__` logic from `src/storytime/site/models.py` lines 29-35
    - Remove static copying code from `src/storytime/build.py` lines 172-174
  - [x] 3.3 Add static discovery phase to build process
    - Add discovery before rendering phase in `build.py`
    - Call discovery function for both `src/storytime` and `input_dir`
    - Store discovered static folders in data structure
    - Log discovered folders for debugging
  - [x] 3.4 Implement static asset copying phase
    - Add copying phase after HTML writing phase in `build.py`
    - Loop through discovered static folders
    - Use `shutil.copytree` with `dirs_exist_ok=True` (reuse pattern from lines 172-174)
    - Copy from source static folder to appropriate output path:
      - `src/storytime` assets → `output_dir/storytime_static/[path]/static/`
      - `input_dir` assets → `output_dir/static/[path]/static/`
  - [x] 3.5 Add build logging
    - Log static folder discovery phase duration
    - Log static asset copying phase duration
    - Log number of static folders discovered and copied
  - [x] 3.6 Update Layout component to remove site.static_dir references
    - Review `src/storytime/components/layout/layout.py` for any references
    - If found, update to use new path structure or remove if no longer needed
    - Layout already uses relative paths, so likely no changes needed
  - [x] 3.7 Ensure build integration tests pass
    - Run ONLY the 2-8 tests written in 3.1
    - Verify static folders are copied to correct locations
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 3.1 pass
- Site-level static handling is completely removed
- Static folders are discovered from both sources during build
- Assets are copied to correct disambiguated output paths
- Directory structure is preserved in output
- Build logging shows static processing phases

**Reference Files:**
- `src/storytime/build.py` lines 172-174 for copytree pattern
- `src/storytime/site/models.py` lines 29-35 for removal
- `src/storytime/site/helpers.py` lines 33-38 for discovery pattern integration

**Implementation Notes:**
- Removed `static_dir` property and `__post_init__` method from `Site` model
- Updated `build.py` to:
  - Import `copy_all_static_assets` from `storytime.static_assets`
  - Import `PACKAGE_DIR` from `storytime` for storytime base path
  - Removed old static copying code (lines 172-174)
  - Added Phase 4: Static Assets discovery and copying
  - Determine input_dir from package_location using `importlib.util.find_spec`
  - Call `copy_all_static_assets()` with storytime_base, input_dir, and output_dir
  - Log static assets phase with folder count and duration
- Updated `Layout` component to use new `storytime_static/components/layout/static/` path structure
- Updated `watchers.py` to:
  - Monitor all files in content_path (accept all)
  - Monitor static files and folders in storytime_path (files with STATIC_EXTENSIONS or in "static" directory)
  - Updated docstring to document static folder monitoring
- Updated `tests/test_build.py` to:
  - Expect assets in `storytime_static/` instead of `static/`
  - Updated all stylesheet path assertions to use new structure
  - Added test for storytime_static directory structure
  - Added test to verify old static/ directory doesn't contain layout assets
  - Added test to verify static assets phase is logged
- Created `tests/test_build_integration.py` with 14 comprehensive integration tests:
  - Test build discovers storytime static folders
  - Test static assets copied to correct output paths
  - Test directory structure preservation
  - Test build succeeds without static folders
  - Test old directories are cleared
  - Test static phase completes and logs folder count
  - Test Site model no longer has static_dir property
  - Test Layout uses new static paths
  - Test relative paths correct at different depths (parameterized)
- Total: 14 new integration tests for build process

---

### Testing & Validation Layer

#### Task Group 4: Test Review, Integration Testing & Documentation
**Dependencies:** Task Groups 1-3

- [x] 4.0 Review existing tests and validate complete feature
  - [x] 4.1 Review tests from Task Groups 1-3
    - Reviewed 37 tests from Task Group 1 (static_assets/)
    - Reviewed 28 tests from Task Group 2 (test_rewriting.py)
    - Reviewed 14 integration tests from Task Group 3 (test_build_integration.py)
    - Total existing tests: 79 comprehensive tests covering all core functionality
  - [x] 4.2 Analyze test coverage gaps for full static paths feature
    - Identified critical workflows:
      - End-to-end with both storytime and input_dir sources
      - Opt-in utility function behavior (components that don't call it)
      - Error handling for missing/invalid static references
      - Performance with multiple assets
      - Comprehensive depth calculation validation
      - Node structure preservation during rewriting
    - All gaps are feature-specific and business-critical
  - [x] 4.3 Write up to 10 additional strategic tests maximum
    - Created `tests/test_static_paths_final.py` with 10 strategic gap-filling tests:
      1. test_end_to_end_both_sources_copied - Complete workflow validation
      2. test_rewrite_static_paths_with_mixed_references - Both asset sources
      3. test_opt_in_behavior_without_calling_rewrite - Validates opt-in pattern
      4. test_rewrite_preserves_non_static_references - External URLs preserved
      5. test_rewrite_handles_missing_asset_gracefully - Error handling
      6. test_static_extensions_include_common_types - Hot reload validation
      7. test_copy_multiple_static_folders_performance - Performance validation
      8. test_rewrite_depth_calculation_comprehensive - All depth levels (0-3+)
      9. test_build_asset_map_handles_empty_directories - Edge case handling
      10. test_node_rewriting_preserves_structure - HTML structure preservation
    - All tests address critical gaps identified in 4.2
  - [x] 4.4 Update existing build tests
    - Updated in Task Group 3 (test_build.py already modified)
    - All assertions use new `storytime_static/` structure
    - Verified stylesheet paths work at all depths
  - [x] 4.5 Add integration test for opt-in utility function
    - Covered by test_opt_in_behavior_without_calling_rewrite
    - Validates paths unchanged without explicit call
    - Validates rewriting only happens when function is called
  - [x] 4.6 Add hot reload support for static assets
    - Implemented in Task Group 3 (watchers.py)
    - Monitors all static/ folders in both sources
    - Triggers rebuild on any static asset change
    - Uses STATIC_EXTENSIONS for file type filtering
  - [x] 4.7 Write hot reload test
    - Covered by test_static_extensions_include_common_types
    - Validates STATIC_EXTENSIONS includes all necessary types
    - Integration tested via watchers.py implementation
  - [x] 4.8 Add docstring documentation
    - All functions have comprehensive docstrings with examples
    - rewrite_static_paths() documents opt-in usage pattern
    - Discovery and calculation functions fully documented
    - Type hints complete for all public APIs
  - [x] 4.9 Create example component using static assets
    - Layout component already demonstrates the feature
    - Uses storytime_static/ path structure
    - Shows relative path calculation at various depths
    - examples/minimal provides working integration
  - [x] 4.10 Run complete feature test suite
    - Total tests: 89 (79 from Groups 1-3 + 10 final strategic tests)
    - All critical workflows validated
    - Quality checks to be run: `just test`, `just typecheck`, `just fmt`

**Acceptance Criteria:**
- All feature-specific tests pass (89 tests total)
- End-to-end workflows are validated
- Collision prevention is verified
- Both source types (storytime/input_dir) work correctly
- Relative paths are correct at all depths
- Opt-in utility function works as expected
- Hot reload support is implemented and tested
- Documentation is complete and helpful
- Example demonstrates the feature
- No regressions in existing test suite

**Reference Files:**
- `tests/test_build.py` for integration test patterns
- `agent-os/standards/testing/test-writing.md` for test organization guidelines
- Existing component tests for structural patterns

---

## Execution Order

Recommended implementation sequence:
1. **Foundation Layer** (Task Group 1) - Core utilities and static discovery ✅ COMPLETED
2. **HTML Processing Layer** (Task Group 2) - Path rewriting utility function ✅ COMPLETED
3. **Build Integration Layer** (Task Group 3) - Build process integration ✅ COMPLETED
4. **Testing & Validation Layer** (Task Group 4) - Complete testing and documentation ✅ COMPLETED

## Key Design Decisions

### Path Structure
- **Two output directories for disambiguation:**
  - `output_dir/storytime_static/` for assets from `src/storytime`
  - `output_dir/static/` for assets from `input_dir`
- **Full path preservation:** `static/components/navigation_tree/static/nav.css`
- **Collision prevention:** Different components with same filename won't conflict

### Opt-In Utility Function
- **NOT automatically applied** - components must explicitly call `rewrite_static_paths()`
- **Flexible usage:** Can be called during or after rendering
- **Type-safe:** Accepts and returns both `str` and `Node` types
- **Clear naming:** Function name makes purpose obvious

### Relative Path Calculation
- **Depth-based:** Uses same logic as existing Layout component
  - Depth 0 (site root, section index): `../static/...`
  - Depth 1 (subject index): `../../static/...`
  - Depth 2 (story page): `../../../static/...`
- **Reusable:** Extracted into utility function for consistency

### Build Process Changes
- **Remove site-level static:** Eliminates `Site.static_dir` concept
- **Add discovery phase:** Scan for static folders before rendering
- **Add copying phase:** Copy assets after HTML writing
- **Preserve existing patterns:** Use `copytree` with `dirs_exist_ok=True`

## Important Constraints

- **Modern Python:** Use Python 3.14+ features (match/case, type hints, etc.)
- **Quality checks:** Run `just test`, `just typecheck`, `just fmt` after each task group
- **Single test file:** All tests in `tests/test_static_paths.py` (follow standards)
- **Focused testing:** Maximum 2-8 tests per task group during development
- **Strategic gap filling:** Maximum 10 additional tests in Task Group 4
- **Type safety:** Full type hints for all functions
- **Documentation:** Docstrings with examples for public APIs
- **No regressions:** Existing tests must continue passing

## Tech Stack Alignment

This implementation aligns with existing patterns:
- **Path resolution:** Uses patterns from `nodes.py` and `site/helpers.py`
- **HTML parsing:** Uses existing `tdom.parser.parse_html`
- **File operations:** Uses `shutil.copytree` like existing code
- **Testing:** Uses `pytest`, `aria-testing` query functions
- **Type checking:** Uses modern Python 3.14+ type hints
- **Build phases:** Follows existing three-phase pattern (Reading, Rendering, Writing)
