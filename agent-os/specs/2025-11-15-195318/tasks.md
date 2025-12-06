# Task Breakdown: Site Package Refactoring

## Overview
Total Tasks: 4 major task groups
This refactoring extracts Site into its own package following the existing pattern (story/, section/, subject/), and standardizes all node types to use `.items` for child collections.

## Task List

### Package Structure

#### Task Group 1: Create Site Package Structure
**Dependencies:** None

- [x] 1.0 Create site package structure
  - [x] 1.1 Write 2-8 focused tests for Site model functionality
    - Test Site instantiation with BaseNode["Site"] inheritance
    - Test Site.items dict field (dict[str, Section])
    - Test Site.post_update() method (parent assignment, name, package_path, title logic)
    - Test Site.__post_init__() static directory detection
    - Test Site has no parent (parent is None)
    - Limit to 2-8 highly focused tests maximum
    - Reuse pattern from: `/Users/pauleveritt/projects/t-strings/storyville/tests/section/test_section_models.py`
  - [x] 1.2 Create directory structure
    - Create `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/site/` directory
    - Create empty `__init__.py`
    - Create empty `models.py`
    - Create empty `views.py`
    - Create empty `helpers.py`
  - [x] 1.3 Implement Site model in models.py
    - Move Site class from `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/site.py` to `site/models.py`
    - Change from standalone dataclass to inherit from `BaseNode["Site"]`
    - Keep fields: `name`, `parent: None`, `title`, `context`, `package_path`, `items: dict[str, Section]`, `static_dir: Path | None`
    - Keep `__post_init__()` method for static directory detection
    - Implement `post_update()` method (override BaseNode implementation)
    - Remove `find_path()` method (will become standalone helper)
    - Add TYPE_CHECKING imports for Section
    - Follow exact pattern from: `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/section/models.py`
  - [x] 1.4 Export Site from __init__.py
    - Add: `from storyville.site.models import Site`
    - Create `__all__ = ["Site"]` list (will add more exports later)
    - Follow pattern from: `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/section/__init__.py`
  - [x] 1.5 Ensure Site model tests pass
    - Run ONLY the 2-8 tests written in 1.1
    - Verify Site inherits from BaseNode correctly
    - Verify static_dir detection works
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 1.1 pass
- Site package structure matches section/ package pattern
- Site inherits from BaseNode["Site"]
- Site model functionality preserved from original implementation
- Type checking passes (`just typecheck`)

### View Layer

#### Task Group 2: Implement SiteView
**Dependencies:** Task Group 1

- [x] 2.0 Implement SiteView class
  - [x] 2.1 Write 2-8 focused tests for SiteView
    - Test SiteView renders site title in h1
    - Test SiteView lists sections as links when sections exist
    - Test SiteView shows empty state when no sections
    - Test SiteView does NOT include parent link (Site is root)
    - Test SiteView satisfies View Protocol (__call__() -> Node)
    - Limit to 2-8 highly focused tests maximum
    - Reuse pattern from: `/Users/pauleveritt/projects/t-strings/storyville/tests/section/test_section_views.py`
  - [x] 2.2 Create SiteView class in views.py
    - Create dataclass with `site: Site` field
    - Implement `__call__(self) -> Node` method
    - Render site title in h1
    - Render list of sections as links (use section.title and key for URL)
    - Render empty state message if no sections: "No sections defined for this site"
    - Do NOT include parent link (Site has no parent)
    - Use tdom html() with t-strings for template interpolation
    - Follow exact pattern from: `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/section/views.py`
  - [x] 2.3 Export SiteView from __init__.py
    - Add: `from storyville.site.views import SiteView`
    - Update `__all__` to include "SiteView"
  - [x] 2.4 Ensure SiteView tests pass
    - Run ONLY the 2-8 tests written in 2.1
    - Verify rendering with sections works
    - Verify empty state works
    - Verify no parent link is rendered
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 2.1 pass
- SiteView renders correctly with tdom
- SiteView follows same pattern as SectionView and SubjectView
- No parent link in rendered output
- Type checking passes (`just typecheck`)

### Helper Functions

#### Task Group 3: Extract Helper Functions
**Dependencies:** Task Group 1, Task Group 2

- [x] 3.0 Extract and test helper functions
  - [x] 3.1 Write 2-8 focused tests for helpers
    - Test make_site() creates populated Site with sections and subjects
    - Test make_site() handles parent/child relationships correctly
    - Test find_path() finds Site (root ".")
    - Test find_path() finds Section (".section_name")
    - Test find_path() finds Subject (".section.subject")
    - Test find_path() returns None for nonexistent paths
    - Limit to 2-8 highly focused tests maximum
    - Reuse assertions from: `/Users/pauleveritt/projects/t-strings/storyville/tests/test_site.py`
  - [x] 3.2 Extract make_site() to helpers.py
    - Move make_site() function from `site.py` (lines 75-136) to `site/helpers.py`
    - Signature: `def make_site(package_location: str) -> Site`
    - Preserve exact logic and behavior
    - Update imports within helpers.py (TreeNode, Section, Subject)
    - Use relative imports: `from storyville.site.models import Site`
  - [x] 3.3 Extract find_path() to helpers.py
    - Convert Site.find_path() method to standalone function
    - Signature: `def find_path(site: Site, path: str) -> Site | Section | Subject | Story | None`
    - Move logic from `site.py` lines 64-72
    - Preserve exact traversal logic
    - Add TYPE_CHECKING imports for return types
  - [x] 3.4 Export helpers from __init__.py
    - Add: `from storyville.site.helpers import make_site, find_path`
    - Update `__all__` to: `["Site", "SiteView", "make_site", "find_path"]`
  - [x] 3.5 Ensure helper tests pass
    - Run ONLY the 2-8 tests written in 3.1
    - Verify make_site() builds complete tree
    - Verify find_path() traverses correctly
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 3.1 pass
- make_site() function works as standalone helper
- find_path() function works as standalone helper
- All exports available from `storyville.site` package
- Type checking passes (`just typecheck`)

### Consistency Refactoring

#### Task Group 4: Refactor Subject.stories → Subject.items
**Dependencies:** Task Group 3 (so helpers.py uses .items)

- [x] 4.0 Standardize to .items naming convention
  - [x] 4.1 Write 2-8 focused tests for Subject.items
    - Test Subject.items field is list[Story]
    - Test Subject.items defaults to empty list
    - Test Subject.items can be populated with Story instances
    - Test SubjectView renders Subject.items correctly
    - Limit to 2-8 highly focused tests maximum
    - Update assertions from: `/Users/pauleveritt/projects/t-strings/storyville/tests/subject/test_subject_models.py`
  - [x] 4.2 Update Subject model
    - In `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/subject/models.py`
    - Change field from `stories: list[Story]` to `items: list[Story]`
    - Line 20: `stories: list[Story]` → `items: list[Story]`
  - [x] 4.3 Update SubjectView references
    - In `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/subject/views.py`
    - Line 38: Change `if not self.subject.stories:` → `if not self.subject.items:`
    - Line 49: Change `for idx, story in enumerate(self.subject.stories):` → `for idx, story in enumerate(self.subject.items):`
  - [x] 4.4 Update site/helpers.py reference
    - In `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/site/helpers.py`
    - Find line with `for story in subject.stories:` (around line 73)
    - Change to: `for story in subject.items:`
  - [x] 4.5 Update stories.py reference
    - In `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/stories.py`
    - Line 18: Change `story = subject.stories[0]` → `story = subject.items[0]`
  - [x] 4.6 Update all test files
    - Update `/Users/pauleveritt/projects/t-strings/storyville/tests/subject/test_subject_models.py`
      - Change all `subject.stories` references to `subject.items`
      - Lines to update: assertions checking `.stories` field
    - Update `/Users/pauleveritt/projects/t-strings/storyville/tests/subject/test_subject_views.py`
      - Change `subject.stories = [story1, story2]` → `subject.items = [story1, story2]`
    - Update `/Users/pauleveritt/projects/t-strings/storyville/tests/test_site.py`
      - Line 102: Change `stories = heading.stories` → `stories = heading.items`
      - Line 103: Keep reference to `stories` variable (no change)
    - Update `/Users/pauleveritt/projects/t-strings/storyville/examples/minimal/components/heading/stories.py`
      - Change `stories=[Story()]` → `items=[Story()]`
    - Update `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/components/index/stories.py`
      - Change `stories=[...]` → `items=[...]`
    - Update `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/components/component_view/stories.py`
      - Change `stories=[...]` → `items=[...]`
    - Update `/Users/pauleveritt/projects/t-strings/storyville/examples/minimal/stories.py`
      - Change `subject.stories[0]` → `subject.items[0]`
    - Update `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/site.py` (old file, to be deleted in Task 5)
      - Change `subject.stories` → `subject.items` for consistency during transition
  - [x] 4.7 Ensure Subject.items tests pass
    - Run ONLY the tests written in 4.1 and updated Subject-related tests
    - Verify Subject.items field works correctly
    - Verify SubjectView renders items correctly
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 4.1 pass
- All Subject.stories references updated to Subject.items
- All node types now use .items consistently (Site.items, Section.items, Subject.items)
- Views render correctly with .items
- Type checking passes (`just typecheck`)

### Final Integration

#### Task Group 5: Clean Up and Integration Testing
**Dependencies:** Task Groups 1-4

- [x] 5.0 Complete migration and verify all tests pass
  - [x] 5.1 Update import statements throughout codebase
    - Find all files importing from `storyville.site import Site, make_site`
    - Verify imports still work (import path unchanged, now from package)
    - Update any `site.find_path(path)` calls to `find_path(site, path)`
    - Files to check:
      - `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/stories.py` (line 3)
      - `/Users/pauleveritt/projects/t-strings/storyville/tests/test_site.py` (line 4)
      - Any other files importing Site or make_site
  - [x] 5.2 Delete old site.py file
    - Remove `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/site.py`
    - Verify all code has been migrated to site/ package
  - [x] 5.3 Run complete test suite
    - Run: `just test`
    - All tests must pass
    - Expected test count: approximately 20-40 feature tests plus integration tests
  - [x] 5.4 Run type checking
    - Run: `just typecheck`
    - No type errors allowed
    - Verify all type hints use modern syntax (PEP 604: `X | Y`)
  - [x] 5.5 Run formatting
    - Run: `just fmt`
    - Ensure code follows project formatting standards
  - [x] 5.6 Final verification
    - Verify Site package follows same pattern as section/, subject/, story/
    - Verify all node types use .items for child collections
    - Verify make_site() and find_path() work as standalone helpers
    - Verify SiteView renders without parent link
    - Verify breaking changes are documented (find_path call signature)

**Acceptance Criteria:**
- All tests pass (`just test`)
- Type checking passes (`just typecheck`)
- Formatting passes (`just fmt`)
- Old site.py deleted
- Site package structure matches section/subject/story pattern
- All .items references work correctly
- Import statements updated correctly

## Execution Order

Recommended implementation sequence:
1. **Package Structure (Task Group 1)**: Create site/ package and Site model with inheritance
2. **View Layer (Task Group 2)**: Implement SiteView following existing pattern
3. **Helper Functions (Task Group 3)**: Extract make_site() and find_path() as standalone functions
4. **Consistency Refactoring (Task Group 4)**: Refactor Subject.stories → Subject.items throughout codebase
5. **Final Integration (Task Group 5)**: Clean up old files, update imports, run all quality checks

## Key Implementation Notes

### Type Safety
- All type hints use modern Python syntax (PEP 604: `X | Y`, not `Union[X, Y]`)
- Use `TYPE_CHECKING` guard for circular import prevention
- Site inherits from `BaseNode["Site"]` using PEP 695 generic syntax
- find_path return type: `Site | Section | Subject | Story | None`

### File References
- **Pattern to follow**: `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/section/` (models.py, views.py, __init__.py)
- **Current Site implementation**: `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/site.py` (to be deleted)
- **BaseNode implementation**: `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/nodes.py`

### Breaking Changes (Acceptable)
- `site.find_path(path)` becomes `find_path(site, path)` - method to function
- Import path stays same but source changes from file to package

### Testing Strategy
- Each task group writes 2-8 focused tests covering critical behaviors only
- Each task group runs only its own tests during development
- Task Group 5 runs the complete test suite for integration verification
- Total expected new/updated tests: approximately 16-34 tests across all groups
- Focus on critical workflows, skip exhaustive edge case coverage

### Consistency Goals
After completion, all node types will use `.items` for child collections:
- `Site.items: dict[str, Section]` ✓ (already correct)
- `Section.items: dict[str, Subject]` ✓ (already correct)
- `Subject.items: list[Story]` ← Changed from `.stories`
- `Story` has no child collections

### Quality Gates
All three checks must pass before considering work complete:
- `just test` - All tests pass
- `just typecheck` - No type errors
- `just fmt` - Code properly formatted
