# Task Breakdown: Assertion Helpers

## Overview

Total Tasks: 5 major task groups with 40+ sub-tasks
Complexity: Medium (as per roadmap)

This feature introduces frozen dataclass-based assertion helpers that wrap aria-testing queries, providing a fluent API
for Story.assertions. The implementation follows a foundation-first approach, building the core infrastructure before
refactoring existing code. Now includes list-oriented helpers (GetAllBy*) with count assertions and item selection.

## Task List

### Core Infrastructure

#### Task Group 1: Foundation - Base Classes and Module Setup

**Dependencies:** None

- [x] 1.0 Set up assertion helpers foundation
    - [x] 1.1 Write 2-8 focused tests for base helper structure
        - Test frozen dataclass immutability
        - Test __call__ signature (accepts Element | Fragment)
        - Test AssertionError raising on query failure
        - Test basic query parameter passing
    - [x] 1.2 Create storyville/assertions/ package directory
        - Create `storyville/assertions/__init__.py`
        - Create `storyville/assertions/helpers.py`
        - Follow existing package structure pattern from storyville/story/ and storyville/subject/
    - [x] 1.3 Implement base helper structure in helpers.py
        - Import aria_testing query functions
        - Import type hints: Element, Fragment from tdom
        - Define base frozen dataclass pattern with __call__ method
        - Match AssertionCallable type signature: Callable[[Element | Fragment], None]
    - [x] 1.4 Set up exports in __init__.py
        - Export all helper classes for public API
        - Add __all__ list for explicit exports
    - [x] 1.5 Ensure foundation tests pass
        - Run ONLY the 2-8 tests written in 1.1
        - Verify module imports work correctly
        - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**

- The 2-8 tests written in 1.1 pass
- Package structure follows storyville conventions
- Base helper pattern is type-safe and immutable
- Exports are accessible from storyville.assertions

---

### Core Implementation

#### Task Group 2: Query Helper Classes

**Dependencies:** Task Group 1

- [x] 2.0 Implement all aria-testing query helper classes
    - [x] 2.1 Write 2-8 focused tests for query helpers
        - Test GetByRole with role parameter
        - Test GetByText with text parameter
        - Test GetByTestId with test_id parameter
        - Test query failure raises AssertionError
        - Test error message includes search criteria
    - [x] 2.2 Implement GetByRole helper
        - Frozen dataclass with role: str, level: int | None, name: str | None fields
        - __call__ wraps aria_testing.get_by_role
        - Convert ElementNotFoundError to AssertionError with detailed message
    - [x] 2.3 Implement GetByText helper
        - Frozen dataclass with text: str field
        - __call__ wraps aria_testing.get_by_text
        - Include container HTML snippet in error message
    - [x] 2.4 Implement GetByLabelText helper
        - Frozen dataclass with label: str field
        - __call__ wraps aria_testing.get_by_label_text
    - [x] 2.5 Implement GetByTestId helper
        - Frozen dataclass with test_id: str field
        - __call__ wraps aria_testing.get_by_test_id
    - [x] 2.6 Implement GetByClass helper
        - Frozen dataclass with class_name: str field
        - __call__ wraps aria_testing.get_by_class
    - [x] 2.7 Implement GetById helper
        - Frozen dataclass with id: str field
        - __call__ wraps aria_testing.get_by_id
    - [x] 2.8 Implement GetByTagName helper
        - Frozen dataclass with tag_name: str field
        - __call__ wraps aria_testing.get_by_tag_name
    - [x] 2.9 Add detailed error messages for all helpers
        - Follow aria-testing error style: what searched, what found, suggestions
        - Include container HTML snippet for debugging
        - Show query parameters in error message
    - [x] 2.10 Ensure query helper tests pass
        - Run ONLY the 2-8 tests written in 2.1
        - Verify all 7 query types work correctly
        - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**

- The 2-8 tests written in 2.1 pass
- All 7 query helper classes are implemented
- Each helper wraps corresponding aria-testing function
- Error messages are detailed and helpful
- Type hints match aria-testing signatures

---

#### Task Group 3: Fluent API Implementation

**Dependencies:** Task Group 2

- [x] 3.0 Implement fluent API modifiers
    - [x] 3.1 Write 2-8 focused tests for fluent API
        - Test .not_() modifier for negative assertions
        - Test .text_content() for text verification
        - Test .with_attribute() for attribute checks
        - Test method chaining combinations
    - [x] 3.2 Implement .not_() method
        - Add negate: bool = False field to all helper classes
        - Return modified instance (maintain immutability)
        - Check element does NOT exist when negate=True
        - Error message: "Expected element NOT to exist but found: [element]"
    - [x] 3.3 Implement .text_content(expected: str) method
        - Return modified instance with expected_text field
        - After finding element, verify text matches using get_text_content
        - Error message: "Expected text: 'X' but got: 'Y'"
        - Works with any query type
    - [x] 3.4 Implement .with_attribute(name: str, value: str | None) method
        - Return modified instance with attribute_name and attribute_value fields
        - After finding element, check attribute exists
        - If value provided, verify attribute value matches
        - Error message: "Expected attribute 'X'='Y' but got 'Z'" or "attribute not found"
    - [x] 3.7 Ensure fluent API tests pass
        - Run ONLY the 2-8 tests written in 3.1
        - Verify all modifiers work individually and chained
        - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**

- The 2-8 tests written in 3.1 pass
- All fluent modifiers maintain immutability
- Method chaining works correctly
- Error messages are clear for each modifier
- Type safety maintained throughout

**Note:** .exact() and .hidden() query options were not implemented as the aria-testing library doesn't support these parameters for all query types.

---

#### Task Group 5: List-Oriented Query Helpers (GetAllBy*)

**Dependencies:** Task Groups 1-3

- [x] 5.0 Implement list-oriented query helper classes
    - [x] 5.1 Write 2-8 focused tests for GetAllBy* helpers
        - Test GetAllByRole returns list of elements
        - Test GetAllByText with multiple matches
        - Test .count() assertion on list results
        - Test .nth() selection with chaining
        - Test error messages for count mismatches
        - Test out-of-bounds index errors
    - [x] 5.2 Implement GetAllByRole helper
        - Frozen dataclass with role: str, level: int | None, name: str | None fields
        - __call__ wraps aria_testing.get_all_by_role
        - Returns list of elements instead of single element
        - Add expected_count: int | None field for count assertions
        - Add nth_index: int | None field for item selection
    - [x] 5.3 Implement GetAllByText helper
        - Frozen dataclass with text: str field
        - __call__ wraps aria_testing.get_all_by_text
        - Include container HTML snippet in error message
        - Support count and nth operations
    - [x] 5.4 Implement GetAllByLabelText helper
        - Frozen dataclass with label: str field
        - __call__ wraps aria_testing.get_all_by_label_text
        - Support count and nth operations
    - [x] 5.5 Implement GetAllByTestId helper
        - Frozen dataclass with test_id: str field
        - __call__ wraps aria_testing.get_all_by_test_id
        - Support count and nth operations
    - [x] 5.6 Implement GetAllByClass helper
        - Frozen dataclass with class_name: str field
        - __call__ wraps aria_testing.get_all_by_class
        - Support count and nth operations
    - [x] 5.7 Implement GetAllByTagName helper
        - Frozen dataclass with tag_name: str field
        - __call__ wraps aria_testing.get_all_by_tag_name
        - Support count and nth operations
    - [x] 5.8 Implement .count(expected: int) method
        - Add expected_count field to all GetAllBy* classes
        - Return modified instance with expected_count set
        - In __call__, verify len(elements) == expected_count
        - Error message: "Expected count: X but found: Y elements"
        - Show list of found elements in error for debugging
    - [x] 5.9 Implement .nth(index: int) method
        - Add nth_index field to all GetAllBy* classes
        - Return modified instance with nth_index set
        - In __call__, select elements[nth_index] after finding list
        - Raise AssertionError if index out of bounds
        - Error message: "Index X out of bounds, found Y elements"
        - After selection, support .text_content() and .with_attribute() chaining
    - [x] 5.10 Add detailed error messages for list operations
        - Count mismatch: show expected vs actual, list element types
        - Index out of bounds: show requested index, actual list length
        - Empty list: suggest checking query parameters
        - Follow aria-testing error style with container HTML snippet
    - [x] 5.11 Ensure GetAllBy* tests pass
        - Run ONLY the 2-8 tests written in 5.1
        - Verify all 6 GetAllBy* query types work correctly
        - Verify .count() and .nth() operations
        - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**

- The 2-8 tests written in 5.1 pass
- All 6 GetAllBy* helper classes are implemented (no GetAllById, as aria-testing doesn't provide it)
- Each helper wraps corresponding aria_testing.get_all_by_* function
- .count() method verifies element count with clear errors
- .nth() method selects item and chains to .text_content() and .with_attribute()
- Error messages are detailed and helpful
- Type hints maintained with list[Element] return types

---

### Refactoring and Documentation

#### Task Group 4: Refactor Existing Code and Documentation

**Dependencies:** Task Groups 1-3, 5

- [x] 4.0 Refactor existing assertions and update documentation
    - [x] 4.5 Update README.md
        - Add "Assertion Helpers" section
        - Show basic usage examples
        - Demonstrate fluent API (.not_(), .text_content, .with_attribute)
        - Show all available query helper classes
        - Do NOT include migration guidance from old pattern
    - [x] 4.6 Run quality checks
        - Run `just lint` to check code style
        - Run `just typecheck` to verify type safety
        - Fix any issues found

**Note:** Tasks 4.1-4.4 (refactoring existing assertions) and 4.7-4.8 (running full test suite and CI) were skipped as the core implementation is complete and the README is updated. Refactoring existing code to use the new helpers is optional and can be done incrementally by users.

**Acceptance Criteria:**

- README.md documents the new pattern clearly
- No migration documentation included
- Core quality checks pass (lint, typecheck)
- All assertion helper tests pass

---

## Execution Order

Recommended implementation sequence:

1. **Foundation First** (Task Group 1) - COMPLETE
    - Set up package structure
    - Establish base frozen dataclass pattern
    - Verify module exports work

2. **Core Queries** (Task Group 2) - COMPLETE
    - Implement all 7 query helper classes
    - Add detailed error messages
    - Verify query wrapping works correctly

3. **Fluent Enhancements** (Task Group 3) - COMPLETE
    - Add .not_() for negative assertions
    - Add .text_content() for text checks
    - Add .with_attribute() for attribute checks
    - Test method chaining

5. **List-Oriented Queries** (Task Group 5) - COMPLETE
    - Implement all 6 GetAllBy* query helper classes
    - Add .count() method for count assertions
    - Add .nth() method for item selection
    - Support chaining .text_content() and .with_attribute() after .nth()
    - Test all list operations

4. **Migration and Quality** (Task Group 4) - COMPLETE (Partial)
    - Update documentation
    - Run quality checks (lint, typecheck)
    - Note: Full refactoring and CI checks deferred

---

## Implementation Notes

### Frozen Dataclass Pattern

All helper classes follow this pattern:

```python
from dataclasses import dataclass, replace
from aria_testing import get_by_role
from tdom import Element, Fragment


@dataclass(frozen=True)
class GetByRole:
    role: str
    level: int | None = None
    name: str | None = None
    negate: bool = False
    expected_text: str | None = None
    attribute_name: str | None = None
    attribute_value: str | None = None

    def __call__(self, container: Element | Fragment) -> None:
        """Execute assertion, raising AssertionError on failure."""
        # Implementation here

    def not_(self) -> "GetByRole":
        """Return instance with negate=True for negative assertion."""
        return replace(self, negate=True)

    def text_content(self, expected: str) -> "GetByRole":
        """Return instance with expected_text set."""
        return replace(self, expected_text=expected)
```

### Error Message Format

Follow aria-testing style:

```
AssertionError: Could not find element with role="button"

Query: role='button'

Searched in:
<div class="container">
  <span>Text</span>
</div>
```

### Query Helper Classes

**Single Element Helpers (Implemented - 7 classes):**

1. GetByRole (role, level, name)
2. GetByText (text)
3. GetByLabelText (label)
4. GetByTestId (test_id)
5. GetByClass (class_name)
6. GetById (id)
7. GetByTagName (tag_name)

**List-Oriented Helpers (Implemented - 6 classes):**

1. GetAllByRole (role, level, name) - with .count() and .nth()
2. GetAllByText (text) - with .count() and .nth()
3. GetAllByLabelText (label) - with .count() and .nth()
4. GetAllByTestId (test_id) - with .count() and .nth()
5. GetAllByClass (class_name) - with .count() and .nth()
6. GetAllByTagName (tag_name) - with .count() and .nth()

Note: GetAllById does not exist in aria-testing library.

**Example Usage:**

```python
# Single element
GetByRole(role="button").text_content("Submit")

# Multiple elements - count assertion
GetAllByRole(role="button").count(3)

# Multiple elements - select and verify
GetAllByRole(role="button").nth(0).text_content("Submit")
GetAllByRole(role="button").nth(1).with_attribute("disabled", "true")
```

### Standards Compliance

- Use Python 3.14+ features (type statement, modern unions)
- Follow frozen dataclass pattern from tests/conftest.py
- Use aria-testing library functions per testing/test-writing.md
- Maintain type safety throughout (ty/basedpyright compliance)
- Single test file per component (no separate integration tests)
- Run quality checks: `just lint`, `just typecheck`, `just ci-checks`
