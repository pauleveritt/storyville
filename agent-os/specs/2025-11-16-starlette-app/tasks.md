# Task Breakdown: Starlette App for Static Site Serving

## Overview
Total Tasks: 3 task groups with focused implementation

## Task List

### Application Layer

#### Task Group 1: Clean and Implement Application Factory
**Dependencies:** None

- [x] 1.0 Complete application factory implementation
  - [x] 1.1 Write 2-5 focused tests for create_app functionality
    - Test that create_app accepts Path parameter
    - Test that create_app returns Starlette instance
    - Test that app has debug=True
    - Test that app serves from provided path
    - Skip exhaustive testing of StaticFiles behavior (handled by Starlette)
  - [x] 1.2 Clean up existing app.py implementation
    - Remove RebuildServer class (lines 28-90)
    - Remove watchfiles imports (line 11)
    - Remove WebSocketRoute import (line 14)
    - Remove WebSocket import (line 16)
    - Remove Site import (line 18)
    - Remove TYPE_CHECKING and type imports (lines 20-21)
    - Remove asyncio and concurrent.futures imports (lines 4-5)
    - Remove asynccontextmanager import (line 7)
    - Remove process_changes function (lines 24-25)
    - Remove render_node endpoint function (lines 92-94)
  - [x] 1.3 Implement create_app(path: Path) -> Starlette
    - Accept path: Path parameter (built site root directory)
    - Use modern Python 3.14+ type hints
    - Create single StaticFiles mount: `Mount("/", app=StaticFiles(directory=path, html=True), name="site")`
    - Return Starlette instance with debug=True
    - No lifespan parameter
    - No WebSocket routes
    - Function should be synchronous (no async def)
    - Follow pattern: `Starlette(debug=True, routes=[Mount(...)])`
  - [x] 1.4 Update imports in app.py
    - Keep: `from pathlib import Path`
    - Keep: `from starlette.applications import Starlette`
    - Keep: `from starlette.routing import Mount`
    - Keep: `from starlette.staticfiles import StaticFiles`
    - Remove all other imports
  - [x] 1.5 Ensure application layer tests pass
    - Run ONLY the 2-5 tests written in 1.1
    - Verify create_app returns proper Starlette instance
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-5 tests written in 1.1 pass
- create_app has correct signature: `create_app(path: Path) -> Starlette`
- All reload/watching infrastructure removed from app.py
- Single StaticFiles mount at root with html=True
- Application sets debug=True

### Testing Layer

#### Task Group 2: Implement Test Infrastructure
**Dependencies:** Task Group 1

- [x] 2.0 Complete test infrastructure
  - [x] 2.1 Write 3-6 focused tests for static file serving
    - Test serving index.html at root path `/`
    - Test serving section index at `/section/components/`
    - Test serving static asset at `/static/bulma.css`
    - Test 404 for non-existent path
    - Limit to critical serving behaviors only
    - Skip edge cases like permission errors or malformed paths
  - [x] 2.2 Update test_app.py to use tmp_path fixture
    - Remove current test_application function (lines 7-13)
    - Replace site = make_site() pattern with build_site() pattern
    - Each test should call: `build_site(package_location="storyville", output_dir=tmp_path)`
    - Then create app: `app = create_app(tmp_path)`
    - Use TestClient for synchronous HTTP testing
    - Follow pattern from test_build.py fixture usage
  - [x] 2.3 Add import for build_site
    - Add: `from storyville.build import build_site`
    - Remove: `from storyville import make_site`
    - Keep: `from starlette.testclient import TestClient`
    - Keep: `from storyville.app import create_app`
  - [x] 2.4 Implement test for root index serving
    - Build site to tmp_path
    - Create app with tmp_path
    - Request: `client.get("/")`
    - Assert: status_code == 200
    - Assert: response content contains expected HTML
    - Verify index.html is served
  - [x] 2.5 Implement test for section page serving
    - Build site to tmp_path
    - Create app with tmp_path
    - Request: `client.get("/section/components/")`
    - Assert: status_code == 200
    - Assert: response content contains section content
    - Verify directory request resolves to index.html
  - [x] 2.6 Implement test for static asset serving
    - Build site to tmp_path
    - Create app with tmp_path
    - Request: `client.get("/static/bulma.css")`
    - Assert: status_code == 200
    - Assert: response content contains CSS content
    - Verify static files are accessible
  - [x] 2.7 Ensure test layer tests pass
    - Run ONLY the 3-6 tests written in 2.1
    - Verify all serving behaviors work correctly
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 3-6 tests written in 2.1 pass
- Tests use tmp_path fixture for isolation
- Tests verify index.html serving at root
- Tests verify section page serving with directory paths
- Tests verify static asset serving
- All tests use build_site() before create_app()

### Quality Assurance

#### Task Group 3: Quality Checks and Cleanup
**Dependencies:** Task Groups 1-2

- [x] 3.0 Complete quality assurance
  - [x] 3.1 Review all tests from Task Groups 1-2
    - Review the 2-5 tests from Task 1.1 (application factory)
    - Review the 3-6 tests from Task 2.1 (static serving)
    - Total existing tests: approximately 5-11 tests
    - Identify any critical gaps in serving behavior
  - [x] 3.2 Add up to 3 additional tests if critical gaps exist
    - Only add tests for business-critical missing scenarios
    - Focus on end-to-end serving workflows
    - Do NOT add exhaustive edge case coverage
    - Examples: subject page serving, 404 handling, trailing slash behavior
  - [x] 3.3 Run project quality checks
    - Execute: `just test` (run all feature tests)
    - Execute: `just typecheck` (verify type hints)
    - Execute: `just fmt` (format code)
    - All checks must pass
  - [x] 3.4 Verify integration with build_site
    - Confirm built site structure is preserved
    - Verify StaticFiles serves all built content correctly
    - Check that html=True parameter enables index.html resolution
    - Test that relative paths in HTML work correctly

**Acceptance Criteria:**
- All tests pass (approximately 8-14 tests total)
- Type checking passes with no errors
- Code is properly formatted
- No more than 3 additional tests added in gap analysis
- Integration with build_site verified
- All project quality checks pass (just test, just typecheck, just fmt)

## Execution Order

Recommended implementation sequence:
1. Application Layer (Task Group 1) - Clean up and implement factory
2. Testing Layer (Task Group 2) - Build comprehensive test coverage
3. Quality Assurance (Task Group 3) - Verify and polish

## Key Implementation Notes

**Path Parameter Usage:**
- The `path` parameter points to the built site root (e.g., `var/` directory)
- This directory contains: `index.html`, `section/*/index.html`, `static/*`
- Do NOT accept Site model object - this is post-build serving only

**StaticFiles Mount Configuration:**
- Single mount at root: `Mount("/", app=StaticFiles(directory=path, html=True), name="site")`
- The `html=True` parameter is critical for automatic index.html resolution
- No separate routes needed for static assets or dynamic content

**Test Isolation Strategy:**
- Every test should use pytest's `tmp_path` fixture
- Build site fresh in each test: `build_site(package_location="storyville", output_dir=tmp_path)`
- Then create app: `app = create_app(tmp_path)`
- This ensures no pollution between tests or to project workspace

**Cleanup Requirements:**
- Remove entire RebuildServer class and all related infrastructure
- Remove all async/await code related to file watching
- Remove WebSocket route and reload functionality
- Keep implementation minimal and focused on static serving only

**Modern Python Standards:**
- Use `Path` from pathlib (not string paths)
- Use modern type hints: `path: Path`, return type `-> Starlette`
- No type aliases needed for this simple feature
- Function is synchronous (no async)

**Files Modified:**
- `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/app.py`
- `/Users/pauleveritt/projects/t-strings/storyville/tests/test_app.py`
- `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/__main__.py` (bonus: updated to work with new signature)
