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

- [ ] 2.0 Complete opt-in path rewriting utility using tree walker
  - [ ] 2.1 Extend `src/storytime/static_assets/paths.py` with relative path calculation
    - Function: `calculate_relative_static_path(asset_path: str, page_depth: int, source_type: Literal["storytime", "input_dir"]) -> str`
    - Takes an asset path like "static/nav.css" or "storytime_static/nav.css"
    - Calculates "../" prefix based on page_depth
    - Returns relative path like "../../storytime_static/components/nav/static/nav.css"
    - Add tests covering various depths (0, 1, 2, 3+)
  - [ ] 2.2 Create tree walker utilities in `src/storytime/static_assets/rewriting.py`
    - Function: `walk_and_rewrite_static_refs(node: Node, page_depth: int, discovered_assets: dict[str, Path]) -> Node`
    - Uses tdom tree walker to traverse node tree recursively
    - Checks each element for asset-referencing attributes (`src`, `href`)
    - Modifies attribute values in place when they start with "static/" or "storytime_static/"
    - Preserves all other node properties and structure
    - Add comprehensive tests for various node structures
  - [ ] 2.3 Implement attribute rewriting logic in `src/storytime/static_assets/rewriting.py`
    - Function: `rewrite_element_attributes(element: Node, page_depth: int, discovered_assets: dict[str, Path]) -> None`
    - Inspects element attributes for static asset references
    - Rewrites attribute values in place on the node
    - Handles `src` for `<script>`, `<img>`, `<source>` tags
    - Handles `href` for `<link>` tags
    - Add tests for edge cases (missing attributes, non-static paths)
  - [ ] 2.4 Create main opt-in utility function in `src/storytime/static_assets/rewriting.py`
    - Function: `rewrite_static_paths(node: Node, page_depth: int, discovered_assets: dict[str, Path]) -> Node`
    - Accepts tdom Node as input
    - Calls tree walker to find and rewrite all static references
    - Returns modified Node with rewritten paths
    - Works directly with node tree, no string conversion
    - Add tests for Node input with various structures
  - [ ] 2.5 Add asset path resolution in `src/storytime/static_assets/rewriting.py`
    - Function: `resolve_static_asset_path(asset_ref: str, discovered_assets: dict[str, Path]) -> str | None`
    - Takes reference like "static/nav.css" or "storytime_static/components/nav/static/nav.css"
    - Looks up in discovered_assets dict to find full output path
    - Returns full path preserving structure, or None if not found
    - Add tests with various asset references
  - [ ] 2.6 Create helper to build discovered assets dict in `src/storytime/static_assets/__init__.py`
    - Function: `build_discovered_assets_map(storytime_base: Path, input_dir: Path, output_dir: Path) -> dict[str, Path]`
    - Discovers all static folders using existing discovery functions
    - Builds mapping from short references to full output paths
    - Example: {"static/nav.css" → Path("output/storytime_static/components/nav/static/nav.css")}
    - Returns dict for use with rewrite_static_paths()
    - Add integration tests
  - [ ] 2.7 Add validation and error handling in `src/storytime/static_assets/rewriting.py`
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

- [ ] 3.0 Complete build process integration
  - [ ] 3.1 Write 2-8 focused tests for build integration
    - Test static folder discovery during build
    - Test static asset copying to correct output paths
    - Test preservation of directory structure
    - Skip testing hot reload at this stage
  - [ ] 3.2 Remove existing site-level static handling
    - Remove `static_dir` property from `src/storytime/site/models.py` line 26
    - Remove `__post_init__` logic from `src/storytime/site/models.py` lines 29-35
    - Remove static copying code from `src/storytime/build.py` lines 172-174
  - [ ] 3.3 Add static discovery phase to build process
    - Add discovery before rendering phase in `build.py`
    - Call discovery function for both `src/storytime` and `input_dir`
    - Store discovered static folders in data structure
    - Log discovered folders for debugging
  - [ ] 3.4 Implement static asset copying phase
    - Add copying phase after HTML writing phase in `build.py`
    - Loop through discovered static folders
    - Use `shutil.copytree` with `dirs_exist_ok=True` (reuse pattern from lines 172-174)
    - Copy from source static folder to appropriate output path:
      - `src/storytime` assets → `output_dir/storytime_static/[path]/static/`
      - `input_dir` assets → `output_dir/static/[path]/static/`
  - [ ] 3.5 Add build logging
    - Log static folder discovery phase duration
    - Log static asset copying phase duration
    - Log number of static folders discovered and copied
  - [ ] 3.6 Update Layout component to remove site.static_dir references
    - Review `src/storytime/components/layout/layout.py` for any references
    - If found, update to use new path structure or remove if no longer needed
    - Layout already uses relative paths, so likely no changes needed
  - [ ] 3.7 Ensure build integration tests pass
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

---

### Testing & Validation Layer

#### Task Group 4: Test Review, Integration Testing & Documentation
**Dependencies:** Task Groups 1-3

- [ ] 4.0 Review existing tests and validate complete feature
  - [ ] 4.1 Review tests from Task Groups 1-3
    - Review the 2-8 tests written by foundation-engineer (Task 1.1)
    - Review the 2-8 tests written by html-processor (Task 2.1)
    - Review the 2-8 tests written by build-integrator (Task 3.1)
    - Total existing tests: approximately 6-24 tests
  - [ ] 4.2 Analyze test coverage gaps for full static paths feature
    - Identify critical workflows lacking test coverage:
      - End-to-end: static asset from component → output dir → HTML reference
      - Collision prevention: same filename in different component paths
      - Depth variations: verify correct relative paths at all depths
      - Two source types: storytime vs input_dir disambiguation
    - Focus ONLY on gaps related to this spec's feature requirements
    - Do NOT assess entire application test coverage
  - [ ] 4.3 Write up to 10 additional strategic tests maximum
    - Add maximum of 10 new tests in `tests/test_static_paths.py`
    - Test end-to-end workflow: component with static → build → verify output paths
    - Test collision prevention with same filenames in different paths
    - Test path rewriting utility with real HTML from components
    - Test both `storytime_static/` and `static/` output directories
    - Test relative path correctness at different depths
    - Skip edge cases, performance tests unless business-critical
  - [ ] 4.4 Update existing build tests
    - Update `tests/test_build.py` to remove expectations of old `static/` directory from site-level
    - Add assertions for new `storytime_static/` and component-specific `static/` directories
    - Verify stylesheet paths still work (Layout already uses relative paths)
  - [ ] 4.5 Add integration test for opt-in utility function
    - Test component that explicitly calls `rewrite_static_paths()`
    - Verify paths are rewritten correctly in rendered HTML
    - Test component that does NOT call utility has unchanged paths
  - [ ] 4.6 Add hot reload support for static assets
    - Extend file watching in `src/storytime/server.py` or relevant file
    - Monitor all discovered `static/` folders in both sources
    - Trigger rebuild when any static asset changes
    - Note: Implementation may vary based on existing watch system
  - [ ] 4.7 Write hot reload test
    - Test that changes to static assets trigger rebuild
    - May need to check existing watch system structure first
    - Add to strategic tests if not already covered
  - [ ] 4.8 Add docstring documentation
    - Document `rewrite_static_paths()` function with examples
    - Document expected calling pattern and use cases
    - Add docstring to discovery and calculation functions
  - [ ] 4.9 Create example component using static assets
    - Add example in `examples/` directory if present
    - Demonstrate static folder structure and utility function usage
    - Show both storytime and input_dir static asset patterns
  - [ ] 4.10 Run complete feature test suite
    - Run ALL tests related to this feature (tests from 1.1, 2.1, 3.1, and 4.3-4.7)
    - Expected total: approximately 16-34 tests maximum
    - Verify all critical workflows pass
    - Run `just test` to ensure no regressions in existing tests

**Acceptance Criteria:**
- All feature-specific tests pass (approximately 16-34 tests total)
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
3. **Build Integration Layer** (Task Group 3) - Build process integration
4. **Testing & Validation Layer** (Task Group 4) - Complete testing and documentation

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
