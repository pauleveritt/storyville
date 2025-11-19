# Task Breakdown: pytest Plugin for Story Assertions

## Overview

Total Task Groups: 7
Implementation approach: Bottom-up foundation (config, plugin hooks) → core functionality (discovery, collection) →
rendering and reporting → fixtures and examples → testing and quality checks

## Task List

### Foundation Layer

#### Task Group 1: Configuration Schema and Plugin Registration

**Dependencies:** None

- [x] 1.0 Complete configuration foundation
    - [x] 1.1 Write 2-8 focused tests for configuration handling
        - Test reading `[tool.storytime.pytest]` section from pyproject.toml
        - Test `story_paths` setting with custom paths
        - Test `enabled` setting (true/false)
        - Test default values: `story_paths = ["examples/"]`, `enabled = true`
        - Test path validation (paths exist and readable)
        - Limit to 2-8 highly focused tests maximum
    - [x] 1.2 Add `[project.entry-points.pytest11]` to pyproject.toml
        - Register plugin entry point: `storytime = "storytime.pytest_plugin"`
        - Ensure plugin activates automatically when storytime is installed
    - [x] 1.3 Create `/src/storytime/pytest_plugin.py` module
        - Implement config reading using pytest.Config.getini() API
        - Define config schema for `[tool.storytime.pytest]` section
        - Implement path validation during plugin initialization
        - Use modern Python 3.14+ syntax (type statements, pattern matching)
    - [x] 1.4 Add configuration options to pyproject.toml
        - Add `[tool.storytime.pytest]` section with example settings
        - Document `story_paths` (list of directory paths, default: ["examples/"])
        - Document `enabled` (boolean, default: true)
    - [x] 1.5 Ensure configuration tests pass
        - Run ONLY the 2-8 tests written in 1.1
        - Verify config reading works correctly
        - Verify default values applied when section missing
        - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**

- The 2-8 tests written in 1.1 pass
- Plugin registered in pyproject.toml entry points
- Config schema defined and documented
- Default paths work out of the box

### Discovery and Collection Layer

#### Task Group 2: Test Discovery and Collection Hooks

**Dependencies:** Task Group 1

- [x] 2.0 Complete test discovery and collection
    - [x] 2.1 Write 2-8 focused tests for test discovery
        - Test `pytest_collect_file` hook discovers `stories.py` files
        - Test discovery only scans configured `story_paths`
        - Test discovery ignores files outside configured paths
        - Test `make_site()` builds story tree correctly
        - Test traversal finds stories with non-empty assertions
        - Limit to 2-8 highly focused tests maximum
    - [x] 2.2 Implement `pytest_collect_file` hook
        - Scan only directories specified in `story_paths` config
        - Use Path.rglob("stories.py") pattern for discovery
        - Return custom Collector for each stories.py file found
        - Read config using pytest.Config API
    - [x] 2.3 Create custom pytest Collector class
        - Implement StoryFileCollector extending pytest.File
        - Override collect() method to generate test items
        - Use `make_site()` from storytime.site.helpers to build tree
        - Handle tree traversal to find all Story instances
    - [x] 2.4 Implement story tree traversal logic
        - Traverse Site -> Section -> Subject -> Story hierarchy
        - Filter stories with non-empty `assertions` list
        - Extract story path from parent chain (Subject -> Section -> Site)
        - Use structural pattern matching for tree navigation
    - [x] 2.5 Ensure discovery tests pass
        - Run ONLY the 2-8 tests written in 2.1
        - Verify stories.py files discovered in configured paths
        - Verify stories with assertions identified correctly
        - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**

- The 2-8 tests written in 2.1 pass
- `pytest_collect_file` hook discovers stories.py files
- Custom Collector traverses story tree
- Only configured paths scanned

### Test Generation Layer

#### Task Group 3: pytest Item Creation and Naming

**Dependencies:** Task Group 2

- [x] 3.0 Complete test item generation
    - [x] 3.1 Write 2-8 focused tests for test item creation
        - Test one pytest Item generated per assertion
        - Test naming convention: `test_story[site.section.subject.story_name::assertion_name]`
        - Test story path extraction from hierarchy
        - Test assertion naming (1-based index: "Assertion 1", "Assertion 2")
        - Test filesystem-safe name generation
        - Limit to 2-8 highly focused tests maximum
    - [x] 3.2 Create custom pytest Item class
        - Implement StoryAssertionItem extending pytest.Item
        - Store story reference, assertion callable, and metadata
        - Implement runtest() method for test execution
        - Use modern Python type hints with PEP 695 generics
    - [x] 3.3 Implement test naming convention
        - Format: `test_story[site.section.subject.story_name::assertion_name]`
        - Extract dotted path from Story -> Subject -> Section -> Site
        - Use story index within Subject.items if title unavailable
        - Generate assertion names: "Assertion 1", "Assertion 2", etc. (1-based)
    - [x] 3.4 Generate one test item per assertion
        - Iterate over story.assertions list in Collector.collect()
        - Create StoryAssertionItem for each assertion
        - Pass story, assertion callable, and metadata to Item
        - Use flat structure (not hierarchical)
    - [x] 3.5 Ensure test item generation tests pass
        - Run ONLY the 2-8 tests written in 3.1
        - Verify correct number of test items generated
        - Verify test names follow convention
        - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**

- The 2-8 tests written in 3.1 pass
- One test item per assertion created
- Test names follow convention and are filesystem-safe
- Flat test structure used

### Rendering and Isolation Layer

#### Task Group 4: Fresh Rendering and Test Execution

**Dependencies:** Task Group 3

- [x] 4.0 Complete fresh rendering and execution
    - [x] 4.1 Write 2-8 focused tests for fresh rendering
        - Test story rendered fresh for each test execution
        - Test cached `assertion_results` not used
        - Test assertion executed against fresh `story.instance`
        - Test test isolation for parallel execution
        - Test AssertionError capture from assertion callables
        - Limit to 2-8 highly focused tests maximum
    - [x] 4.2 Implement fresh rendering in StoryAssertionItem.runtest()
        - Render story.instance fresh (Element or Fragment)
        - Do NOT use cached `story.assertion_results`
        - Clear any cached results before rendering
        - Call assertion callable with freshly rendered instance
    - [x] 4.3 Implement assertion execution logic
        - Pattern: call assertion(rendered_element)
        - Catch AssertionError exceptions
        - Extract error message from exception
        - Re-raise with enhanced context
    - [x] 4.4 Ensure test isolation for parallel execution
        - Verify each test item independently executable
        - Avoid shared state between test items
        - Ensure stateless execution for pytest-xdist compatibility
        - Test with `pytest -n auto` during development
    - [x] 4.5 Ensure fresh rendering tests pass
        - Run ONLY the 2-8 tests written in 4.1
        - Verify stories render fresh each time
        - Verify no state leakage between tests
        - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**

- The 2-8 tests written in 4.1 pass
- Stories rendered completely fresh per test
- No cached results used
- Test isolation verified for parallel execution

### Reporting Layer

#### Task Group 5: Failure Reporting with Diffs

**Dependencies:** Task Group 4

- [x] 5.0 Complete failure reporting
    - [x] 5.1 Write 2-8 focused tests for failure reporting
        - Test AssertionError capture and message extraction
        - Test HTML rendering of story instance
        - Test unified diff generation using difflib
        - Test failure output includes story metadata
        - Test failure output includes assertion name and error message
        - Limit to 2-8 highly focused tests maximum
    - [x] 5.2 Implement failure message construction
        - Capture AssertionError from assertion callable
        - Extract error message (first line for brevity)
        - Include story metadata: props, title, description
        - Include assertion name and index
    - [x] 5.3 Implement HTML rendering for diffs
        - Render story.instance to HTML string using tdom serialization
        - Generate expected vs actual HTML comparison
        - Use Python's difflib.unified_diff() for diff generation
        - Format diff for terminal readability
    - [x] 5.4 Format failure output for pytest reporter
        - Include sections: story metadata, assertion name, error, diff
        - Use clear section headers and indentation
        - Ensure compatibility with pytest's terminal reporter
        - Test output readability in terminal
    - [x] 5.5 Ensure failure reporting tests pass
        - Run ONLY the 2-8 tests written in 5.1
        - Verify rich failure messages generated
        - Verify diffs are readable and helpful
        - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**

- The 2-8 tests written in 5.1 pass
- Failure messages include all required information
- Unified diffs generated correctly
- Output formatted for excellent terminal readability

### Fixtures and Manual Testing Layer

#### Task Group 6: Manual Testing Fixtures and Examples

**Dependencies:** Task Groups 1-5

- [x] 6.0 Complete manual testing support
    - [x] 6.1 Write 2-8 focused tests for fixtures
        - Test `storytime_site` fixture returns loaded Site instance
        - Test `storytime_story` fixture factory accesses stories by path
        - Test fixture session scope for performance
        - Test fixture usage in manual tests
        - Limit to 2-8 highly focused tests maximum
    - [x] 6.2 Implement `storytime_site` fixture
        - Return loaded Site instance from configured paths
        - Use session scope for performance
        - Call `make_site()` with configured package location
        - Document fixture usage in docstring
    - [x] 6.3 Implement `storytime_story` fixture factory
        - Accept story path as parameter (dotted notation)
        - Use `find_path()` to traverse tree
        - Return specific Story instance
        - Document usage examples in docstring
    - [x] 6.4 Create example tests in `/tests/`
        - Example: accessing specific story and running custom assertions
        - Example: parameterized tests across multiple stories
        - Example: testing story metadata and structure
        - Keep examples concise and well-commented
    - [x] 6.5 Ensure fixture tests pass
        - Run ONLY the 2-8 tests written in 6.1
        - Verify fixtures work correctly
        - Verify example tests demonstrate manual testing
        - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**

- The 2-8 tests written in 6.1 pass
- `storytime_site` and `storytime_story` fixtures implemented
- Example tests demonstrate manual testing capability
- Fixtures well-documented with usage examples

### Testing and Quality Layer

#### Task Group 7: Comprehensive Testing and Quality Checks

**Dependencies:** Task Groups 1-6

- [x] 7.0 Review existing tests and fill critical gaps only
    - [x] 7.1 Review tests from Task Groups 1-6
        - Review the 2-8 tests written for configuration (Task 1.1)
        - Review the 2-8 tests written for discovery (Task 2.1)
        - Review the 2-8 tests written for test items (Task 3.1)
        - Review the 2-8 tests written for rendering (Task 4.1)
        - Review the 2-8 tests written for reporting (Task 5.1)
        - Review the 2-8 tests written for fixtures (Task 6.1)
        - Total existing tests: approximately 12-48 tests
    - [x] 7.2 Analyze test coverage gaps for pytest plugin feature only
        - Identify critical user workflows that lack test coverage
        - Focus ONLY on gaps related to pytest plugin requirements
        - Do NOT assess entire application test coverage
        - Prioritize end-to-end workflows over unit test gaps
    - [x] 7.3 Write up to 10 additional strategic tests maximum
        - Add maximum of 10 new tests to fill identified critical gaps
        - Focus on integration points and end-to-end workflows
        - Test with pytest-xdist parallel execution
        - Test edge cases: empty assertions, invalid paths, malformed config
        - Test error handling and validation
        - Do NOT write comprehensive coverage for all scenarios
    - [x] 7.4 Run feature-specific tests only
        - Run ONLY tests related to pytest plugin feature
        - Expected total: approximately 22-58 tests maximum
        - Verify all tests pass
        - Do NOT run the entire application test suite
    - [x] 7.5 Run quality checks
        - Run `just test` (feature-specific tests only)
        - Run `just typecheck` to verify type hints
        - Run `just fmt` to format code
        - Ensure all checks pass before considering feature complete
    - [x] 7.6 Test parallel execution with pytest-xdist
        - Run `pytest -n auto` to verify parallel compatibility
        - Verify no race conditions or shared state issues
        - Verify test isolation maintained across workers
        - Confirm test results consistent with serial execution

**Acceptance Criteria:**

- All feature-specific tests pass (approximately 22-58 tests total)
- Critical user workflows for pytest plugin covered
- No more than 10 additional tests added when filling gaps
- All quality checks pass (`just test`, `just typecheck`, `just fmt`)
- Parallel execution with pytest-xdist works correctly

## Execution Order

Recommended implementation sequence:

1. **Foundation Layer** (Task Group 1): Configuration schema and plugin registration
2. **Discovery and Collection Layer** (Task Group 2): Test discovery and collection hooks
3. **Test Generation Layer** (Task Group 3): pytest Item creation and naming
4. **Rendering and Isolation Layer** (Task Group 4): Fresh rendering and test execution
5. **Reporting Layer** (Task Group 5): Failure reporting with diffs
6. **Fixtures and Manual Testing Layer** (Task Group 6): Manual testing fixtures and examples
7. **Testing and Quality Layer** (Task Group 7): Comprehensive testing and quality checks

## Key Technical Notes

### Python 3.14+ Standards (from CLAUDE.md)

- Use `type` statement for type aliases (e.g., `type StoryPath = str`)
- Use structural pattern matching (`match`/`case`) for tree traversal
- Use PEP 604 union syntax (`X | Y` instead of `Union[X, Y]`)
- Use built-in generics (`list[str]` instead of `List[str]`)
- Use PEP 695 syntax for generic functions where appropriate

### pytest Plugin Patterns

- Entry point registration: `[project.entry-points.pytest11]`
- Collection hooks: `pytest_collect_file`
- Custom classes: extend `pytest.File` (Collector) and `pytest.Item`
- Config API: use `pytest.Config.getini()` for reading settings

### Existing Code to Leverage

- `Story.assertions`: list of AssertionCallable
- `Story.instance`: property that renders component
- `make_site(package_location)`: builds complete story tree
- `find_path(site, path)`: traverses tree using dotted notation
- `AssertionCallable = Callable[[Element | Fragment], None]`
- `AssertionResult = tuple[str, bool, str | None]`

### Test Isolation Strategy

- Always render `story.instance` fresh
- Do NOT use cached `story.assertion_results`
- Ensure stateless execution for pytest-xdist compatibility
- Avoid shared state between test items

### Failure Reporting Format

```
Story: examples.huge_assertions.forms.form_button[1]
Props: {'text': 'Disabled', 'variant': 'secondary', 'state': 'disabled'}
Assertion: Assertion 2

AssertionError: No common tags

Expected vs Actual HTML:
--- expected
+++ actual
@@ -1,2 +1,2 @@
-<div>...</div>
+<span>...</span>
```
