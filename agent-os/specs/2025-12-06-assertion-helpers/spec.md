# Specification: Playwright Assertion Helpers

## Goal
Create 16 assertion helper classes using a chained builder API pattern that wrap Playwright's locator methods, providing Testing Library-style assertions with descriptive error messages and implicit waiting for pytest-playwright tests.

## User Stories
- As a test writer, I want clear assertion helpers with descriptive errors so that I can quickly identify DOM issues when tests fail
- As a developer, I want a chained API that mirrors Playwright's fluent interface so that assertions feel natural and discoverable

## Specific Requirements

**16 Assertion Helper Classes**
- Map to Playwright's 8 locator types: role, text, label, placeholder, alt_text, title, test_id, tag_name
- Each type has two variants: `get_by_*` (throws on not found) and `query_by_*` (returns None on not found)
- Each type has list variants: `get_all_by_*` and `query_all_by_*` for multiple elements
- Classes: `GetByRole`, `QueryByRole`, `GetAllByRole`, `QueryAllByRole` (repeat for each type)
- Use chained builder pattern for fluent API
- All classes accept a `page` parameter from pytest-playwright's page fixture

**Chained Assertion Builder API**
- Primary query methods initialize the builder (e.g., `GetByRole(page, role="button")`)
- Builder methods return self for chaining (e.g., `.with_text("Submit")`, `.with_attribute("disabled")`)
- Terminal method executes the query (e.g., `.execute()` or implicitly on assertion)
- Support count assertions for list variants via `expected_count` parameter
- Provide clear error messages that include search criteria and relevant DOM context

**Error Messages with Context**
- Include what was being searched for (role, text, exact match, etc.)
- Show relevant portion of DOM (parent element + children or siblings)
- Format error messages for readability in pytest output
- Highlight query parameters that were used
- Avoid full DOM dumps; focus on relevant context (max 20-30 lines)

**Playwright Locator Options Support**
- Support `exact` parameter for exact text matching
- Support `disabled` parameter for enabled/disabled state filtering
- Support `name` parameter for accessible name matching
- Support `level` parameter for heading level (role="heading")
- Pass through any additional Playwright locator options
- Use modern type hints (Python 3.14+) for IDE autocompletion

**Implicit Waiting Behavior**
- `get_by_*` variants wait for element to appear (raise exception if timeout)
- `query_by_*` variants wait briefly then return None if not found
- Use Playwright's built-in waiting mechanisms (default timeout from page)
- Configurable timeout via optional parameter (default: inherit from page)
- Wait behavior matches Testing Library's assertion style

**Count Assertions for List Queries**
- `GetAllByRole(page, role="button", expected_count=3)` validates exact count
- Parameter is optional; if omitted, no count validation
- Error message shows expected vs actual count
- Error message lists all found elements' basic properties (role, text content)
- Count mismatch should be clear and actionable

**Type Safety and IDE Support**
- Comprehensive type hints using Python 3.14+ syntax
- Use `type` statement for complex type aliases
- Return types should be `Element` for singular queries, `list[Element]` for list queries
- `query_by_*` variants return `Element | None`
- Generic types where appropriate for builder pattern
- Full type coverage for IDE autocompletion

**Integration with pytest-playwright**
- Accept `page` fixture from pytest-playwright as primary parameter
- Work with both sync and async page fixtures (focus on sync first)
- Compatible with pytest-playwright's built-in assertions
- Can be combined with Playwright's `expect` API
- Follow pytest conventions for assertion failures

## Visual Design
No visual assets provided.

## Existing Code to Leverage

**aria-testing library patterns**
- Study existing usage in `tests/test_layout_structure.py` for query patterns
- Functions: `get_by_role`, `get_by_tag_name`, `query_all_by_tag_name`, `get_text_content`
- These work with tdom Elements; new helpers work with Playwright Locators
- Adopt similar naming conventions for consistency
- Follow testing style: descriptive names, clear assertions

**pytest-playwright integration patterns**
- Reference `tests/test_playwright_integration.py` for page fixture usage
- Pattern: `page.locator("selector").click()` and `expect(element).to_have_attribute(...)`
- Note: Tests marked with `@pytest.mark.playwright` to avoid conflicts with anyio tests
- New helpers should work seamlessly with existing Playwright test patterns

**Test fixture factories in conftest.py**
- Factory pattern for creating test helpers (e.g., `mock_tree_node`, `module_factory`)
- Could create assertion helper factory fixture if needed
- Follow established fixture patterns for consistency

**Modern Python standards from CLAUDE.md**
- Use structural pattern matching (`match`/`case`) for complex conditionals
- Use `type` statement for type aliases (e.g., `type ElementLocator = Locator | str`)
- Use PEP 604 union syntax (`X | Y` not `Union[X, Y]`)
- Use built-in generics (`list[str]` not `List[str]`)

**Existing test patterns to replace**
- Search for lambda-based locator patterns in tests: `lambda: page.get_by_role(...)`
- Replace with new assertion helpers: `GetByRole(page, role="button")`
- Look for custom error handling around Playwright locators
- Consolidate into standardized helpers

## Out of Scope
- Advanced assertion helpers for visibility, text content validation, or attribute checking (defer to future iteration)
- Context manager style API (`with AssertionHelper(page) as helper:`)
- Simple function style API (`get_by_role(page, role="button")`)
- Migration automation tools to convert existing tests
- DOM snapshot debugging tools beyond basic error messages in assertions
- Screenshot capture on assertion failure (rely on pytest-playwright's built-in features)
- Async page fixture support (start with sync, add async in future if needed)
- Custom timeout strategies beyond Playwright's default mechanisms
- Integration with other testing frameworks beyond pytest
- Assertion helpers for non-Playwright contexts (e.g., requests/httpx responses)
