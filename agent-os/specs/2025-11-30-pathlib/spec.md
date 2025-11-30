# Specification: Pathlib Migration

## Goal
Comprehensively migrate all string-based path handling to use Python's `pathlib.Path` objects throughout the Storytime codebase, improving type safety, code clarity, and leveraging modern Python path handling capabilities.

## User Stories
- As a developer, I want path operations to use type-safe Path objects so that I can catch path-related errors at type-check time rather than runtime
- As a maintainer, I want consistent path handling across the codebase so that path operations are predictable and easier to reason about

## Specific Requirements

**Convert all string-based paths to Path objects**
- Replace all string path variables with `Path` objects in all modules
- Convert `__main__.py` input_path and output_dir_arg parameters to use Path internally immediately after receiving string inputs
- Convert `build.py` package_location handling to use Path where filesystem operations occur
- Convert `nodes.py` path string manipulations to use Path methods
- Update `static_assets/__init__.py` and submodules to ensure all path parameters and return values use Path
- Update `watchers.py` to use Path objects consistently

**Update function signatures with Path type hints**
- Change function parameters from `str` to `Path` where paths are expected
- For user-facing CLI arguments that must accept strings, convert to Path immediately at API boundary
- Return `Path` objects from functions that currently return string paths
- Use `Path` type hints consistently throughout: `def function(path: Path) -> Path:`
- Apply modern Python type hints using PEP 604 union syntax if fallback needed: `Path | str`

**Leverage pathlib validation methods extensively**
- Replace manual string-based existence checks with `.exists()` method
- Replace manual directory checks with `.is_dir()` method
- Replace manual file checks with `.is_file()` method
- Use `.resolve()` to get absolute paths instead of manual string manipulation
- Use `.relative_to()` for calculating relative paths instead of string operations
- Replace string path joining with `/` operator: `base_path / "subdir" / "file.txt"`

**Consolidate import statements**
- Standardize all pathlib imports to: `from pathlib import Path`
- Remove any `import pathlib` style imports
- Place import at top of file with other standard library imports
- Apply consistently across all modules

**Handle string conversion strategically**
- Convert Path to string using `str()` only when necessary for external libraries
- Convert Path to string for template rendering or JSON serialization where required
- Keep Path objects as long as possible in internal operations
- Document conversion points with brief inline comments where non-obvious

**Update path operations to use Path methods**
- Replace `os.path.join()` with Path `/` operator
- Replace `os.path.dirname()` with `.parent` property
- Replace `os.path.basename()` with `.name` property
- Replace `os.path.splitext()` with `.stem` and `.suffix` properties
- Replace string `.split('/')` operations with Path traversal methods
- Use `.mkdir(parents=True, exist_ok=True)` instead of os.makedirs

**Maintain existing error handling patterns**
- Keep current error handling approaches in each module
- Do not introduce new error handling strategies
- Ensure pathlib exceptions (like `ValueError` from `.relative_to()`) are handled where currently appropriate
- Preserve existing try/except blocks and error messages

**Document cross-platform considerations**
- Pathlib automatically handles path separators across Windows/Unix
- Path operations are case-sensitive on Unix, case-insensitive on Windows
- Windows drive letters are handled automatically by pathlib
- Symlink behavior differs between platforms but pathlib abstracts this
- No special handling needed - pathlib manages cross-platform concerns

## Visual Design
No visual assets provided (not applicable for this refactoring task).

## Existing Code to Leverage

**`__init__.py` PACKAGE_DIR pattern**
- Already uses `Path(__file__).resolve().parent` to get package directory
- This pattern should be replicated wherever package/module directories are resolved
- Demonstrates correct usage of Path for module-relative path resolution

**`build.py` Path usage in writing operations**
- Already uses Path objects for `output_dir` parameter and file operations
- Uses `.mkdir(parents=True, exist_ok=True)` for directory creation
- Uses `.write_text()` for writing HTML files
- Pattern: `(output_dir / "index.html").write_text(content)`
- This demonstrates correct Path usage for file I/O operations

**`app.py` Path type hints and operations**
- Function signatures use `Path` type for path parameters: `path: Path`, `output_dir: Path | None`
- Uses `Path("src/storytime")` for constructing paths
- Uses `.exists()` for path validation
- This demonstrates proper type hints and validation patterns to replicate

**`nodes.py` get_package_path() function**
- Converts package names to filesystem paths using `Path(package.__file__).parent`
- Handles namespace packages with `Path(package.__path__[0])`
- This is the authoritative pattern for package-to-path conversion

**`static_assets` modules Path consistency**
- `discovery.py` uses `.rglob("static")` for recursive directory finding
- `__init__.py` uses `.relative_to()` for calculating relative paths
- Uses `.rglob("*")` and `.is_file()` for traversing file trees
- These patterns demonstrate proper pathlib idioms for file discovery and traversal

## Out of Scope
- Adding new pathlib-based features beyond migration
- Testing pathlib's own functionality (only test our usage)
- Changing behavior of existing functionality
- Modifying external library interfaces that require strings
- Adding backwards compatibility for string-based paths in public APIs
- Introducing new validation or error handling strategies
- Performance optimization of path operations
- Adding path-specific test cases unless behavior changes
- Modifying pytest fixtures or test infrastructure beyond path type changes
- Changing logging or debug output formats
