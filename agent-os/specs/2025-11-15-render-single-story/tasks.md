# Task Breakdown: Render a Single Story

## Overview

Total Task Groups: 5
Focus: Implement type-safe story rendering with View Protocol, update Story class, create StoryView with dual rendering
modes

## Task List

### Foundation: View Protocol

#### Task Group 1: Create View Protocol

**Dependencies:** None

- [x] 1.0 Complete View Protocol foundation
    - [x] 1.1 Write 2-4 focused tests for View Protocol
        - Limit to 2-4 highly focused tests maximum
        - Test protocol satisfaction with a simple test view class
        - Test return type is Node, tests verify Element with type guards
        - Skip exhaustive protocol compliance testing
    - [x] 1.2 Create `src/storytime/models.py` with View Protocol
        - Import: `from typing import Protocol`
        - Import: `from tdom import Node`
        - Define `View` Protocol with `__call__(self) -> Node` signature
        - Add docstring explaining Protocol purpose (type-safe structural typing)
        - Note: Tests use type guards to verify Element, not implementation code
    - [x] 1.3 Ensure View Protocol tests pass
        - Run ONLY the 2-4 tests written in 1.1
        - Verify Protocol can be satisfied by dataclass with `__call__`
        - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**

- The 2-4 tests written in 1.1 pass
- View Protocol properly defines `__call__(self) -> Node`
- Protocol enables structural typing without inheritance
- Tests use type guards (assert isinstance(result, Element)) not implementation code

### Story Package Structure

#### Task Group 2: Restructure Story Module into Package

**Dependencies:** None (can run parallel to Task Group 1)

- [x] 2.0 Complete story package restructure
    - [x] 2.1 Create story package directory
        - Create directory: `src/storytime/story/`
        - Create file: `src/storytime/story/__init__.py`
        - Export Story class: `from storytime.story.models import Story`
    - [x] 2.2 Move Story class to story package
        - Create file: `src/storytime/story/models.py`
        - Move Story class from `src/storytime/story.py` to new file
        - Keep all existing functionality intact
        - Preserve imports and type checking block
    - [x] 2.3 Update imports throughout codebase
        - Update `from storytime.story import Story` references
        - Should continue to work: `from storytime.story import Story`
        - Check files: tests/, src/storytime/
    - [x] 2.4 Remove old story.py file
        - Delete `src/storytime/story.py`
        - Verify no broken imports remain
    - [x] 2.5 Ensure existing Story tests pass
        - Run tests in `tests/story/test_story.py`
        - Verify all Story functionality unchanged
        - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**

- Story package created with proper `__init__.py`
- Story class accessible via `from storytime.story import Story`
- All existing tests in `tests/story/test_story.py` pass
- Old `story.py` file removed

### Story Model Updates

#### Task Group 3: Update Story Class for Element Return Type

**Dependencies:** Task Group 2

- [x] 3.0 Complete Story class modifications
    - [x] 3.1 Write 2-4 focused tests for updated Story.instance property
        - Create tests in `tests/story/test_story_instance.py`
        - Limit to 2-4 highly focused tests maximum
        - Test instance returns Node when component provided
        - Tests use type guard assertions to verify Element
        - Skip testing non-Element components (will fail assertion)
    - [x] 3.2 Remove vdom method from Story class (if exists)
        - Open `src/storytime/story/models.py`
        - Remove `vdom` method entirely (check if it exists first)
        - All rendering should flow through StoryView instead
    - [x] 3.3 Update Story.instance property return type
        - Change return type from `object | None` to `Node | None`
        - Import: `from tdom import Node`
        - NO type guard in implementation - tests do type guards instead
        - Keep existing logic: `self.component(**self.props)`
        - Handle None case when no component exists
    - [x] 3.4 Ensure Story.instance tests pass
        - Run ONLY the 2-4 tests written in 3.1
        - Verify Node return type
        - Verify type guard assertions in tests work
        - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**

- The 2-4 tests written in 3.1 pass
- `vdom` method removed from Story class
- `Story.instance` returns `Node | None`
- Tests use type guards (assert isinstance(result, Element)) not implementation code

### StoryView Implementation

#### Task Group 4: Create StoryView with Dual Rendering Modes

**Dependencies:** Task Groups 1, 2, 3

- [x] 4.0 Complete StoryView implementation
    - [x] 4.1 Write 4-8 focused tests for StoryView rendering
        - Create tests in `tests/story/test_story_view.py`
        - Limit to 4-8 highly focused tests maximum
        - Test custom template mode: story with template uses it
        - Test default layout mode: story without template shows title, props, instance, parent link
        - Test type safety: tests use type guards to verify Element
        - Test one edge case: empty props dict displays correctly
        - Skip exhaustive edge case testing (various prop types, nested structures)
    - [x] 4.2 Create `src/storytime/story/views.py` file
        - Import necessary types: `from dataclasses import dataclass`
        - Import: `from tdom import html, Node`
        - Import: `from storytime.story.models import Story`
    - [x] 4.3 Implement StoryView dataclass structure
        - Decorator: `@dataclass`
        - Field: `story: Story`
        - Method signature: `def __call__(self) -> Node:`
    - [x] 4.4 Implement custom template rendering mode (Mode A)
        - Check: `if self.story.template is not None:`
        - Call template directly: `return self.story.template()`
        - No wrapping elements or additional layout
        - Template has full control over output
    - [x] 4.5 Implement default layout rendering mode (Mode B)
        - Check: `else:` (when template is None)
        - Create tdom template with `html(t"""...""")` syntax
        - Include story title as heading (h1 or h2)
        - Show props: `Props: <code>{str(self.story.props)}</code>`
        - Render component: embed `{self.story.instance}`
        - Add parent link: `<a href="..">Parent</a>`
        - Follow pattern from `src/storytime/views/index_view.py`
    - [x] 4.6 NO type guard in implementation
        - Do NOT add type guards in StoryView.__call__
        - Tests will handle type guard assertions
        - Implementation simply returns Node
    - [x] 4.7 Update `src/storytime/story/__init__.py` exports
        - Add export: `from storytime.story.views import StoryView`
        - Enable: `from storytime.story import Story, StoryView`
    - [x] 4.8 Ensure StoryView tests pass
        - Run ONLY the 4-8 tests written in 4.1
        - Verify both rendering modes work correctly
        - Verify tests use type guards to verify Element
        - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**

- The 4-8 tests written in 4.1 pass
- StoryView implements View Protocol (returns Node)
- Custom template mode (Mode A) works: uses story.template for all rendering
- Default layout mode (Mode B) works: shows title, props, instance, parent link
- Tests use type guards (assert isinstance(result, Element)) not implementation code
- No error handling - exceptions propagate naturally

### Testing & Quality

#### Task Group 5: Test Review & Quality Checks

**Dependencies:** Task Groups 1-4

- [ ] 5.0 Review tests and run quality checks
    - [ ] 5.1 Review tests from Task Groups 1-4
        - Review the 2-4 tests written in Task 1.1 (View Protocol)
        - Review the 2-4 tests written in Task 3.1 (Story.instance)
        - Review the 4-8 tests written in Task 4.1 (StoryView)
        - Total existing tests: approximately 8-16 tests
    - [ ] 5.2 Analyze test coverage gaps for this feature only
        - Identify critical rendering workflows lacking coverage
        - Focus ONLY on gaps related to story rendering
        - Do NOT assess entire application test coverage
        - Prioritize integration between Story and StoryView
    - [ ] 5.3 Write up to 6 additional strategic tests maximum
        - Add maximum of 6 new tests to fill critical gaps
        - Focus on Story + StoryView integration workflows
        - Test aria-testing usage with get_by_tag_name, get_text_content
        - Test edge cases only if business-critical (e.g., None handling)
        - Skip performance tests, exhaustive prop variations, accessibility tests
    - [ ] 5.4 Create test infrastructure if needed
        - `tests/story/` directory already exists with Story-related tests
        - Create `tests/story/test_story_view.py` for StoryView tests
        - Consider fixtures for common test data (sample stories, components)
    - [ ] 5.5 Run feature-specific tests only
        - Run ONLY tests related to this spec's feature
        - Expected total: approximately 14-22 tests maximum
        - Command: `pytest tests/story/`
        - Do NOT run the entire application test suite
    - [ ] 5.6 Run type checking
        - Command: `just typecheck`
        - Verify all type hints pass
        - Verify View Protocol satisfaction
        - Verify Element return types correct
    - [ ] 5.7 Run code formatting
        - Command: `just fmt`
        - Apply consistent code style
        - Verify formatting passes
    - [ ] 5.8 Final verification - run all quality checks
        - Command: `just test` (full test suite)
        - Ensure no regressions in existing tests
        - All checks must pass

**Acceptance Criteria:**

- All feature-specific tests pass (approximately 14-22 tests total)
- No more than 6 additional tests added when filling gaps
- Type checking passes (`just typecheck`)
- Code formatting passes (`just fmt`)
- Full test suite passes (`just test`)
- Critical Story rendering workflows covered

## Execution Order

Recommended implementation sequence:

1. Foundation: View Protocol (Task Group 1) - can run parallel with Task Group 2
2. Story Package Structure (Task Group 2) - can run parallel with Task Group 1
3. Story Model Updates (Task Group 3) - depends on Task Group 2
4. StoryView Implementation (Task Group 4) - depends on Task Groups 1, 2, 3
5. Testing & Quality (Task Group 5) - depends on Task Groups 1-4

## Implementation Notes

### Python Standards

- Use Python 3.14+ features: modern type hints, PEP 604 union syntax (`X | Y`)
- Use Protocol for structural typing (no inheritance required)
- Type guards in tests only: `assert isinstance(result, Element)` in test code, not implementation
- Use tdom t-string templates: `html(t"""...""")` syntax

### Type Safety

- View Protocol enables compile-time checking of view implementations (returns Node)
- Type guards are ONLY in tests, NOT in implementation code
- Tests use `assert isinstance(result, Element)` to verify and narrow types
- Implementation code returns Node, tests verify Element
- All return types must be explicit and verifiable by type checker

### Error Handling

- No special error handling or try/except blocks
- Let exceptions propagate naturally to caller
- Fail-fast principle: missing components, invalid props, template errors should raise immediately

### Testing Strategy

- Use pytest for all tests
- Use aria-testing for HTML verification: `get_by_tag_name`, `get_text_content`
- StoryView returns Element directly - pass to aria-testing functions without parsing
- Focus on behavior testing, not implementation details
- Keep tests fast and isolated

### Quality Checks

After each task group completion:

- Run focused tests for that group only
- Avoid running full test suite until final verification
- Use `just test`, `just typecheck`, `just fmt` for final quality checks

### Code Reuse

- Follow pattern from `src/storytime/views/index_view.py` for StoryView structure
- Reference `tests/story/test_story.py` for test patterns with Story class
- Use dataclass decorator consistently
- Use tdom templates consistently across all views

### Test Organization

- All Story-related tests are organized under `tests/story/` directory
- `tests/story/test_story.py` - Core Story class functionality tests
- `tests/story/test_story_instance.py` - Story.instance property tests
- `tests/story/test_story_view.py` - StoryView rendering tests (to be created)
