# Task Breakdown: Story Assertions

## Overview

Total Task Groups: 5
Feature: Add server-side assertion capabilities that execute during StoryView rendering and display visual pass/fail
badges in the browser.

## Task List

### Foundation Layer

#### Task Group 1: Data Models and Type Definitions

**Dependencies:** None

- [x] 1.0 Complete Story model updates for assertions
    - [x] 1.1 Write 2-8 focused tests for Story model assertion fields
        - Test Story creation with populated assertions list
        - Test Story creation with empty assertions list
        - Test assertion_results field initialization
        - Test type safety of assertions field (accepts callables)
        - Verify field defaults (default_factory for empty lists)
    - [x] 1.2 Add type aliases to models.py
        - Import Element from tdom
        - Import Callable from typing
        - Add `type AssertionCallable = Callable[[Element], None]` after existing type aliases
        - Add `type AssertionResult = tuple[str, bool, str | None]` after AssertionCallable
        - Follow existing pattern: place before class definitions at module level
    - [x] 1.3 Update Story dataclass with new fields
        - Add `assertions: list[AssertionCallable] = field(default_factory=list)` (optional field)
        - Add `assertion_results: list[AssertionResult] = field(default_factory=list)` (optional field)
        - Both fields are **not required** on the dataclass - they have defaults
        - Import field from dataclasses if not already imported
        - Follow existing field pattern with default_factory for mutable defaults
        - Place new fields after existing fields (after template field)
    - [x] 1.4 Ensure Story model tests pass
        - Run ONLY the 2-8 tests written in 1.1
        - Run `just typecheck` to verify type hints are correct
        - Verify assertions field accepts list of callables
        - Verify assertion_results field accepts list of tuples

**Acceptance Criteria:**

- The 2-8 tests written in 1.1 pass
- Type aliases defined using modern `type` statement syntax
- Story model has assertions and assertion_results fields with correct types
- Type checking passes with no errors
- Fields use default_factory pattern for empty list defaults

---

### Assertion Execution Layer

#### Task Group 2: Server-Side Assertion Logic

**Dependencies:** Task Group 1

- [x] 2.0 Complete assertion execution engine
    - [x] 2.1 Write 2-8 focused tests for assertion execution
        - Test assertion execution with passing assertions (no error raised)
        - Test assertion execution with failing assertions (AssertionError raised)
        - Test assertion execution with critical errors (other exceptions)
        - Test position-based naming ("Assertion 1", "Assertion 2")
        - Test error message extraction (only first line captured)
        - Test assertion results storage format
    - [x] 2.2 Add CLI flag to __main__.py serve command
        - Add `with_assertions: bool` parameter to serve() function
        - Use typer.Option with default True
        - Add flag: `--with-assertions/--no-with-assertions`
        - Add help text: "Enable assertion execution during StoryView rendering (default: True)"
        - Pass flag through create_app() to make available to views
        - Follow existing pattern from use_subinterpreters flag
    - [x] 2.3 Pass with_assertions flag through app creation chain
        - Update create_app() signature to accept with_assertions parameter
        - Store flag in app.state.with_assertions for view access
        - Default to True if not provided (maintains backward compatibility)
        - Follow existing pattern from subinterpreter pool setup
    - [x] 2.4 Implement assertion execution in StoryView.__call__()
        - Import logging module and create logger
        - Add assertion execution after story instance rendering
        - Only execute if story.assertions is not empty
        - Only execute if with_assertions flag is enabled (check app.state if available)
        - Get rendered element from self.story.instance before executing
        - Iterate with enumerate: `for i, assertion in enumerate(self.story.assertions, start=1)`
        - Generate name: `f"Assertion {i}"`
    - [x] 2.5 Add exception handling for assertion execution
        - Catch AssertionError: extract first line of error with `str(e).split('\n')[0]`
        - Record as: `(name, False, error_message)`
        - Catch all other exceptions: prefix with "Critical error: "
        - Log critical errors: `logger.error(f"Critical error in {name}: {e}", exc_info=True)`
        - Record as: `(name, False, f"Critical error: {error_msg}")`
        - For passing assertions: `(name, True, None)`
        - Store all results in self.story.assertion_results
    - [x] 2.6 Ensure assertion execution tests pass
        - Run ONLY the 2-8 tests written in 2.1
        - Verify assertions execute correctly
        - Verify CLI flag controls execution
        - Verify error handling prevents crashes

**Acceptance Criteria:**

- The 2-8 tests written in 2.1 pass
- CLI flag --with-assertions works (default: True)
- Assertions execute after story rendering
- Position-based naming works ("Assertion 1", "Assertion 2")
- AssertionError handled gracefully (no server crash)
- Other exceptions logged and handled (no server crash)
- Results stored in correct format: list[tuple[str, bool, str | None]]

---

### UI Layer

#### Task Group 3: Badge Rendering and Visual Design

**Dependencies:** Task Group 2

- [x] 3.0 Complete StoryView badge UI
    - [x] 3.1 Write 2-8 focused tests for badge rendering
        - Test badge display with passing assertions
        - Test badge display with failing assertions
        - Test badge display with critical errors
        - Test no badges when assertions empty
        - Test no badges when with_assertions disabled
        - Test mouseover tooltip (title attribute) on failed badges
        - Use aria-testing for accessibility verification
    - [x] 3.2 Update StoryView template header layout
        - Modify Mode B template (default layout) to support badge display
        - Add flexbox/grid container for header with justify-content: space-between
        - Left side: title and description (existing content)
        - Right side: badge container (new)
        - Use semantic HTML for accessibility
        - Follow existing tdom html(t'''...) pattern
    - [x] 3.3 Implement conditional badge rendering logic
        - Only render badges section when story.assertion_results is not empty
        - Skip badges when with_assertions flag disabled
        - Skip badges when story.assertions is empty/None
        - Iterate over story.assertion_results: `for name, passed, error_msg in story.assertion_results`
        - Render each badge based on pass/fail status
    - [x] 3.4 Design badge components using PicoCSS
        - Research PicoCSS badge/pill patterns from documentation
        - Green badge (success): use PicoCSS success semantic class
        - Red badge (failure): use PicoCSS danger semantic class
        - Small, compact design with rounded corners
        - Badge content: assertion name (e.g., "Assertion 1")
        - Failed badges: add title attribute with error_msg for mouseover tooltip
        - Use inline styles if PicoCSS doesn't have built-in pill badges
        - Follow existing PicoCSS usage patterns from Layout component
    - [x] 3.5 Add custom CSS if needed for badge styling
        - Check if storytime.css needs additional badge styles
        - Ensure badges are right-aligned in header
        - Ensure badges don't wrap awkwardly on mobile
        - Follow responsive design principles
        - Test visual appearance in browser during development
    - [x] 3.6 Ensure badge UI tests pass
        - Run ONLY the 2-8 tests written in 3.1
        - Verify badges render correctly for all states
        - Verify accessibility with aria-testing
        - Verify conditional display logic works

**Acceptance Criteria:**

- The 2-8 tests written in 3.1 pass
- Badges display in StoryView header (right-aligned)
- Green badges for passing assertions
- Red badges for failing assertions
- Mouseover tooltip shows error message on failed badges
- No badges shown when assertions empty or disabled
- Responsive design works on mobile/tablet/desktop
- Accessibility verified with aria-testing

---

### Integration Layer

#### Task Group 4: End-to-End Integration

**Dependencies:** Task Groups 1-3

- [ ] 4.0 Complete end-to-end integration
    - [ ] 4.1 Write 2-8 focused integration tests
        - Test complete flow: Story with assertions -> StoryView rendering -> badges displayed
        - Test CLI flag integration: --with-assertions vs --no-with-assertions
        - Test hot-reload behavior: assertions re-execute on file change
        - Test error handling doesn't crash dev server
        - Test multiple assertions in single story
        - Test mixed pass/fail assertions in single story
    - [ ] 4.2 Verify StoryView has access to app state
        - Ensure StoryView can access app.state.with_assertions flag
        - May need to pass flag through Site or rendering context
        - Follow existing pattern for passing configuration to views
        - Update StoryView constructor if needed to accept flag parameter
    - [ ] 4.3 Test with real component examples
        - Create example story with lambda assertions
        - Verify assertions execute during hot-reload development
        - Verify badges display correctly in browser
        - Test mouseover tooltips work
        - Verify server doesn't crash on assertion failures
    - [ ] 4.4 Document CLI flag usage
        - Update help text if needed
        - Ensure default behavior is clear (assertions enabled by default)
        - Verify negative form works: --no-with-assertions
    - [ ] 4.5 Ensure integration tests pass
        - Run ONLY the 2-8 tests written in 4.1
        - Verify complete workflow functions correctly
        - Test in actual browser during development

**Acceptance Criteria:**

- The 2-8 tests written in 4.1 pass
- Complete workflow tested: assertions -> execution -> badge display
- CLI flag properly controls assertion execution
- Hot-reload works correctly with assertions
- Real component examples work in browser
- Server remains stable with failing assertions

---

### Testing and Quality

#### Task Group 5: Test Review and Quality Checks

**Dependencies:** Task Groups 1-4

- [ ] 5.0 Review tests and ensure quality standards
    - [ ] 5.1 Review all tests from Task Groups 1-4
        - Review 2-8 tests from Story model (Task 1.1)
        - Review 2-8 tests from assertion execution (Task 2.1)
        - Review 2-8 tests from badge rendering (Task 3.1)
        - Review 2-8 tests from integration (Task 4.1)
        - Total existing tests: approximately 8-32 tests
    - [ ] 5.2 Analyze test coverage gaps for Story Assertions feature only
        - Identify critical user workflows lacking coverage
        - Focus ONLY on gaps related to Story Assertions feature
        - Do NOT assess entire application test coverage
        - Prioritize end-to-end workflows over unit test gaps
    - [ ] 5.3 Write up to 10 additional tests maximum IF needed
        - Add tests ONLY for critical gaps identified in 5.2
        - Focus on edge cases like:
            - Empty error messages
            - None vs empty list for assertions
            - Assertions that return non-None (should still pass?)
            - Multiple critical errors in sequence
        - Do NOT write comprehensive coverage for all scenarios
        - Skip performance tests, extensive accessibility tests unless business-critical
    - [ ] 5.4 Run feature-specific tests only
        - Run ONLY tests related to Story Assertions feature
        - Expected total: approximately 18-42 tests maximum
        - Do NOT run entire application test suite
        - Verify all critical workflows pass
    - [ ] 5.5 Run quality checks
        - Run `just test` (focused on Story Assertions tests)
        - Run `just typecheck` (verify all type hints are correct)
        - Run `just fmt` (format all modified code)
        - Ensure all quality checks pass before considering task complete
    - [ ] 5.6 Manual browser testing
        - Start dev server with `python -m storytime serve`
        - Test with example story containing assertions
        - Verify badges display correctly
        - Verify mouseover tooltips work
        - Test --no-with-assertions flag disables badges
        - Verify hot-reload re-executes assertions

**Acceptance Criteria:**

- All Story Assertions tests pass (approximately 18-42 tests total)
- No more than 10 additional tests added in gap-filling
- Type checking passes with no errors (just typecheck)
- Code formatting is correct (just fmt)
- Manual browser testing confirms expected behavior
- Feature works correctly with hot-reload development

---

## Execution Order

Recommended implementation sequence:

1. **Task Group 1** - Foundation Layer (data models, type definitions)
    - Establishes the data structures for assertions
    - Defines type-safe interfaces
    - No dependencies

2. **Task Group 2** - Assertion Execution Layer (server-side logic)
    - Implements the core assertion execution engine
    - Adds CLI flag control
    - Depends on Task Group 1 (needs Story model fields)

3. **Task Group 3** - UI Layer (badge rendering, visual design)
    - Implements visual feedback in browser
    - Adds PicoCSS-based badge components
    - Depends on Task Group 2 (needs assertion_results data)

4. **Task Group 4** - Integration Layer (end-to-end workflow)
    - Connects all pieces together
    - Tests complete user workflows
    - Depends on Task Groups 1-3 (needs all layers working)

5. **Task Group 5** - Testing and Quality (gap analysis, quality checks)
    - Reviews test coverage
    - Fills critical gaps
    - Runs quality checks
    - Depends on Task Groups 1-4 (needs complete feature)

---

## Implementation Notes

### Modern Python Standards

All code must use Python 3.14+ features:

- **Type aliases**: Use `type` statement (e.g., `type AssertionCallable = Callable[[Element], None]`)
- **Union syntax**: Use `str | None` instead of `Union[str, None]`
- **Built-in generics**: Use `list[str]` instead of `List[str]`
- **Structural pattern matching**: Use `match`/`case` if applicable for complex conditionals

### Testing Philosophy

Follow the project's testing standards:

- **Minimal tests during development**: 2-8 focused tests per task group
- **Test core user flows only**: Focus on critical behaviors
- **Defer edge cases**: Unless business-critical
- **Fast execution**: Tests should run in milliseconds
- **Descriptive names**: `test_<functionality>_<scenario>` format

### Quality Checks

After each task group, run:

- `just test` - Run focused tests for that task group
- `just typecheck` - Verify type hints
- `just fmt` - Format code

All checks must pass before moving to the next task group.

### Code Reuse Patterns

Leverage existing patterns:

- **Story model**: Follow dataclass pattern with field(default_factory=list)
- **StoryView template**: Use tdom html(t'''...) pattern
- **CLI flags**: Follow typer.Option pattern from use_subinterpreters
- **Exception handling**: Catch specific exceptions, log with context
- **PicoCSS styling**: Follow semantic color classes from Layout component

### Key Technical Decisions

From requirements analysis:

1. **Results storage**: `list[tuple[str, bool, str | None]]` (simple, flat structure)
2. **Callable signature**: `def assertion(element: Element) -> None` (pytest-style)
3. **Execution timing**: After rendering (validate final output)
4. **Exception handling**: Catch all, distinguish AssertionError from critical errors
5. **Assertion naming**: Position-based for lambda compatibility ("Assertion 1", "Assertion 2")
6. **Badge visibility**: Conditional (only show when results exist)

### Out of Scope

Explicitly NOT included:

- Production environment handling
- Performance optimization (caching, background workers)
- pytest integration for CI/CD
- Interactive assertion debugging
- Assertion history/timeline tracking
- Custom assertion reporters
- Multiple lines of error text (only first line)
- Custom assertion naming/labeling
- Assertion editor/IDE integration

These may be considered for future enhancements.
