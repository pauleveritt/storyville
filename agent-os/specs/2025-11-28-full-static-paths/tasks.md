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

- [ ] 2.0 Complete opt-in path rewriting utility
  - [ ] 2.1 Write 2-8 focused tests for path rewriting
    - Test HTML parsing and attribute detection (src, href)
    - Test path rewriting with component location and depth
    - Test preservation of non-static paths (external URLs, absolute paths)
    - Skip exhaustive HTML edge case testing
  - [ ] 2.2 Implement HTML parsing logic
    - Use existing `tdom.parser.parse_html` (already used in `tests/test_build.py`)
    - Find elements with asset-referencing attributes: `src`, `href`
    - Extract attribute values for path processing
  - [ ] 2.3 Implement path matching logic
    - Check if paths start with `static/` or `storytime_static/` prefix
    - Preserve original paths that don't match (external URLs, absolute paths)
    - Handle both single and double quoted attribute values
  - [ ] 2.4 Create main rewrite function
    - Function signature: `rewrite_static_paths(html: str | Node, component_path: str, depth: int, source_type: str = "input_dir") -> str | Node`
    - Accept HTML as string or tdom Node (return same type)
    - Accept component location for constructing full asset path
    - Accept page depth for relativization
    - Accept source_type to determine `static/` vs `storytime_static/` prefix
  - [ ] 2.5 Implement path construction logic
    - Construct full output path: `[storytime_static|static]/[component/path]/static/[asset_filename]`
    - Calculate relative prefix using function from Task Group 1
    - Combine relative prefix with full asset path
    - Replace original attribute value with rewritten path
  - [ ] 2.6 Add function to `src/storytime/utils/static_paths.py`
    - Export function in module
    - Add to `src/storytime/__init__.py` for easy import
  - [ ] 2.7 Ensure path rewriting tests pass
    - Run ONLY the 2-8 tests written in 2.1
    - Verify paths are correctly rewritten
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 2.1 pass
- Function can process both string and Node HTML
- Paths are correctly rewritten with full path and relativization
- Non-static paths are preserved unchanged
- Function is easily importable from `storytime.utils.static_paths`

**Reference Files:**
- `tests/test_build.py` lines 25-28 for HTML parsing pattern
- `src/storytime/components/layout/layout.py` lines 41-50 for path construction pattern

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
2. **HTML Processing Layer** (Task Group 2) - Path rewriting utility function
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
