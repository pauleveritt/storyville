# Spec Requirements: Story Assertions

## Initial Description

Add assertion capabilities to Storytime stories that run in the **StoryView UI** during development, displaying **pass/fail badges** in the rendered HTML page.

### Key Design Decision

Assertions should execute in the StoryView component (the browser-based story renderer), not just in pytest. This means:

- Assertions run during hot-reload development in the browser
- Visual feedback (badges) shows pass/fail status directly in the rendered page
- Developers see assertion results immediately as they code, without running pytest

This is a significant architectural decision that affects:
- Where assertions execute (browser context vs test context)
- When they execute (every render vs on-demand)
- How errors are displayed (visual badges vs test output)
- Performance considerations (assertions running on every hot-reload)
- Safety/sandboxing (assertions running in production-like UI context)

## Product Context

**Product Mission:**
Storytime is a component-driven development (CDD) platform that helps Python developers create, visualize, and test UI components by providing a Storybook-like experience that is framework-independent and fully integrated with Python's modern testing ecosystem.

**Current State:**
- Hot reload development server: Complete
- Component organization system: Complete
- Next priorities: Story-to-test integration, component browser, CLI workflow

**How This Feature Fits:**
Story assertions directly support the "Story-to-Test Integration" roadmap item by enabling developers to:
- Write assertions alongside stories for immediate visual feedback
- Validate component rendering during development (not just in CI/CD)
- Bridge the gap between visual development and automated testing

## Requirements Discussion

### First Round Questions

**Q1: Execution Timing**
When should assertions run?
**Answer:** Run on every StoryView render. Check later if performance impact is too high.

**Q2: Badge Placement**
Where should badges appear in the UI?
**Answer:** StoryView header with title and description on the left and badge on the right.

**Q3: Error Display**
How should assertion failures be shown to users?
**Answer:** Mouseover to see text on assertion failure (use title attribute). One line of text only.

**Q4: Production Environment**
Should assertions run in production?
**Answer:** Don't worry about production for now.

**Q5: Performance & Caching**
Should we consider caching assertion results or background workers?
**Answer:** Good ideas - keep notes on all 3 choices (run every render, cache, background worker), but implement none for now.

**Q6: pytest Integration**
How do assertions integrate with pytest?
**Answer:** Assertions don't run in the browser yet. Look at pytest integration later.

**Q7: Field Naming**
Should the Story field be `assertion` (singular) or `assertions` (plural)?
**Answer:** Use `assertions` (plural).

**Q8: Badge Visual Design**
What should the badge styling look like?
**Answer:** Small pill-based using PicoCSS.

**Q9: Critical Architecture Clarification**
Where exactly do assertions execute?
**Answer:** Assertions don't run in browser - they run during `StoryView` rendering (server-side). The process is:
- Grab an assertion
- Execute it during rendering
- Capture the failure/success
- Store results on the Story object
- Later render results to HTML (badges)
- This means `Story` needs a place to store assertion results for later rendering to HTML

**Q10: Out of Scope Features**
What features are explicitly out of scope?
**Answer:** All advanced features are out of scope:
- Interactive assertion debugging
- Assertion history/timeline
- Custom assertion reporters
- Assertion performance profiling

### Technical Decision Questions

The following technical architecture decisions were made after the initial requirements gathering:

**TD1: Assertion Results Storage Type**
What type should be used to store assertion results on the Story object?

**Decision:** Option A - `list[tuple[str, bool, str | None]]`

**Structure:**
- Simple list of tuples
- Each tuple contains: `(assertion_name, passed, error_message)`
- `error_message` is `None` when assertion passes

**Rationale:**
- Straightforward to iterate over for badge rendering
- No nested structures to navigate
- Clear separation of concerns (name, status, error)

---

**TD2: Assertion Callable Signature**
What should the signature of assertion callables be?

**Decision:** Option B - `def assertion(element: Element) -> None`

**Signature:**
```python
def assertion(element: Element) -> None:
    # Receives rendered output
    # Raises AssertionError on failure
    # Returns None on success
```

**Rationale:**
- Assertions validate the rendered `Element`/`Fragment` output
- Follows pytest convention of raising on failure
- Clean, simple interface

---

**TD3: Execution Timing**
When should assertions execute relative to rendering?

**Decision:** Choice 2 - After rendering

**Execution Flow:**
1. Story renders (produces `Element`/`Fragment`)
2. Assertions execute against the rendered output
3. Results are collected
4. Badges are displayed in StoryView header

**Rationale:**
- Assertions validate the final rendered state
- Matches typical testing workflow
- Allows assertions to inspect actual output

---

**TD4: Exception Handling Strategy**
Should we catch all exceptions from assertions or let some bubble up?

**Decision:** Option C - Catch assertion errors but log/display critical errors differently

**Specific Implementation:**
- Catch non-assertion exceptions to prevent server crash
- Distinguish between:
  - **AssertionError**: Expected failure (show in red badge)
  - **Other exceptions**: Unexpected errors (log differently, may show warning badge)

**Rationale:**
- Prevents development server from crashing on assertion failures
- Allows developers to continue working even with failing assertions
- Maintains visibility of unexpected errors

---

**TD5: Empty Assertions Display**
What happens if a Story has `assertions=None` or `assertions=[]`?

**Decision:** Option C - Different visual treatment (grayed out badge)

**Visual Treatment:**
- When `assertions=[]` or no assertions defined
- Show grayed out badge or subtle indicator
- Communicates "no assertions configured" vs "assertions passed/failed"

**Rationale:**
- Distinguishes between "no assertions" and "all passing"
- Provides visual consistency
- Encourages developers to add assertions

---

**TD6: Assertion Naming/Identification**
How should assertions be identified in the UI?

**Decision:** Option C - Use position/index (e.g., "Assertion 1", "Assertion 2")

**IMPORTANT CONTEXT:**
User is using **lambda functions** for assertions, not named functions. This means `__name__` will not work (lambdas have generic names like `<lambda>`).

**Implementation:**
- Enumerate assertions by position in the list
- Display as "Assertion 1", "Assertion 2", etc.
- Simple, predictable, works with any callable (including lambdas)

**Rationale:**
- Lambdas don't have meaningful `__name__` attributes
- Position-based naming is reliable and consistent
- Easy to correlate with source code order

### Existing Code to Reference

No specific similar features were identified for direct code reuse. However, the implementation should:
- Follow existing patterns in the `Story` model for field definitions
- Use existing StoryView template patterns for UI integration
- Leverage existing exception handling in the development server
- Follow PicoCSS patterns already in use for badge styling

## Visual Assets

### Files Provided:
No visual assets provided.

### Visual Insights:
Not applicable.

## Requirements Summary

### Functional Requirements

**Core Functionality:**
- Add `assertions` field to `Story` class
- Field type: `list[Callable[[Element], None]]` (list of assertion callables)
- Execute assertions after story renders (server-side during StoryView rendering)
- Collect results in format: `list[tuple[str, bool, str | None]]`
- Display pass/fail badges in StoryView header using PicoCSS pill badges

**Assertion Execution Model:**
1. Story renders to produce `Element`/`Fragment`
2. Each assertion callable receives the rendered `Element`
3. Assertion raises `AssertionError` if validation fails (or returns None on success)
4. Exception handler catches:
   - `AssertionError`: Record as failed assertion
   - Other exceptions: Log as critical error (different treatment to prevent server crash)
5. Results collected as `(name, passed, error_message)` tuples
6. Names generated as "Assertion 1", "Assertion 2", etc. based on position (for lambda compatibility)
7. Results stored on Story object for later rendering to HTML

**UI Display:**
- Badges appear in StoryView header (title/description on left, badges on right)
- Use PicoCSS pill badges for styling (small, pill-based design)
- Visual states:
  - Green badge: Assertion passed
  - Red badge: Assertion failed
  - Gray badge: No assertions defined
  - Warning badge: Critical error (non-assertion exception)
- Badge shows assertion name and status
- Error messages displayed on mouseover (HTML title attribute)
- Only one line of error text shown

**User Actions Enabled:**
- Define assertions as list of callables in `Story` class
- See assertion results immediately during hot-reload development
- Identify failing assertions by position number
- Continue developing even when assertions fail (no server crash)
- Hover over failed badges to see error details

**Data to be Managed:**
- Story model: `assertions` field (list of callables)
- Story model: assertion results storage (list of tuples)
- Runtime: Rendered Element/Fragment passed to assertions
- UI: Badge rendering state

### Reusability Opportunities

**Similar Features Identified:**
No specific similar features were identified during requirements gathering.

**Components to Potentially Reuse:**
- PicoCSS pill badge styling (already in use)
- StoryView header layout and styling
- Exception catching/logging infrastructure in development server

**Backend Patterns to Reference:**
- Story model extension patterns for adding fields
- StoryView rendering pipeline (where to hook in assertion execution)
- Server-side execution during hot-reload
- Exception handling to prevent server crashes

### Scope Boundaries

**In Scope:**
- Adding `assertions` field to `Story` model (plural, list of callables)
- Executing assertions after rendering in StoryView context (server-side)
- Collecting assertion results in format: `list[tuple[str, bool, str | None]]`
- Displaying pass/fail badges in StoryView header (right-aligned)
- Handling assertion errors gracefully (catch AssertionError and other exceptions)
- Position-based assertion naming for lambda compatibility ("Assertion 1", "Assertion 2")
- Different visual treatment for "no assertions" state (grayed out badge)
- Error message display on mouseover using title attribute (one line only)
- Preventing server crashes from assertion failures

**Out of Scope:**
- Production environment handling
- Performance optimization (caching, background workers) - noted for future but not implemented
- pytest integration - deferred for later
- Interactive assertion debugging
- Assertion history/timeline tracking
- Custom assertion reporters
- Assertion performance profiling
- Multiple lines of error text
- Custom assertion naming/labeling (beyond position-based)
- Assertion editor/IDE integration
- Assertion templates/helpers

**Future Enhancements Mentioned:**
- Pytest integration for CI/CD testing
- Performance optimizations (caching, background workers)
- More sophisticated assertion reporting
- Assertion history/tracking over time

### Technical Considerations

**Integration Points:**
- `Story` class: Add `assertions` field and results storage field
- StoryView rendering pipeline: Add post-render assertion execution phase
- StoryView template: Add badge rendering in header
- Development server: Ensure exceptions don't crash server

**Technology Stack:**
- Python 3.14+ (structural pattern matching, modern type hints, PEP 695 generics)
- tdom for templating
- PicoCSS for badge styling
- Starlette for web server
- Uvicorn ASGI server
- Hot reload with subinterpreter pool

**Type Safety:**
```python
from typing import Callable

# Type aliases for clarity
type AssertionCallable = Callable[[Element], None]
type AssertionResult = tuple[str, bool, str | None]

# Story model fields
assertions: list[AssertionCallable]
assertion_results: list[AssertionResult]
```

**Assertion Callable Signature:**
```python
def assertion(element: Element) -> None:
    """
    Validates the rendered Element/Fragment.
    Raises AssertionError on failure.
    Returns None on success.
    """
    # Validation logic here
    if some_condition_fails:
        raise AssertionError("One line error message")
```

**Exception Handling Pattern:**
```python
results: list[AssertionResult] = []

for i, assertion in enumerate(story.assertions):
    name = f"Assertion {i + 1}"  # Position-based naming for lambdas
    try:
        assertion(rendered_element)
        results.append((name, True, None))
    except AssertionError as e:
        # Expected assertion failure
        error_msg = str(e).split('\n')[0]  # First line only
        results.append((name, False, error_msg))
    except Exception as e:
        # Unexpected critical error - log differently
        # May show warning badge with different styling
        error_msg = f"Critical error: {str(e).split('\n')[0]}"
        results.append((name, False, error_msg))
        # Log the full exception for debugging
        logger.error(f"Critical error in {name}: {e}", exc_info=True)

story.assertion_results = results
```

**Badge Rendering Logic:**
```python
# In StoryView template
if not story.assertions:
    # Gray badge for "no assertions"
    render_gray_badge("No assertions")
else:
    for name, passed, error_msg in story.assertion_results:
        if passed:
            render_green_badge(name)
        else:
            # Red badge with title attribute for mouseover
            render_red_badge(name, title=error_msg)
```

**Performance Considerations:**
- Assertions run on every hot-reload render (no caching initially)
- Keep assertion execution lightweight
- Monitor for performance impact during development
- Consider future optimization if needed for large assertion suites
- Notes kept on alternative approaches (caching, background workers)

**Architecture Decisions Summary:**
1. Results storage: `list[tuple[str, bool, str | None]]`
2. Callable signature: `def assertion(element: Element) -> None`
3. Execution timing: After rendering
4. Exception handling: Catch all exceptions, distinguish AssertionError from critical errors
5. Empty assertions: Show grayed out badge
6. Assertion naming: Position-based ("Assertion 1", "Assertion 2") for lambda compatibility

**Similar Code Patterns:**
- Story-based development pattern already established
- Model extension pattern for adding fields
- Server-side rendering execution pattern
- Exception handling in hot-reload server
- PicoCSS styling patterns for badges
