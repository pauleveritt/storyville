# Specification: Story Assertions

## Goal

Add assertion capabilities to Storyville stories that execute server-side during StoryView rendering and display
pass/fail badges in the rendered HTML page, providing immediate visual feedback during hot-reload development.

## User Stories

- As a component developer, I want to define assertions alongside my stories so that I can validate component rendering
  during development
- As a developer, I want to see assertion results as badges in the browser so that I know immediately when my component
  breaks without running pytest

## Specific Requirements

**Story Model: Add assertions field**

- Add `assertions` field to Story dataclass with type `list[Callable[[Element], None]]`
- **Field is optional** - not required on the dataclass
- Field should default to empty list using `field(default_factory=list)`
- Add `assertion_results` field with type `list[tuple[str, bool, str | None]]` to store execution results
- **assertion_results field is also optional** - not required on the dataclass
- Use modern Python type alias: `type AssertionCallable = Callable[[Element], None]`
- Use modern Python type alias: `type AssertionResult = tuple[str, bool, str | None]`
- Follow existing Story model patterns (dataclass, field defaults)
- Import Element from tdom for type hints

**CLI Configuration: Assertion control flag**

- Add `--with-assertions` boolean flag to dev server CLI arguments
- Default value: `True` (assertions enabled by default)
- Support negative form: `--no-with-assertions` to disable
- Pass flag value to StoryView rendering context
- When disabled, skip all assertion execution logic entirely
- Flag controls whether assertions run, not whether they're defined
- Follow existing CLI argument patterns in storyville dev server

**Assertion Execution: Server-side during rendering**

- Execute assertions after story renders in StoryView.__call__() method
- Get rendered element from `self.story.instance` before executing assertions
- Only execute if `self.story.assertions` is not empty
- Only execute if `--with-assertions` CLI flag is enabled
- Pass rendered Element to each assertion callable
- Assertions raise AssertionError on failure, return None on success
- Run on every StoryView render (no caching initially)
- Store results in `self.story.assertion_results` for badge rendering

**Exception Handling: Graceful failure management**

- Catch AssertionError as expected failure (record as failed assertion)
- Catch all other exceptions as critical errors (prevent server crash)
- Extract only first line of error message using `str(e).split('\n')[0]`
- Store results as tuple: `(assertion_name, passed, error_message)`
- For AssertionError: `error_message` contains assertion message
- For other exceptions: `error_message` prefixed with "Critical error: "
- Log critical errors with full stack trace for debugging (use logger.error with exc_info=True)
- Never let assertion failures crash the development server

**Assertion Naming: Position-based identification**

- Generate assertion names based on position in list (1-indexed)
- Use format: "Assertion 1", "Assertion 2", etc.
- Enumerate using `for i, assertion in enumerate(story.assertions)`
- Calculate name as `f"Assertion {i + 1}"`
- Position-based naming works with lambda functions (which have generic `__name__`)

**StoryView Rendering: Badge display in header**

- Modify StoryView template to add assertion badges in header
- Layout: title and description on left, badges on right
- Use flexbox or grid for header layout with justify-content: space-between
- Badges should be compact and aligned to the right edge
- Only render badges section when story has assertion results to display
- When CLI flag disabled: no badges shown (assertions didn't run)
- When assertions empty/None: no badges shown (no assertions defined)
- Iterate over `story.assertion_results` to render each badge

**Badge Visual Design: PicoCSS pill badges**

- Use PicoCSS semantic colors for badge states
- Green badge (success): Use PicoCSS "success" or similar class
- Red badge (failure): Use PicoCSS "danger" or similar class
- Small pill-based design (compact, rounded corners)
- Badge content: assertion name (e.g., "Assertion 1")
- Failed badges: add HTML title attribute with error message for mouseover tooltip
- Follow PicoCSS badge/pill patterns from documentation

**Badge Display Logic: Conditional visibility**

- No badge shown when `story.assertions` is empty or None
- No badge shown when `--with-assertions` CLI flag is disabled
- Distinction: "assertions disabled by CLI" means they didn't run at all
- Distinction: "no assertions defined" means story.assertions is empty/None
- Both cases result in no badge display (clean UI when assertions not in use)
- Only show badges when assertions were executed and results exist

**Story Instance Rendering: Maintain existing behavior**

- Keep existing `story.instance` property for rendering component
- Assertions receive the rendered Element/Fragment from instance property
- Don't modify component rendering logic
- Assertions validate the final rendered output

**Type Safety: Modern Python type hints**

- Use PEP 604 union syntax: `str | None` instead of `Union[str, None]`
- Use built-in generics: `list[AssertionCallable]` instead of `List[AssertionCallable]`
- Use `type` statement for type aliases (Python 3.14+)
- Import Callable from typing module
- Import Element from tdom module
- Follow existing type hint patterns in Story model

**Testing Strategy: Comprehensive test coverage**

- Test Story model with assertions field populated and empty
- Test assertion execution with passing assertions (no errors raised)
- Test assertion execution with failing assertions (AssertionError raised)
- Test assertion execution with critical errors (other exceptions)
- Test position-based naming generation (verify "Assertion 1", "Assertion 2" format)
- Test StoryView badge rendering for all states (pass, fail, critical error)
- Test StoryView badge rendering with no badges when assertions empty/None
- Test CLI flag enabled vs disabled behavior (assertions run vs skipped)
- Test error message extraction (verify only first line captured)
- Test mouseover tooltip with title attribute
- Use aria-testing for accessibility verification of badges

## Visual Design

No visual assets provided. Implementation should follow PicoCSS conventions for pills/badges with semantic colors.

## Existing Code to Leverage

**Story model pattern (src/storyville/story/models.py)**

- Use dataclass decorator for Story class
- Use field(default_factory=dict) pattern for mutable defaults
- Follow existing property pattern for instance property
- Import types from typing and tdom modules
- Use type hints aggressively throughout

**StoryView rendering pattern (src/storyville/story/views.py)**

- Follow dual-mode rendering (custom template vs default layout)
- Use tdom html() with t-string for template rendering
- Access story properties via self.story
- Render story.instance for component output
- Wrap with Layout component in Mode B

**Layout component pattern (src/storyville/components/layout/layout.py)**

- Follow tdom Element/Fragment/Node type hierarchy
- Use html(t'''...) for multi-line templates
- Calculate relative paths for static assets based on depth
- Use PicoCSS classes for styling
- Follow existing header structure pattern

**Exception handling pattern (error-handling.md standard)**

- Fail gracefully for non-critical failures
- Use specific exception types (AssertionError vs Exception)
- Clean up resources in finally blocks (not applicable here)
- Clear, actionable error messages
- Log with full context for debugging

**Type alias pattern (models.py and code-style.md)**

- Use `type` statement for type aliases (Python 3.14+)
- Example: `type Target = type | Callable`
- Example: `type Template = Callable[[], Node]`
- Place type aliases at module level before class definitions

**CLI argument patterns (dev server implementation)**

- Follow existing click or argparse patterns used in dev server
- Boolean flags with default values
- Support negative forms for boolean flags (--no-flag)
- Pass configuration down to view/rendering layer

## Out of Scope

- Production environment handling (assertions may run in production for now)
- Performance optimization (caching assertion results between renders)
- Performance optimization (background workers for assertion execution)
- pytest integration (running assertions in test context vs browser context)
- Interactive assertion debugging tools
- Assertion history or timeline tracking
- Custom assertion reporters or formatters
- Assertion performance profiling or metrics
- Multiple lines of error text (only first line shown)
- Custom assertion naming or labeling (beyond position-based)
- Assertion editor or IDE integration
- Assertion templates or helper libraries
- Browser-side assertion execution (all assertions run server-side)
- Assertion result persistence across server restarts
- Environment variable configuration (only CLI flag for now)
- Per-story assertion toggle (only global CLI flag)
