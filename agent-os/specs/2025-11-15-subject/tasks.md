# Task Breakdown: Subject Package Implementation

## Overview

Total Tasks: 4 task groups with 15 sub-tasks
Estimated Complexity: Medium
Pattern: Follow Story package structure (models.py, views.py, __init__.py)

## Task List

### Task Group 1: Package Structure and Models

**Dependencies:** None

- [ ] 1.0 Refactor Subject to package structure
  - [ ] 1.1 Write 2-4 focused tests for Subject model functionality
    - Location: `/Users/pauleveritt/projects/pauleveritt/storytime/tests/subject/test_subject_models.py`
    - Tests to write:
      - `test_subject_initialization()` - Basic instantiation
      - `test_subject_with_parent()` - Parent relationship
      - `test_subject_with_target()` - Target attribute
      - `test_subject_with_stories()` - Stories list
    - Migrate existing tests from `/Users/pauleveritt/projects/pauleveritt/storytime/tests/test_subject.py`
    - Pattern: Use real instances, not mocks (follow `tests/story/test_story_models.py`)
  - [ ] 1.2 Create package directory structure
    - Create directory: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/subject/`
    - Create empty file: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/subject/__init__.py`
  - [ ] 1.3 Move Subject class to models.py
    - Move `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/subject.py` to `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/subject/models.py`
    - Keep all existing attributes: parent, target, stories, title, package_path (from BaseNode)
    - Maintain BaseNode["Subject"] inheritance
    - Keep Target type import from storytime.models
    - Update TYPE_CHECKING imports: Section, Story
  - [ ] 1.4 Create __init__.py exports
    - File: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/subject/__init__.py`
    - Export: `from storytime.subject.models import Subject`
    - Export: `__all__ = ["Subject", "SubjectView"]` (SubjectView added in Task Group 2)
    - Pattern: Follow `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/story/__init__.py`
  - [ ] 1.5 Update all imports throughout codebase
    - Find files importing `from storytime.subject import Subject`
    - Keep imports as `from storytime.subject import Subject` (package __init__.py handles this)
    - Verify no direct imports of `storytime.subject` module exist
    - Command: `grep -r "from storytime.subject import" /Users/pauleveritt/projects/pauleveritt/storytime/src/`
  - [ ] 1.6 Create tests directory structure
    - Create directory: `/Users/pauleveritt/projects/pauleveritt/storytime/tests/subject/`
    - Create empty file: `/Users/pauleveritt/projects/pauleveritt/storytime/tests/subject/__init__.py`
    - Delete old test file: `/Users/pauleveritt/projects/pauleveritt/storytime/tests/test_subject.py`
  - [ ] 1.7 Run focused tests for models only
    - Command: `pytest /Users/pauleveritt/projects/pauleveritt/storytime/tests/subject/test_subject_models.py -v`
    - Verify: 2-4 tests written in 1.1 pass
    - Do NOT run full test suite yet

**Acceptance Criteria:**
- Subject class moved to `src/storytime/subject/models.py`
- Package exports Subject from `__init__.py`
- All existing Subject attributes preserved
- 2-4 focused model tests pass
- Imports throughout codebase work correctly

### Task Group 2: SubjectView Implementation

**Dependencies:** Task Group 1

- [ ] 2.0 Create SubjectView for rendering subjects
  - [ ] 2.1 Write 2-4 focused tests for SubjectView functionality
    - Location: `/Users/pauleveritt/projects/pauleveritt/storytime/tests/subject/test_subject_views.py`
    - Tests to write:
      - `test_subject_view_renders_title_in_h1()` - Title rendering
      - `test_subject_view_renders_story_cards()` - Story list with links
      - `test_subject_view_shows_empty_state()` - Empty state message
      - `test_subject_view_returns_element_type()` - Type verification with isinstance guard
    - Use aria_testing helpers: `get_by_tag_name`, `get_text_content`, `query_all_by_tag_name`
    - Pattern: Follow `/Users/pauleveritt/projects/pauleveritt/storytime/tests/story/test_story_views.py`
    - Type guards: `assert isinstance(result, Element)` in tests only
  - [ ] 2.2 Create SubjectView class
    - File: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/subject/views.py`
    - Class structure:
      ```python
      @dataclass
      class SubjectView:
          subject: Subject

          def __call__(self) -> Node:
              # Render subject metadata and stories
      ```
    - Pattern: Follow `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/story/views.py`
    - Satisfies View Protocol from `storytime.models`
  - [ ] 2.3 Implement subject metadata rendering
    - Render title in h1 element: `<h1>{self.subject.title}</h1>`
    - Display target info if present: `<p>Target: {self.subject.target.__name__ if self.subject.target else "None"}</p>`
    - Include parent navigation: `<a href="..">Parent</a>`
    - Use tdom html() with t-string template
  - [ ] 2.4 Implement story cards rendering
    - Check if stories list is empty: `if not self.subject.stories:`
    - Empty state: `<p>No stories defined for this component</p>`
    - Non-empty: Render as ul/li structure
    - Each card: `<li><a href="{story_url}">{story.title}</a></li>`
    - Do NOT use StoryView for individual stories
    - Do NOT render story.instance or call story components
    - Keep cards minimal: title and link only
  - [ ] 2.5 Update __init__.py to export SubjectView
    - File: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/subject/__init__.py`
    - Add: `from storytime.subject.views import SubjectView`
    - Update __all__: `__all__ = ["Subject", "SubjectView"]`
  - [ ] 2.6 Run focused tests for views only
    - Command: `pytest /Users/pauleveritt/projects/pauleveritt/storytime/tests/subject/test_subject_views.py -v`
    - Verify: 2-4 tests written in 2.1 pass
    - Do NOT run full test suite yet

**Acceptance Criteria:**
- SubjectView class created in `src/storytime/subject/views.py`
- SubjectView satisfies View Protocol (__call__ returns Node)
- Renders subject title, target info, parent link
- Renders story cards as simple list with links
- Shows empty state message when no stories
- 2-4 focused view tests pass
- SubjectView exported from package __init__.py

### Task Group 3: Story.post_update() Verification

**Dependencies:** Task Groups 1, 2

- [ ] 3.0 Verify Story.post_update() compatibility with Subject.target
  - [ ] 3.1 Write 2 focused integration tests
    - Location: `/Users/pauleveritt/projects/pauleveritt/storytime/tests/subject/test_subject_integration.py`
    - Tests to write:
      - `test_story_inherits_target_from_subject()` - Story gets Subject.target when Story.target is None
      - `test_subject_view_with_stories_having_inherited_target()` - SubjectView renders stories that inherited target
    - Use real Subject and Story instances
    - Verify Story.post_update() works without modification
  - [ ] 3.2 Verify Story.post_update() uses self.parent.target
    - Review: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/story/models.py`
    - Line 39: `if self.target is None and self.parent.target:`
    - Confirm: Already uses self.parent.target (correct after terminology change)
    - No changes needed to Story class
  - [ ] 3.3 Test Subject properly exposes target attribute
    - Create test Subject with target attribute set
    - Create test Story with target=None
    - Call story.post_update(subject)
    - Verify: story.target is subject.target
    - Pattern: Similar to existing test in `tests/story/test_story_models.py`
  - [ ] 3.4 Run focused integration tests
    - Command: `pytest /Users/pauleveritt/projects/pauleveritt/storytime/tests/subject/test_subject_integration.py -v`
    - Verify: 2 integration tests pass
    - Do NOT run full test suite yet

**Acceptance Criteria:**
- Story.post_update() works with Subject.target without modification
- Story inherits parent.target when story.target is None
- Subject properly exposes target attribute to child stories
- 2 focused integration tests pass

### Task Group 4: Quality Checks and Full Test Suite

**Dependencies:** Task Groups 1, 2, 3

- [ ] 4.0 Run comprehensive quality checks
  - [ ] 4.1 Run all Subject-related tests
    - Command: `pytest /Users/pauleveritt/projects/pauleveritt/storytime/tests/subject/ -v`
    - Expected: All tests pass (approximately 8-10 tests total from groups 1-3)
    - Tests should cover: models, views, integration
  - [ ] 4.2 Run full test suite
    - Command: `just test`
    - Verify: All tests pass across entire codebase
    - Ensure: No regressions from refactoring
  - [ ] 4.3 Run type checking
    - Command: `just typecheck`
    - Verify: No type errors in Subject package
    - Check: Subject, SubjectView, imports all type-safe
    - Ensure: Python 3.14+ type hints used (X | Y syntax, modern generics)
  - [ ] 4.4 Run code formatting
    - Command: `just fmt`
    - Verify: All code properly formatted
    - Check: Subject package follows project style

**Acceptance Criteria:**
- All Subject tests pass (8-10 tests total)
- Full test suite passes (`just test`)
- Type checking passes (`just typecheck`)
- Code formatting passes (`just fmt`)
- No regressions introduced

## Execution Order

Recommended implementation sequence:

1. **Task Group 1**: Package Structure and Models
   - Establish package structure
   - Move Subject to models.py
   - Set up exports and imports
   - Verify with focused model tests

2. **Task Group 2**: SubjectView Implementation
   - Create SubjectView class
   - Implement rendering logic
   - Handle empty state
   - Verify with focused view tests

3. **Task Group 3**: Story.post_update() Verification
   - Verify inheritance behavior
   - Test integration between Subject and Story
   - Confirm no Story changes needed

4. **Task Group 4**: Quality Checks and Full Test Suite
   - Run all Subject tests
   - Run full test suite
   - Run type checking
   - Run code formatting

## Key Technical Decisions

**Package Structure:**
- Follow exact pattern from Story package
- models.py for data (Subject class)
- views.py for rendering (SubjectView class)
- __init__.py for exports

**Type Safety:**
- Use Python 3.14+ modern type hints (X | Y syntax)
- Use built-in generics (list[Story] not List[Story])
- Type guards (isinstance) only in tests, not implementation
- Subject already uses Target type alias from storytime.models

**Testing Approach:**
- Write 2-4 focused tests per task group (8-10 tests total)
- Use aria_testing helpers for DOM verification
- Test with real instances, not mocks
- Run focused tests during development, full suite at end

**Story Cards Rendering:**
- Simple ul/li structure with links
- Title and link only, no additional metadata
- Do NOT use StoryView for individual stories
- Do NOT render story.instance
- Empty state: "No stories defined for this component"

**Compatibility:**
- Subject.target already exists (no changes needed)
- Story.post_update() already uses self.parent.target (correct)
- No changes to Story class required
- Maintain backward compatibility where possible

## Files Modified/Created

**Created:**
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/subject/models.py` (moved from subject.py)
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/subject/views.py` (new)
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/subject/__init__.py` (new)
- `/Users/pauleveritt/projects/pauleveritt/storytime/tests/subject/test_subject_models.py` (moved from test_subject.py)
- `/Users/pauleveritt/projects/pauleveritt/storytime/tests/subject/test_subject_views.py` (new)
- `/Users/pauleveritt/projects/pauleveritt/storytime/tests/subject/test_subject_integration.py` (new)
- `/Users/pauleveritt/projects/pauleveritt/storytime/tests/subject/__init__.py` (new, empty)

**Deleted:**
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/subject.py` (moved to subject/models.py)
- `/Users/pauleveritt/projects/pauleveritt/storytime/tests/test_subject.py` (moved to tests/subject/)

**Modified:**
- Any files importing `from storytime.subject import Subject` (verify imports still work via package __init__.py)

## Notes

- All file paths are absolute as required
- Tests use type guards (assert isinstance) following project patterns
- SubjectView returns Node, tests verify Element type
- Story.post_update() requires no changes (already uses self.parent.target)
- Follow CLAUDE.md quality standards: `just test`, `just typecheck`, `just fmt`
