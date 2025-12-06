# Task Breakdown: Assertion Helpers

## Overview

Total Tasks: 4 major task groups with 24 sub-tasks
Complexity: Medium (as per roadmap)

This feature introduces frozen dataclass-based assertion helpers that wrap aria-testing queries, providing a fluent API
for Story.assertions. The implementation follows a foundation-first approach, building the core infrastructure before
refactoring existing code.

## Task List

### Core Infrastructure

#### Task Group 1: Foundation - Base Classes and Module Setup

**Dependencies:** None

- [ ] 1.0 Set up assertion helpers foundation
    - [ ] 1.1 Write 2-8 focused tests for base helper structure
        - Test frozen dataclass immutability
        - Test __call__ signature (accepts Element | Fragment)
        - Test AssertionError raising on query failure
        - Test basic query parameter passing
    - [ ] 1.2 Create storyville/assertions/ package directory
        - Create `storyville/assertions/__init__.py`
        - Create `storyville/assertions/helpers.py`
        - Follow existing package structure pattern from storyville/story/ and storyville/subject/
    - [ ] 1.3 Implement base helper structure in helpers.py
        - Import aria_testing query functions
        - Import type hints: Element, Fragment from tdom
        - Define base frozen dataclass pattern with __call__ method
        - Match AssertionCallable type signature: Callable[[Element | Fragment], None]
    - [ ] 1.4 Set up exports in __init__.py
        - Export all helper classes for public API
        - Add __all__ list for explicit exports
    - [ ] 1.5 Ensure foundation tests pass
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

- [ ] 2.0 Implement all aria-testing query helper classes
    - [ ] 2.1 Write 2-8 focused tests for query helpers
        - Test GetByRole with role parameter
        - Test GetByText with text parameter
        - Test GetByTestId with test_id parameter
        - Test query failure raises AssertionError
        - Test error message includes search criteria
    - [ ] 2.2 Implement GetByRole helper
        - Frozen dataclass with role: str, level: int | None, name: str | None fields
        - __call__ wraps aria_testing.get_by_role
        - Convert ElementNotFoundError to AssertionError with detailed message
    - [ ] 2.3 Implement GetByText helper
        - Frozen dataclass with text: str field
        - __call__ wraps aria_testing.get_by_text
        - Include container HTML snippet in error message
    - [ ] 2.4 Implement GetByLabelText helper
        - Frozen dataclass with label: str field
        - __call__ wraps aria_testing.get_by_label_text
    - [ ] 2.5 Implement GetByTestId helper
        - Frozen dataclass with test_id: str field
        - __call__ wraps aria_testing.get_by_test_id
    - [ ] 2.6 Implement GetByClass helper
        - Frozen dataclass with class_name: str field
        - __call__ wraps aria_testing.get_by_class
    - [ ] 2.7 Implement GetById helper
        - Frozen dataclass with id: str field
        - __call__ wraps aria_testing.get_by_id
    - [ ] 2.8 Implement GetByTagName helper
        - Frozen dataclass with tag_name: str field
        - __call__ wraps aria_testing.get_by_tag_name
    - [ ] 2.9 Add detailed error messages for all helpers
        - Follow aria-testing error style: what searched, what found, suggestions
        - Include container HTML snippet for debugging
        - Show query parameters in error message
    - [ ] 2.10 Ensure query helper tests pass
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

- [ ] 3.0 Implement fluent API modifiers
    - [ ] 3.1 Write 2-8 focused tests for fluent API
        - Test .not modifier for negative assertions
        - Test .text_content() for text verification
        - Test .with_attribute() for attribute checks
        - Test .exact() query option
        - Test .hidden() query option
        - Test method chaining combinations
    - [ ] 3.2 Implement .not property/method
        - Add not: bool = False field to all helper classes
        - Return modified instance (maintain immutability)
        - Check element does NOT exist when not=True
        - Error message: "Expected element NOT to exist but found: [element]"
    - [ ] 3.3 Implement .text_content(expected: str) method
        - Return modified instance with expected_text field
        - After finding element, verify text matches using get_text_content
        - Error message: "Expected text: 'X' but got: 'Y'"
        - Works with any query type
    - [ ] 3.4 Implement .with_attribute(name: str, value: str | None) method
        - Return modified instance with attribute_name and attribute_value fields
        - After finding element, check attribute exists
        - If value provided, verify attribute value matches
        - Error message: "Expected attribute 'X'='Y' but got 'Z'" or "attribute not found"
    - [ ] 3.5 Implement .exact() query option method
        - Add exact: bool = False field
        - Pass exact parameter to aria-testing query
        - Return modified instance for chaining
    - [ ] 3.6 Implement .hidden() query option method
        - Add hidden: bool = False field
        - Pass hidden parameter to aria-testing query
        - Return modified instance for chaining
    - [ ] 3.7 Ensure fluent API tests pass
        - Run ONLY the 2-8 tests written in 3.1
        - Verify all modifiers work individually and chained
        - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**

- The 2-8 tests written in 3.1 pass
- All fluent modifiers maintain immutability
- Method chaining works correctly
- Error messages are clear for each modifier
- Type safety maintained throughout

---

### Refactoring and Documentation

#### Task Group 4: Refactor Existing Code and Documentation

**Dependencies:** Task Groups 1-3

- [ ] 4.0 Refactor existing assertions and update documentation
    - [ ] 4.1 Review all existing assertion usage
        - Scan src/storyville/components/ for Story with assertions
        - Scan examples/huge_assertions/ for Story with assertions
        - Scan tests/ for Story with assertions
        - Document current assertion patterns to migrate
    - [ ] 4.2 Refactor src/ component assertions
        - Replace lambda-based assertions with helper classes
        - Update imports to use storyville.assertions
        - Maintain exact same test behavior
        - Files likely to update: footer_test.py, layout_test.py, header_test.py
    - [ ] 4.3 Refactor examples/ story assertions
        - Update examples/huge_assertions/forms/form_button/stories.py
        - Update examples/huge_assertions/forms/form_checkbox/stories.py
        - Update examples/huge_assertions/forms/form_switch/stories.py
        - Replace complex lambda assertions with declarative helpers
        - Do NOT add assertions where none exist
    - [ ] 4.4 Refactor tests/ story assertions
        - Update test Story instances using assertions
        - Replace with helper classes maintaining test coverage
    - [ ] 4.5 Update README.md
        - Add "Assertion Helpers" section
        - Show basic usage examples
        - Demonstrate fluent API (.not, .text_content, .with_attribute)
        - Show all available query helper classes
        - Do NOT include migration guidance from old pattern
    - [ ] 4.6 Run quality checks
        - Run `just lint` to check code style
        - Run `just typecheck` to verify type safety
        - Fix any issues found
    - [ ] 4.7 Run full test suite
        - Run `just test` to verify all tests pass
        - Ensure refactored assertions maintain behavior
        - Verify no regressions introduced
    - [ ] 4.8 Run complete CI checks
        - Run `just ci-checks` to execute full CI pipeline
        - Ensure all quality gates pass
        - Fix any remaining issues

**Acceptance Criteria:**

- All Story assertions in src/, examples/, tests/ use new helpers
- README.md documents the new pattern clearly
- No migration documentation included
- All quality checks pass (lint, typecheck, tests)
- Full CI pipeline passes
- No functionality changes, only API improvements

---

## Execution Order

Recommended implementation sequence:

1. **Foundation First** (Task Group 1)
    - Set up package structure
    - Establish base frozen dataclass pattern
    - Verify module exports work

2. **Core Queries** (Task Group 2)
    - Implement all 7 query helper classes
    - Add detailed error messages
    - Verify query wrapping works correctly

3. **Fluent Enhancements** (Task Group 3)
    - Add .not for negative assertions
    - Add .text_content() for text checks
    - Add .with_attribute() for attribute checks
    - Add .exact() and .hidden() query options
    - Test method chaining

4. **Migration and Quality** (Task Group 4)
    - Refactor all existing assertions
    - Update documentation
    - Run comprehensive quality checks
    - Verify full CI pipeline

---

## Implementation Notes

### Frozen Dataclass Pattern

All helper classes follow this pattern:

```python
from dataclasses import dataclass
from aria_testing import get_by_role
from tdom import Element, Fragment


@dataclass(frozen=True)
class GetByRole:
    role: str
    level: int | None = None
    name: str | None = None
    not_: bool = False
    expected_text: str | None = None
    attribute_name: str | None = None
    attribute_value: str | None = None
    exact: bool = False
    hidden: bool = False

    def __call__(self, container: Element | Fragment) -> None:
        """Execute assertion, raising AssertionError on failure."""
        # Implementation here

    def not(self) -> GetByRole:
        """Return instance with not_=True for negative assertion."""
        return GetByRole(..., not_=True)

    def text_content(self, expected: str) -> GetByRole:
        """Return instance with expected_text set."""
        return GetByRole(..., expected_text=expected)
```

### Error Message Format

Follow aria-testing style:

```
AssertionError: Could not find element with role="button"

Searched in:
<div class="container">
  <span>Text</span>
</div>

Suggestions:
- Check if role is correct
- Verify element is rendered
```

### Query Helper Classes

Implement these 7 classes:

1. GetByRole (role, level, name)
2. GetByText (text)
3. GetByLabelText (label)
4. GetByTestId (test_id)
5. GetByClass (class_name)
6. GetById (id)
7. GetByTagName (tag_name)

### Standards Compliance

- Use Python 3.14+ features (type statement, modern unions)
- Follow frozen dataclass pattern from tests/conftest.py
- Use aria-testing library functions per testing/test-writing.md
- Maintain type safety throughout (ty/basedpyright compliance)
- Single test file per component (no separate integration tests)
- Run quality checks: `just lint`, `just typecheck`, `just ci-checks`
