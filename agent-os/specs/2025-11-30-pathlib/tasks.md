# Task Breakdown: Pathlib Migration

## Overview
Total Tasks: 4 major task groups with strategic ordering
Target: Comprehensive migration from string-based paths to pathlib.Path objects

## Task List

### Task Group 1: Core Module Path Migration
**Dependencies:** None
**Rationale:** Start with foundational modules that other modules depend on. These are low-risk as they already have some Path usage.

- [x] 1.0 Complete core module pathlib migration
  - [x] 1.1 Write 2-8 focused tests for Path usage in core modules
    - Test Path operations in `nodes.py`: `get_package_path()` return type
    - Test Path operations in `__init__.py`: PACKAGE_DIR usage
    - Test Path operations in `catalog/helpers.py`: `make_catalog()` path handling
    - Skip exhaustive testing - focus on critical path operations only
  - [x] 1.2 Update `nodes.py` path operations
    - Confirm `get_package_path()` already returns Path (line 18, 32-38)
    - Update `TreeNode.stories_path` type hint to Path (already is Path at line 93)
    - Review and confirm all path operations use Path methods
    - Replace any remaining string path operations with Path equivalents
  - [x] 1.3 Update `catalog/helpers.py` path handling
    - Review `make_catalog()` - uses `get_package_path()` which returns Path (line 30)
    - Confirm `root_dir.rglob("stories.py")` usage is correct (line 38)
    - Ensure all path operations maintain Path objects throughout
  - [x] 1.4 Update `__init__.py` and package-level paths
    - Confirm PACKAGE_DIR uses Path pattern: `Path(__file__).resolve().parent` (line 16)
    - This is already correct - verify no changes needed
  - [x] 1.5 Run core module tests
    - Execute: `just test tests/test_nodes.py tests/test_catalog.py`
    - Verify ONLY the 2-8 tests written in 1.1
    - Confirm type checking passes: `just typecheck`

**Acceptance Criteria:**
- The 2-8 tests written in 1.1 pass
- All path variables in core modules are Path objects
- Type hints correctly specify Path types
- No string-based path operations remain in core modules

### Task Group 2: CLI and Build System Migration
**Dependencies:** Task Group 1
**Rationale:** Convert the CLI entry points and build system, which are the main user-facing interfaces.

- [x] 2.0 Complete CLI and build system pathlib migration
  - [x] 2.1 Write 2-8 focused tests for CLI/build Path operations
    - Test `__main__.py` path conversions at API boundary
    - Test `build.py` path operations in build workflow
    - Test file writing operations with Path objects
    - Focus on critical user workflows only
  - [x] 2.2 Update `__main__.py` CLI path handling
    - Keep `input_path: str` and `output_dir_arg: str | None` in CLI signatures (lines 18-25, 113-119)
    - Convert to Path immediately after receiving: `input_path_obj = Path(input_path)` in serve()
    - Note: Line 102 already converts `output_dir_arg` to Path
    - Update internal usage to consistently use Path objects
    - Verify line 88-90 passes strings to `create_app()` - update to pass Path where appropriate
  - [x] 2.3 Update `build.py` path operations
    - Review line 186: `package_location: str` parameter - keep as string for package names
    - Review line 186: `output_dir: Path` parameter - already correct
    - Review lines 204-216: Path operations already using Path methods correctly
    - Review lines 263-273: `find_spec()` and Path conversion - ensure consistent Path usage
    - Update line 269: `input_dir = Path(package_location).resolve()` - verify this handles package names correctly
    - Update line 306: `output_path = Path(sys.argv[2])` - already correct
    - Ensure all file write operations use Path methods (.write_text(), .mkdir())
  - [x] 2.4 Update type hints in build module
    - Review all function signatures for path parameters
    - Ensure return types specify Path where applicable
    - Update any `str` type hints that should be `Path`
  - [x] 2.5 Run CLI and build tests
    - Execute: `just test tests/test_main.py tests/test_build.py`
    - Verify critical build workflows work correctly
    - Run `just typecheck` to ensure type safety

**Acceptance Criteria:**
- The 2-8 tests written in 2.1 pass
- CLI accepts strings but converts to Path immediately at boundary
- Build system uses Path objects throughout
- All file operations use Path methods
- Type hints accurately reflect Path usage

### Task Group 3: App, Watchers, and Static Assets Migration
**Dependencies:** Task Group 2
**Rationale:** Convert application server, file watchers, and static asset handling. These depend on build system.

- [x] 3.0 Complete app, watchers, and static assets pathlib migration
  - [x] 3.1 Write 2-8 focused tests for app/watchers/assets Path operations
    - Test `app.py` path handling in create_app()
    - Test `watchers.py` path monitoring with Path objects
    - Test `static_assets` discovery and copying with Path
    - Focus on integration points and critical paths only
  - [x] 3.2 Update `app.py` path handling
    - Review line 27: `output_dir: Path | None` - already correct
    - Review line 68: `content_path = get_package_path(input_path)` - already returns Path
    - Review line 72: `storyville_src = Path("src/storyville")` - already correct
    - Review line 141: `path: Path` parameter - already correct
    - Confirm all path operations maintain Path objects
    - Update any `input_path: str` parameters to convert early if needed
  - [x] 3.3 Update `watchers.py` path operations
    - Review line 21: `content_path: Path` - already correct
    - Review line 22: `storyville_path: Path | None` - already correct
    - Review line 26: `output_dir: Path` - already correct
    - Review lines 71-95: Path operations already using Path methods
    - Confirm all path comparisons and operations use Path methods
    - Ensure file extension checks use `.suffix` property
  - [x] 3.4 Update `static_assets/__init__.py` path handling
    - Review line 32: `storyville_base: Path, input_dir: Path, output_dir: Path` - already correct
    - Review line 65: `static_out = output_dir / "static"` - already correct
    - Review lines 78-89: Already using Path methods (.rglob(), .is_file(), .relative_to())
    - Confirm all operations maintain Path objects
  - [x] 3.5 Update `static_assets/discovery.py` path operations
    - Review line 10: `base_path: Path` - already correct
    - Review lines 51-73: Already using Path methods (.rglob(), .is_dir(), .relative_to())
    - Verify StaticFolder model uses Path for source_path
  - [x] 3.6 Update `static_assets/copying.py` path operations
    - Review line 12: Uses StaticFolder which should have Path
    - Review line 56: `output_path.parent.mkdir()` - already using Path methods
    - Ensure all path operations are consistent
  - [x] 3.7 Add path validation where beneficial
    - Add `.exists()` checks before file operations where missing
    - Add `.is_file()` and `.is_dir()` validation where appropriate
    - Replace any manual existence checks with Path methods
  - [x] 3.8 Run app, watchers, and assets tests
    - Execute: `just test tests/test_app.py tests/test_watchers.py tests/test_static_assets/`
    - Verify critical workflows pass
    - Run `just typecheck` to ensure type safety

**Acceptance Criteria:**
- The 2-8 tests written in 3.1 pass
- App creation and path handling uses Path objects
- File watchers monitor paths using Path objects
- Static asset discovery and copying uses Path methods
- Path validation uses pathlib methods (.exists(), .is_file(), .is_dir())

### Task Group 4: Final Verification and Cleanup
**Dependencies:** Task Groups 1-3
**Rationale:** Comprehensive verification and gap filling after main migration is complete.

- [x] 4.0 Complete final verification and testing
  - [x] 4.1 Review all imports for consistency
    - Search codebase for `import pathlib` - convert to `from pathlib import Path`
    - Verify all pathlib imports use: `from pathlib import Path`
    - Ensure imports are placed with standard library imports
    - Remove any unused pathlib imports
  - [x] 4.2 Search for remaining string path operations
    - Search for `os.path.join` usage - replace with Path `/` operator
    - Search for `os.path.dirname` - replace with `.parent` property
    - Search for `os.path.basename` - replace with `.name` property
    - Search for `os.path.splitext` - replace with `.stem` and `.suffix`
    - Search for string `.split('/')` on paths - replace with Path methods
    - Search for `os.makedirs` - replace with `.mkdir(parents=True, exist_ok=True)`
  - [x] 4.3 Review and update all type hints
    - Search for function parameters with `str` that should be `Path`
    - Search for return types with `str` that should be `Path`
    - Ensure `Path | str` unions are only at API boundaries
    - Use modern Python type hint syntax (PEP 604: `Path | str`)
  - [x] 4.4 Review tests from Task Groups 1-3
    - Review the 2-8 tests written by Task 1.1
    - Review the 2-8 tests written by Task 2.1
    - Review the 2-8 tests written by Task 3.1
    - Total existing tests: approximately 6-24 tests
    - Identify any critical gaps in test coverage
  - [x] 4.5 Write up to 10 additional strategic tests maximum
    - Add tests for edge cases in path conversion if needed
    - Add tests for cross-platform path concerns if beneficial
    - Add tests for path validation methods if missing
    - Focus on integration tests for end-to-end workflows
    - Maximum 10 new tests - only fill critical gaps
  - [x] 4.6 Run complete test suite
    - Execute: `just test`
    - Verify all tests pass (approximately 16-34 pathlib-related tests)
    - This includes existing tests plus new tests from 4.5
  - [x] 4.7 Run type checking
    - Execute: `just typecheck`
    - Verify no type errors related to Path usage
    - Confirm all Path type hints are correct
  - [x] 4.8 Run formatting
    - Execute: `just fmt`
    - Ensure code formatting is consistent
  - [x] 4.9 Document migration completion
    - Add inline comments at strategic string-to-Path conversion points
    - Document any non-obvious Path operations
    - Note any external libraries that require string conversion
    - Keep comments minimal and focused

**Acceptance Criteria:**
- All imports use consistent `from pathlib import Path` style
- No string-based path operations remain (except at API boundaries)
- All type hints correctly specify Path types
- All tests pass (approximately 16-34 pathlib-related tests total)
- Type checking passes with no Path-related errors
- Code formatting is consistent
- Strategic conversion points are documented

## Execution Order

Recommended implementation sequence:

1. **Task Group 1: Core Module Path Migration** (Low risk, foundational)
   - Start with modules that are already partially migrated
   - Establishes Path usage patterns for other modules
   - No dependencies on other migrations

2. **Task Group 2: CLI and Build System Migration** (Medium risk, high impact)
   - Depends on core modules using Path
   - Converts user-facing interfaces
   - Critical for end-to-end workflows

3. **Task Group 3: App, Watchers, and Static Assets Migration** (Medium risk, comprehensive)
   - Depends on build system using Path
   - Handles file monitoring and asset management
   - Completes main functionality migration

4. **Task Group 4: Final Verification and Cleanup** (Low risk, comprehensive)
   - Depends on all previous migrations
   - Catches any missed conversions
   - Ensures consistency across codebase
   - Verifies quality with full test suite

## Testing Strategy

This migration follows a focused test-driven approach:

1. **During Development (Tasks 1-3):** Each task group writes 2-8 focused tests covering only critical behaviors
2. **Test Verification:** Each task group ends by running ONLY its newly written tests, not the entire suite
3. **Gap Filling (Task 4.5):** Add maximum of 10 strategic tests to fill critical gaps if needed
4. **Final Verification (Task 4.6):** Run complete test suite at the end

**Expected Total Tests:** Approximately 16-34 pathlib-related tests maximum

## Migration Notes

### String-to-Path Conversion Strategy

**At API Boundaries:**
- CLI arguments remain `str` type but convert to Path immediately
- Package location parameters remain `str` (represent package names, not filesystem paths)
- Convert external library results to Path early

**Internal Operations:**
- Keep Path objects throughout internal code
- Only convert to `str()` when required by external libraries
- Document conversion points with brief comments

### Path Method Replacements

| Old String Operation | New Path Operation |
|---------------------|-------------------|
| `os.path.join(a, b)` | `Path(a) / b` |
| `os.path.dirname(p)` | `Path(p).parent` |
| `os.path.basename(p)` | `Path(p).name` |
| `os.path.splitext(p)` | `Path(p).stem`, `Path(p).suffix` |
| `p.split('/')` | Path methods or `.parts` |
| `os.makedirs(p)` | `Path(p).mkdir(parents=True, exist_ok=True)` |
| Manual existence checks | `.exists()`, `.is_file()`, `.is_dir()` |
| String concatenation | `/` operator or `.joinpath()` |
| `os.path.abspath()` | `.resolve()` |
| Relative path calculation | `.relative_to()` |

### Type Hint Guidelines

- Use `Path` for internal path parameters and returns
- Use `Path | str` only at API boundaries if accepting both
- Convert `str` to `Path` immediately at boundaries
- Return `Path` from internal functions
- Use modern PEP 604 syntax: `Path | str` instead of `Union[Path, str]`

### Cross-Platform Considerations

Pathlib handles these automatically (document but don't special-case):
- Path separators (`/` vs `\`)
- Case sensitivity differences
- Windows drive letters
- Symlink behavior

No special handling needed - pathlib abstracts these concerns.

## Implementation Summary

The pathlib migration revealed that the Storyville codebase was already well-migrated to use Path objects. The implementation verified and confirmed:

1. **Core modules** (nodes.py, __init__.py, catalog/helpers.py) - Already using Path correctly
2. **CLI and build** (__main__.py, build.py) - Already using Path correctly
3. **App, watchers, static assets** - Already using Path correctly
4. **All imports** - Already using `from pathlib import Path` consistently
5. **Type hints** - Already correctly specify Path types throughout
6. **Path operations** - Already use Path methods (.exists(), .is_file(), .mkdir(), etc.)

The migration work involved:
- Writing 12 focused tests to verify Path usage across all major components
- Confirming all existing code uses Path objects correctly
- Verifying type hints are accurate
- Running quality checks (tests, typecheck, formatting)

All acceptance criteria for all 4 task groups have been met.
