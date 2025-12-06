# Spec Requirements: Assertion Helpers

## Initial Description
Next roadmap item on assertion helpers

## Roadmap Item (Item 16)
Assertion helpers — Make dataclass variations of aria-testing queries that can be used in `Story.assertions`. For example `GetByRole` would be passed a `role`. Later, the instance would be passed a `container` and would raise `AssertionError` if not passing. Refactor all `Story` in `src` `examples` `tests` that have assertion functions to instead use these helpers, where appropriate. Update README and docs.

Size: M (Medium)

## Requirements Discussion

### First Round Questions

**Q1: Query Type Coverage** - Should we implement assertion helpers for all aria-testing query types (GetByRole, GetByText, GetByLabelText, etc.), or focus on a subset initially?
**Answer:** All aria-testing query types

**Q2: Implementation Pattern** - I'm assuming these will be frozen dataclasses with a `__call__` method that takes the container and raises AssertionError. Is that the pattern you want?
**Answer:** Yes - frozen dataclass with __call__ method

**Q3: API Usage** - Should the helpers support both positive assertions (element exists) and negative assertions (element doesn't exist)? For example, `GetByRole(..., should_exist=False)` or a separate `NotGetByRole` class?
**Answer:** Include `not` in a fluent style. Include other fluent additions: `text_content`, an attribute check, etc.

**Q4: Module Organization** - I assume these will live in `storyville/assertions/helpers.py` and be exported from `storyville/assertions/__init__.py`. Is that correct?
**Answer:** Yes - storyville/assertions/helpers.py exported from __init__.py

**Q5: Error Messages** - Should error messages follow the aria-testing library's style (showing what was searched for, what was found, suggesting alternatives)?
**Answer:** Yes - detailed aria-testing-style error messages

**Q6: Refactoring Scope** - For the refactoring phase, should we update all Story instances in src/, examples/, and tests/ that currently use assertion functions?
**Answer:** Yes (but don't add assertions where they aren't already present)

**Q7: Query Options** - Should the helpers support all the query options that aria-testing provides (like exact=True, hidden=True, etc.)?
**Answer:** Yes, as fluent style

**Q8: Documentation** - Should the docs show migration examples (old assertion functions → new helpers) or just document the new pattern?
**Answer:** Just show the new pattern (no migration guidance)

**Q9: Additional Patterns** - Are there any other assertion patterns beyond "element exists/doesn't exist" we should support? For example, "element has text", "element has attribute", etc.?
**Answer:** No additional patterns needed

**Q10: Explicit Exclusions** - Are there any specific Story instances or test files that should NOT be refactored to use the new helpers?
**Answer:** No exclusions

**Q11: Existing Code Reuse** - Are there existing features in your codebase with similar patterns we should reference?
**Answer:** No existing code to reference

### Existing Code to Reference

No similar existing features identified for reference.

### Follow-up Questions

None required - all answers were clear and complete.

## Visual Assets

### Files Provided:
No visual assets provided.

### Visual Insights:
Not applicable.

## Requirements Summary

### Functional Requirements

**Core Functionality:**
- Create frozen dataclass variations of all aria-testing query types
- Each helper class is instantiated with query parameters (role, text, label, etc.)
- Instance has a `__call__` method that accepts a container and raises AssertionError if query fails
- Support fluent-style API including:
  - `.not` - for negative assertions (element should not exist)
  - `.text_content` - for text content assertions
  - Attribute checks - for verifying element attributes
- Support all aria-testing query options in fluent style (exact, hidden, etc.)
- Generate detailed, aria-testing-style error messages with:
  - What was searched for
  - What was found
  - Suggestions for alternatives

**Query Types to Implement:**
- GetByRole
- GetByText
- GetByLabelText
- GetByPlaceholderText
- GetByAltText
- GetByTitle
- GetByDisplayValue
- GetByTestId
- (All other aria-testing query types)

**Refactoring Requirements:**
- Update all Story instances in:
  - src/
  - examples/
  - tests/
- Replace assertion functions with new helpers where assertions already exist
- Do NOT add new assertions where they weren't present before
- Maintain existing test coverage and behavior

**Documentation Requirements:**
- Document the new assertion helper pattern
- Show usage examples with the fluent API
- Do NOT include migration guidance from old to new pattern
- Update README with assertion helpers section

### Reusability Opportunities

No existing similar features identified for code reuse. This is a new pattern being introduced to the codebase.

### Scope Boundaries

**In Scope:**
- Implementation of all assertion helper classes as frozen dataclasses
- Fluent API support (.not, .text_content, attribute checks)
- Fluent-style query options (exact, hidden, etc.)
- Aria-testing-style error messages
- Refactoring existing Story assertions in src/, examples/, and tests/
- Documentation showing the new pattern
- README updates

**Out of Scope:**
- Adding new assertions where they don't currently exist
- Migration guidance documentation (old → new pattern)
- Additional assertion patterns beyond element existence/non-existence
- Changes to the underlying aria-testing query behavior
- Modifications to Story class structure

### Technical Considerations

**Implementation Approach:**
- Use frozen dataclasses for immutability and safety
- Implement `__call__` method for container-based assertions
- Use fluent API pattern for modifiers (.not, .text_content, etc.)
- Integrate with aria-testing library for query execution
- Maintain type safety throughout

**Module Organization:**
- Primary implementation: `storyville/assertions/helpers.py`
- Export from: `storyville/assertions/__init__.py`
- Refactor existing files in src/, examples/, and tests/ directories

**Error Handling:**
- Raise AssertionError on query failures
- Provide detailed error messages matching aria-testing style
- Include search criteria, results found, and suggestions

**Testing:**
- Verify all query types work correctly
- Test positive and negative assertions (.not)
- Test fluent API modifiers
- Test query options in fluent style
- Verify error message quality
- Ensure refactored tests maintain coverage
