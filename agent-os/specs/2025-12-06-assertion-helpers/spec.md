# Specification: Assertion Helpers

## Goal

Create frozen dataclass-based assertion helpers that wrap aria-testing queries for use in Story.assertions, providing a
fluent API and detailed error messages.

## User Stories

- As a component developer, I want to define assertions declaratively using frozen dataclasses so that my Story
  assertions are readable and reusable
- As a developer writing tests, I want fluent-style assertion modifiers (.not, .text_content, attribute checks) so that
  I can express complex assertions naturally

## Specific Requirements

**Frozen Dataclass with __call__ Pattern**

- Each assertion helper is a frozen dataclass with query parameters stored as fields
- Implement __call__ method that accepts container (Element | Fragment) and raises AssertionError on failure
- Maintain immutability throughout - no state changes after instantiation
- Type-safe parameters matching aria-testing query signatures

**All aria-testing Query Types - Single Element**

- GetByRole (role, level, name parameters)
- GetByText (text parameter)
- GetByLabelText (label parameter)
- GetByTestId (test_id parameter)
- GetByClass (class_name parameter)
- GetById (id parameter)
- GetByTagName (tag_name parameter)
- Each helper class corresponds to one aria-testing get_by_* function

**All aria-testing Query Types - Multiple Elements**

- GetAllByRole (role, level, name parameters)
- GetAllByText (text parameter)
- GetAllByLabelText (label parameter)
- GetAllByTestId (test_id parameter)
- GetAllByClass (class_name parameter)
- GetAllByTagName (tag_name parameter)
- Each helper class corresponds to one aria-testing get_all_by_* function
- Returns list of elements instead of single element

**Fluent API - Negation (.not)**

- Add .not property/method to each helper class for negative assertions
- Returns modified instance that checks element does NOT exist
- Example: GetByRole(role="button").not checks that button does not exist
- Raises AssertionError if element is found when .not is used

**Fluent API - Text Content (.text_content)**

- Add .text_content(expected: str) method for text content verification
- Chains onto query to verify element's text matches expected value
- Works with any query type that returns an element
- Raises AssertionError with clear message showing expected vs actual text

**Fluent API - Attribute Checks**

- Add .with_attribute(name: str, value: str | None) method for attribute verification
- Chains onto query to verify element has specified attribute with optional value
- If value is None, just checks attribute exists
- Raises AssertionError showing what attribute/value was expected vs found

**Fluent API - Query Options**

- Support aria-testing query options (exact, hidden, etc.) in fluent style
- Add .exact() method for exact text matching
- Add .hidden() method to include hidden elements
- Options apply to the underlying aria-testing query call

**Fluent API - Count Assertions (GetAllBy* only)**

- Add .count(expected: int) method for list query helpers
- Verifies the number of elements found matches expected count
- Example: GetAllByRole(role="button").count(3) asserts exactly 3 buttons exist
- Raises AssertionError with clear message showing expected vs actual count
- Only available on GetAllBy* helpers, not GetBy* helpers

**Fluent API - Item Selection (GetAllBy* only)**

- Add .nth(index: int) method to select a specific item from the list
- Returns a modified helper that operates on the selected element
- Example: GetAllByRole(role="button").nth(0).text_content("Submit")
- Enables chaining .text_content(), .with_attribute() on the selected element
- Zero-indexed (0 = first element, 1 = second, etc.)
- Raises AssertionError if index is out of bounds
- Only available on GetAllBy* helpers, not GetBy* helpers

**Module Organization**

- Primary implementation in storyville/assertions/helpers.py
- Export all helper classes from storyville/assertions/__init__.py
- Create storyville/assertions/ directory if it doesn't exist
- Follow existing package structure (see storyville/story/, storyville/subject/)

**Detailed Error Messages**

- Match aria-testing error message style (what searched for, what found, suggestions)
- Include container HTML snippet in error for debugging context
- For .not assertions, show "Expected element NOT to exist but found: [element]"
- For .text_content, show "Expected text: 'X' but got: 'Y'"
- For .with_attribute, show "Expected attribute 'X'='Y' but got 'Z'" or "attribute not found"

**Refactor Existing Story Assertions - Source Files**

- Update all Story instances in src/storyville/components/ that have assertions
- Replace lambda-based assertion functions with new helper classes
- Maintain exact same test behavior - no functionality changes
- Focus on files with aria-testing imports: footer_test.py, layout_test.py, header_test.py, etc.

**Refactor Existing Story Assertions - Examples**

- Update examples/huge_assertions/forms/ story files
- Replace complex lambda assertions with declarative helpers
- Examples: form_checkbox/stories.py, form_button/stories.py, form_switch/stories.py, etc.
- Do NOT add assertions where none exist

**Refactor Existing Story Assertions - Tests**

- Update test Story instances that use assertions
- Review tests/ directory for Story usage with assertion functions
- Replace with helper classes maintaining test coverage

## Existing Code to Leverage

**Story.assertions Pattern (storyville/story/models.py)**

- Story dataclass has assertions field: list[AssertionCallable]
- AssertionCallable type alias: Callable[[Element | Fragment], None]
- Helper classes must match this signature in __call__ method
- assertions field is already used in pytest plugin for test execution

**aria-testing Library Integration (storyville/components/)**

- Current usage: get_by_tag_name, get_by_text, query_all_by_tag_name, get_text_content
- Imports from aria_testing module - reuse same import patterns
- Functions raise ElementNotFoundError, MultipleElementsError - wrap these in AssertionError
- Query functions accept container parameter and return Element

**Frozen Dataclass Pattern (tests/conftest.py)**

- Project uses @dataclass decorator with frozen=True pattern
- Example: @dataclass frozen dataclasses in conftest.py
- Follow same pattern for assertion helper classes
- Enables immutability and type safety

**Lambda Assertion Pattern (examples/huge_assertions/)**

- Current pattern: lambda el: None if condition else throw AssertionError
- Complex, hard to read, not reusable
- New helpers replace this pattern with GetByX(...) instantiation
- Example migration: lambda -> GetByTagName(tag_name="button")

**Fluent API Style (Python ecosystem)**

- Method chaining returns self or modified instance
- Example: GetByRole(role="button").not.text_content("Submit")
- Each method returns callable instance maintaining full type safety

## Out of Scope

- Adding new assertions to Story instances that don't currently have them
- Creating migration documentation or guides (old pattern to new pattern)
- Additional assertion patterns beyond element existence/attributes/count (e.g., event handlers, computed styles)
- Changes to underlying aria-testing library behavior or API
- Modifications to Story class structure or fields
- Support for query_by_* functions (only get_by_* and get_all_by_* which raise on failure)
- Custom error message templates or localization
- Integration with other testing frameworks beyond pytest
- Performance optimization of assertion execution
- Async assertion support
- GetById does not have a GetAllById equivalent (aria-testing limitation)
