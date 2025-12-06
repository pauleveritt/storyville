# Task Breakdown: Section Package Refactoring

## Overview
Total Tasks: 12
Estimated Duration: 2-3 hours

This task breakdown refactors the existing Section class from a single-file module (`src/storyville/section.py`) into a package structure with models.py and views.py, following the established patterns from Subject and Story packages. The Section will gain an optional description field and a SectionView for rendering.

## Task List

### Package Structure Migration

#### Task Group 1: Create Package Structure and Migrate Section Model
**Dependencies:** None

- [x] 1.0 Complete package structure migration
  - [x] 1.1 Write 2-4 focused tests for Section model functionality
    - Test file: `tests/section/test_section_models.py`
    - Test Section initialization with title
    - Test Section with parent (Site)
    - Test Section with description field (present and None)
    - Test Section with items dict[str, Subject]
    - Pattern: Follow `tests/subject/test_subject_models.py` structure
  - [x] 1.2 Create section package directory structure
    - Create directory: `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/section/`
    - Create empty `__init__.py` (will populate after model and view are ready)
  - [x] 1.3 Create Section model in models.py
    - File: `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/section/models.py`
    - Move Section class from `src/storyville/section.py`
    - Add `description: str | None = None` field
    - Keep existing: `parent: Site | None = None`
    - Keep existing: `items: dict[str, Subject] = field(default_factory=dict)`
    - Inherit from `BaseNode["Section"]` (already done in existing code)
    - Do NOT override `post_update()` method
    - Use TYPE_CHECKING import guard for Site and Subject
    - Add class docstring explaining Section's organizational role
  - [x] 1.4 Run focused model tests
    - Command: `pytest tests/section/test_section_models.py -v`
    - Verify all 2-4 model tests pass
    - Do NOT run full test suite yet

**Acceptance Criteria:**
- Section package directory exists with models.py
- Section model has all required fields including new description field
- The 2-4 model tests in test_section_models.py pass
- Section inherits from BaseNode without overriding post_update()

### View Implementation

#### Task Group 2: Implement SectionView Rendering
**Dependencies:** Task Group 1

- [x] 2.0 Complete SectionView implementation
  - [x] 2.1 Write 2-4 focused tests for SectionView rendering
    - Test file: `tests/section/test_section_views.py`
    - Test SectionView renders title in h1
    - Test SectionView renders description when present
    - Test SectionView renders Subject cards (iterate over items.values())
    - Test SectionView shows empty state when items dict is empty
    - Test SectionView includes parent link
    - Pattern: Follow `tests/subject/test_subject_views.py` structure
    - Use aria-testing utilities: `get_by_tag_name`, `get_text_content`, `query_all_by_tag_name`
    - Use type guard: `assert isinstance(result, Element)` in tests
  - [x] 2.2 Create SectionView in views.py
    - File: `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/section/views.py`
    - Create dataclass with `section: Section` field
    - Implement `__call__(self) -> Node` method (View Protocol)
    - Use tdom `html(t"""...""")` template syntax
    - Render title as `<h1>{self.section.title}</h1>`
    - Conditionally render description: `{self.section.description}` in `<p>` when not None
    - Iterate over `self.section.items.values()` to create Subject cards
    - Each Subject: `<li><a href="{subject_url}">{subject.title}</a></li>` in `<ul>`
    - Use URL pattern: `subject-{idx}` or key-based from dict
    - Empty state: Show "No subjects defined for this section" when items is empty
    - Include parent link: `<a href="..">Parent</a>`
    - Pattern: Follow SubjectView structure from `src/storyville/subject/views.py`
    - Add docstring explaining rendering behavior
  - [x] 2.3 Run focused view tests
    - Command: `pytest tests/section/test_section_views.py -v`
    - Verify all 2-4 view tests pass
    - Do NOT run full test suite yet

**Acceptance Criteria:**
- SectionView renders all required elements (title, description, Subject cards, parent link)
- The 2-4 view tests in test_section_views.py pass
- Empty state displays correctly when no Subjects
- Conditional description rendering works

### Integration and Cleanup

#### Task Group 3: Package Exports and Import Updates
**Dependencies:** Task Groups 1, 2

- [x] 3.0 Complete package integration
  - [x] 3.1 Create package exports in __init__.py
    - File: `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/section/__init__.py`
    - Export Section from models
    - Export SectionView from views
    - Pattern: Follow `src/storyville/subject/__init__.py` structure
    - Add `__all__ = ["Section", "SectionView"]`
  - [x] 3.2 Update imports in dependent files
    - Update `src/storyville/site.py` if needed
    - Change from `from storyville.section import Section`
    - To: `from storyville.section.models import Section` (or use package import)
    - Verify Site.items dict[str, Section] continues working
    - Check make_site() function compatibility
  - [x] 3.3 Remove old section.py file
    - Delete: `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/section.py`
    - Only after verifying package structure works
  - [x] 3.4 Run section-specific tests
    - Command: `pytest tests/section/ -v`
    - Verify all Section tests pass (approximately 6-8 tests total)
    - Do NOT run full test suite yet

**Acceptance Criteria:**
- Package __init__.py exports Section and SectionView
- Site imports work correctly with new package structure
- Old section.py file is removed
- All section-specific tests pass

### Quality Assurance

#### Task Group 4: Quality Checks and Full Test Suite
**Dependencies:** Task Groups 1, 2, 3

- [x] 4.0 Complete quality assurance
  - [x] 4.1 Run full test suite
    - Command: `just test`
    - Verify all existing tests continue to pass
    - Verify Section model tests pass
    - Verify SectionView rendering tests pass
    - Total Section tests: approximately 6-8 tests
  - [x] 4.2 Run type checking
    - Command: `just typecheck`
    - Verify no type errors introduced
    - Verify Section model type hints are correct
    - Verify SectionView return type is Node
    - Verify TYPE_CHECKING imports work correctly
  - [x] 4.3 Run code formatting
    - Command: `just fmt`
    - Ensure all new files follow project code style
    - Verify formatting of models.py and views.py
    - Verify formatting of test files
  - [x] 4.4 Verify integration with existing features
    - Manually verify Site → Section → Subject → Story hierarchy
    - Check that make_site() continues to work
    - Verify Section.items dict operations
    - Confirm no regression in Subject or Story features

**Acceptance Criteria:**
- All quality checks pass (test, typecheck, fmt)
- No regressions in existing functionality
- Section package integrates seamlessly with Site, Subject, and Story
- Total Section tests: approximately 6-8 focused tests covering critical functionality

## Execution Order

Recommended implementation sequence:
1. **Package Structure Migration** (Task Group 1)
   - Create directory structure
   - Write model tests first
   - Implement Section model with description field
   - Run focused model tests

2. **View Implementation** (Task Group 2)
   - Write view tests first
   - Implement SectionView with rendering logic
   - Run focused view tests

3. **Integration and Cleanup** (Task Group 3)
   - Create package exports
   - Update dependent imports
   - Remove old single-file module
   - Run section-specific tests

4. **Quality Assurance** (Task Group 4)
   - Run full test suite
   - Run type checking
   - Run formatting
   - Verify integration

## Important Notes

### Testing Strategy
- Each task group writes 2-4 focused tests FIRST (test-driven development)
- Run focused tests during development (e.g., `pytest tests/section/test_section_models.py`)
- Run full test suite only at the end (`just test`)
- Total expected tests: approximately 6-8 focused tests covering critical Section functionality

### Code Patterns to Follow
- **Subject package structure**: Use as primary reference for package organization
- **SubjectView rendering**: Follow same pattern for view implementation
- **BaseNode inheritance**: Section inherits without overriding post_update()
- **Type guards**: Use `assert isinstance()` in tests, not in implementation
- **Modern Python**: Use PEP 604 union syntax (`X | None`), built-in generics (`dict[str, Subject]`)

### Key Files
- Existing: `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/section.py` (to migrate)
- New: `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/section/models.py`
- New: `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/section/views.py`
- New: `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/section/__init__.py`
- New: `/Users/pauleveritt/projects/t-strings/storyville/tests/section/test_section_models.py`
- New: `/Users/pauleveritt/projects/t-strings/storyville/tests/section/test_section_views.py`

### Technical Constraints
- Section.items remains `dict[str, Subject]` (do NOT convert to list)
- Section does NOT override `post_update()` method
- Description field is optional: `description: str | None = None`
- SectionView satisfies View Protocol by implementing `__call__() -> Node`
- Use TYPE_CHECKING import guard for circular imports (Site, Subject)

### Quality Standards
All quality checks from CLAUDE.md must pass:
- Tests: `just test`
- Type checking: `just typecheck`
- Formatting: `just fmt`
