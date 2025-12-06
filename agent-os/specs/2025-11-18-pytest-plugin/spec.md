# Specification: Pytest Plugin for Story Assertions

## Goal
Provide automatic pytest test generation from story assertions with zero manual test writing required, while maintaining great developer experience through clear test names, rich failure reporting, and parallel execution support.

## User Stories
- As a developer, I want story assertions to automatically become pytest tests so I don't have to manually write test boilerplate
- As a developer, I want clear test names and rich failure output so I can quickly identify and debug failing assertions

## Specific Requirements

**Plugin Registration and Discovery**
- Register as pytest plugin via entry point in pyproject.toml under `[project.entry-points.pytest11]`
- Use pytest collection hooks (`pytest_collect_file`) to discover story files
- Only scan directories specified in `[tool.storyville.pytest]` config section
- Default to `story_paths = ["examples/"]` if not configured
- Plugin activates automatically when storyville is installed (no `-p` flag needed)

**Configuration Schema**
- Add `[tool.storyville.pytest]` section to pyproject.toml
- Support `story_paths` setting: list of directory paths to scan (default: `["examples/"]`)
- Support `enabled` setting: boolean to enable/disable plugin (default: true)
- Read config using `pytest.Config.getini()` or similar pytest config API
- Validate paths exist and are readable during collection phase

**Test Collection and Generation**
- Scan configured paths for `stories.py` files using Path.rglob() pattern
- Use `make_site()` helper from `storyville.site.helpers` to build story tree
- Traverse tree to find all Story instances with non-empty `assertions` list
- Generate one pytest test item per assertion in each story
- Use flat structure (not hierarchical) for test organization
- Implement custom pytest Item class to represent each assertion test

**Test Naming Convention**
- Format: `test_story[site.section.subject.story_name::assertion_name]`
- Extract story path from parent hierarchy (Subject -> Section -> Site)
- Use story's index within Subject.items for story_name if title unavailable
- Use assertion index (1-based) for assertion_name: "Assertion 1", "Assertion 2", etc.
- Ensure names are filesystem-safe and pytest-compatible

**Fresh Rendering for Test Isolation**
- Always render stories completely fresh for each test execution
- Do NOT use cached `story.assertion_results` from prior rendering
- Create new Story instance or clear cached results before rendering
- Execute assertion against freshly rendered `story.instance` (Element or Fragment)
- Ensure test isolation for parallel execution compatibility

**Failure Reporting with Diffs**
- Capture AssertionError exceptions from assertion callables
- Extract error message from exception (first line for brevity)
- Render story instance to HTML string using tdom serialization
- Generate unified text diff comparing expected vs actual HTML when applicable
- Use Python's `difflib.unified_diff()` for diff generation
- Include in failure output: story metadata (props, title), assertion name, error message, HTML diff
- Format output for readability in pytest's terminal reporter

**Pytest-xdist Integration**
- Ensure plugin works with `pytest -n auto` (pytest-xdist parallel execution)
- Use pytest's built-in xdist support (no custom parallel implementation)
- Verify each test item is independently executable (stateless)
- Avoid shared state between test items that could cause race conditions
- Test with xdist during plugin development to ensure compatibility

**Manual Testing Fixtures**
- Provide `storyville_site` fixture that returns loaded Site instance
- Provide `storyville_story` fixture factory for accessing specific stories by path
- Allow developers to write custom tests using these fixtures
- Document fixture usage in plugin docstrings and comments
- Fixtures should use session scope where appropriate for performance

**Example Tests Demonstrating Manual Usage**
- Create example tests in `tests/` directory showing fixture usage
- Example: accessing specific story and running custom assertions
- Example: parameterized tests across multiple stories
- Example: testing story metadata and structure
- Keep examples concise and well-commented for documentation purposes

## Existing Code to Leverage

**Story Model with Assertions Support**
- `Story.assertions` field: list of AssertionCallable (already defined in models.py)
- `Story.assertion_results` field: list of AssertionResult tuples (name, passed, error_msg)
- `Story.instance` property: renders component with props and returns Node
- `AssertionCallable` type alias: `Callable[[Element | Fragment], None]`
- Fresh rendering approach: ignore `assertion_results` cache and render story.instance anew

**Site Building and Traversal**
- `make_site(package_location)` from `storyville.site.helpers`: builds complete story tree
- `find_path(site, path)` helper: traverses tree using dotted notation
- TreeNode discovery: uses Path.rglob("stories.py") to find story files
- Story tree hierarchy: Site -> Section -> Subject -> Story

**Pytest Infrastructure**
- Existing `tests/conftest.py` with fixture patterns to follow
- Pytest 9.0.0+ collection hooks and Item/Collector API
- Custom pytest.Config usage for reading pyproject.toml settings
- Pytest parametrization patterns for generating multiple test items

**Existing Assertion Execution Pattern**
- StoryView._execute_assertions() shows how assertions are currently run
- Pattern: iterate assertions, call with rendered_element, catch AssertionError
- Result collection: tuple of (name, bool, error_msg | None)
- Fresh rendering in tests: replicate this pattern but without caching results

**Type Definitions**
- Modern Python 3.14+ type syntax using `type` statement
- `type AssertionCallable = Callable[[Element | Fragment], None]`
- `type AssertionResult = tuple[str, bool, str | None]`
- Use structural pattern matching for type checks where beneficial

## Out of Scope
- Visual regression testing with screenshot comparison (use dedicated tools)
- Accessibility testing beyond what's explicitly defined in story assertions
- Mutation testing of story components
- Coverage reporting specific to stories (use standard pytest-cov)
- Separate package distribution (pytest-storyville) - built into core instead
- Hierarchical test tree organization (use flat structure for simplicity)
- Auto-discovery of all Python files (only scan configured story_paths)
- Custom parallel execution implementation (use pytest-xdist instead)
- Interactive test selection UI (use pytest's built-in selection)
- Assertion auto-generation or suggestion features
