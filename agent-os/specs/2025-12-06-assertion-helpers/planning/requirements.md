# Spec Requirements: Assertion Helpers

## Initial Description
16 assertion helpers

## Requirements Discussion

### First Round Questions

**Q1:** I assume you want to create 16 assertion helper functions that wrap playwright-pytest's locator methods (like `get_by_role`, `get_by_text`, etc.) to provide more descriptive test failures. Is that correct?
**Answer:** Yes

**Q2:** I'm thinking these helpers should follow the pattern of Testing Library's assertion style, where each query method has a corresponding assertion that includes implicit waiting and clear error messages. Should we model this after Testing Library's approach?
**Answer:** Yes

**Q3:** Should these 16 helpers map to Playwright's locator methods? For example:
- `get_by_role` / `query_by_role`
- `get_by_text` / `query_by_text`
- `get_by_label` / `query_by_label`
- `get_by_placeholder` / `query_by_placeholder`
- `get_by_alt_text` / `query_by_alt_text`
- `get_by_title` / `query_by_title`
- `get_by_test_id` / `query_by_test_id`
- Plus their `*_all_by_*` variants for multiple elements

Is this the right set of 16?
**Answer:** Yes

**Q4:** I assume these helpers should work with pytest-playwright's `page` fixture. Should they be implemented as standalone functions that take a `page` parameter, or as methods on a helper class/fixture?
**Answer:** Standalone functions that take a `page` parameter

**Q5:** For error messages, should we include:
- What was being searched for (role, text, etc.)
- The full DOM snapshot or a relevant portion?
- Suggestions for similar elements that were found?
**Answer:** What was being searched for and a relevant portion of the DOM

**Q6:** Should these helpers support the same options as Playwright's locator methods (like `exact=True`, `disabled=False`, etc.)?
**Answer:** Yes

**Q7:** For the `get_by_*` variants, should they raise an exception immediately if the element isn't found, while `query_by_*` variants return None? This matches Testing Library's behavior.
**Answer:** Yes

**Q8:** Are there any specific assertion helpers beyond the basic element presence that you want included? For example:
- Element visibility assertions
- Element count assertions (exactly N, at least N, at most N)
- Element text content assertions
- Element attribute assertions

Or should we start with just the presence/absence helpers and add more later?
**Answer:** Start with presence/absence, add more later based on needs

### Existing Code to Reference

**Similar Features Identified:**
In examples, tests, and docs there might be mentions of the older approach. Replace with this new approach.

### Follow-up Questions

**Follow-up 1:** For the API design, which approach would you prefer?
- **Option A**: Simple function style: `get_by_role(page, role="button", name="Submit")`
- **Option B**: Context manager style: `with AssertionHelper(page) as helper: helper.get_by_role(...)`
- **Option C**: Chained assertion builder: `GetByRole(role="button").with_text("Submit").with_attribute("disabled")`
**Answer:** Option C - Chained assertion builder (e.g., `GetByRole(role="button").with_text("Submit").with_attribute("disabled")`)

**Follow-up 2:** For documentation, should we:
- Add comprehensive usage examples to the main README?
- Create a separate docs page for assertion helpers?
- Include minimal usage in README with link to extended docs?
**Answer:** Minimal usage in README, extended usage in a new docs/* page

**Follow-up 3:** You mentioned examples, tests, and docs might have the older approach. Should I:
- Search for and document all locations that need updates?
- Just note that updates may be needed and handle it during implementation?
- Create a migration guide for transitioning from old to new approach?
**Answer:** In examples, tests, and docs there might be mentions of the older approach. Replace with this new approach.

**Follow-up 4:** For count assertions (you mentioned adding more later), when we do add them, should they:
- Be separate functions like `assert_count_by_role(page, role="button", count=3)`?
- Be part of the chained API like `GetByRole(role="button").with_count(3)`?
- Only apply to `*_all_by_*` queries?
**Answer:** Only apply to lists (get_all_by_*, query_all_by_*). Use API like: `GetAllByRole(role="button", expected_count=3)`

## Visual Assets

### Files Provided:
No visual assets provided.

## Requirements Summary

### Functional Requirements
- Create 16 assertion helper functions mapping to Playwright's locator methods:
  - `get_by_role` / `query_by_role`
  - `get_by_text` / `query_by_text`
  - `get_by_label` / `query_by_label`
  - `get_by_placeholder` / `query_by_placeholder`
  - `get_by_alt_text` / `query_by_alt_text`
  - `get_by_title` / `query_by_title`
  - `get_by_test_id` / `query_by_test_id`
  - Plus their `*_all_by_*` variants for multiple elements
- Implement using chained assertion builder pattern (Option C)
- `get_by_*` variants raise exception if element not found
- `query_by_*` variants return None if element not found
- Support same options as Playwright's locator methods (exact, disabled, etc.)
- Provide descriptive error messages including:
  - What was being searched for
  - Relevant portion of the DOM
- Model after Testing Library's assertion style with implicit waiting
- Standalone functions that take a `page` parameter
- Count assertions for list queries: `GetAllByRole(role="button", expected_count=3)`

### Reusability Opportunities
- Replace older approach in existing examples, tests, and documentation
- No specific similar features identified for code reuse
- New pattern to be adopted throughout codebase

### Scope Boundaries

**In Scope:**
- 16 basic presence/absence assertion helpers
- Chained assertion builder API
- Descriptive error messages with DOM context
- Support for Playwright's standard locator options
- Count assertions for `*_all_by_*` queries
- Minimal README documentation with link to extended docs
- Extended documentation in new docs/* page
- Updating examples, tests, and docs to use new approach

**Out of Scope:**
- Advanced assertion helpers (visibility, text content, attributes) - add later based on needs
- Context manager style API
- Simple function style API
- Migration automation tools
- DOM snapshot debugging tools beyond basic error messages

### Technical Considerations
- Must integrate with pytest-playwright's `page` fixture
- Follow Testing Library's assertion patterns
- Use Playwright's built-in waiting mechanisms
- Ensure type hints are comprehensive for IDE support
- Error messages should help developers quickly identify issues
- Chained API should be intuitive and discoverable

### Key Decisions Made
1. **API Style**: Chained assertion builder (Option C) for flexibility and readability
2. **Documentation Strategy**: Minimal in README, comprehensive in separate docs page
3. **Code Migration**: Replace old approach throughout examples, tests, and docs
4. **Count Assertions**: Integrated into list query methods with `expected_count` parameter
5. **Error Handling**: Descriptive messages with search criteria and relevant DOM portion
6. **Scope**: Start with presence/absence, defer advanced assertions to future iterations
