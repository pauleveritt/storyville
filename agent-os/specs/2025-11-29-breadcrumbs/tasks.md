# Task Breakdown: Breadcrumbs Navigation Fix

## Overview

Total Tasks: 8 major task groups
Estimated Sub-tasks: 42

## Task List

### Task Group 1: Data Model Foundation

**Dependencies:** None

- [ ] 1.0 Add resource_path attribute to BaseNode
  - [ ] 1.1 Write 2-8 focused tests for BaseNode.resource_path
    - Test resource_path initialization with empty string default
    - Test resource_path assignment during post_update()
    - Test resource_path format for different node types (Section, Subject)
    - Test resource_path inheritance across Catalog/Section/Subject
    - File: `tests/nodes_test.py` (or create if needed)
  - [ ] 1.2 Add resource_path field to BaseNode dataclass
    - Location: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/nodes.py`
    - Add after line 142: `resource_path: str = field(init=False, default="")`
    - Type as `str` (non-optional)
  - [ ] 1.3 Update BaseNode.post_update() to populate resource_path
    - Calculate resource_path from tree_node and parent
    - For Catalog (root): `resource_path = ""`
    - For Section: `resource_path = self.name`
    - For Subject: `resource_path = f"{parent.resource_path}/{self.name}"`
    - Add logic at line 165 in BaseNode.post_update()
  - [ ] 1.4 Ensure data model tests pass
    - Run: `just test tests/nodes_test.py` (or relevant test file)
    - Verify all 2-8 tests pass
    - Run: `just typecheck` to verify type hints
  - [ ] 1.5 Quality gates
    - Run: `just fmt` to format code
    - Verify no type errors in nodes.py

**Acceptance Criteria:**
- BaseNode has resource_path: str field
- resource_path populated correctly during tree construction
- Catalog has resource_path=""
- Section has resource_path="section_name"
- Subject has resource_path="section_name/subject_name"
- All 2-8 tests pass
- Type checking passes

---

### Task Group 2: Tree Construction Integration

**Dependencies:** Task Group 1

- [ ] 2.0 Populate resource_path during catalog construction
  - [ ] 2.1 Write 2-8 focused tests for make_catalog resource_path population
    - Test Catalog has resource_path="" after construction
    - Test Sections have correct resource_path format
    - Test Subjects have correct nested resource_path format
    - Test resource_path flows through entire tree hierarchy
    - File: `tests/catalog/helpers_test.py` (or create if needed)
  - [ ] 2.2 Verify resource_path in make_catalog function
    - Location: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/catalog/helpers.py`
    - No code changes needed (post_update handles it from Task 1.3)
    - Verify that post_update calls at lines 46, 60, 70 will populate resource_path
  - [ ] 2.3 Add Story.post_update to populate resource_path
    - Story doesn't inherit from BaseNode, needs separate implementation
    - Location: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/story/models.py`
    - Add `resource_path: str = ""` field
    - Update Story.post_update() to calculate: `f"{parent.resource_path}/{story.name}"`
  - [ ] 2.4 Ensure tree construction tests pass
    - Run: `just test tests/catalog/helpers_test.py`
    - Verify all 2-8 tests pass
    - Verify resource_path populated at all levels
  - [ ] 2.5 Quality gates
    - Run: `just typecheck`
    - Run: `just fmt`

**Acceptance Criteria:**
- make_catalog populates resource_path on all nodes
- Story model has resource_path field and calculation logic
- Entire tree has correct resource_path values
- All 2-8 tests pass
- Type checking passes

---

### Task Group 3: Component Renaming (current_path → resource_path)

**Dependencies:** Task Groups 1-2

- [ ] 3.0 Rename current_path to resource_path across all components
  - [ ] 3.1 Write 2-8 focused tests for renamed parameter
    - Test Layout accepts resource_path parameter
    - Test LayoutMain receives resource_path correctly
    - Test LayoutAside receives resource_path correctly
    - Test Breadcrumbs uses resource_path (not current_path)
    - Files: Update existing component tests
  - [ ] 3.2 Rename in Layout component
    - Location: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/layout.py`
    - Line 32: Change `current_path: str | None = None` to `resource_path: str = ""`
    - Update all references to current_path within Layout.__call__()
    - Pass resource_path to LayoutMain and LayoutAside
  - [ ] 3.3 Rename in LayoutMain component
    - Location: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/main/main.py`
    - Change parameter from current_path to resource_path
    - Update type hint to `str` (non-optional)
    - Pass resource_path to Breadcrumbs
  - [ ] 3.4 Rename in LayoutAside component
    - Location: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/aside/aside.py`
    - Change parameter from current_path to resource_path
    - Update type hint to `str` (non-optional)
  - [ ] 3.5 Rename in Breadcrumbs component
    - Location: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/breadcrumbs/breadcrumbs.py`
    - Line 18: Change `current_path: str | None = None` to `resource_path: str = ""`
    - Update all internal references from self.current_path to self.resource_path
    - Update condition at line 27: `if not self.resource_path:`
  - [ ] 3.6 Update NavigationTree component
    - Location: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/navigation_tree/navigation_tree.py`
    - Rename current_path parameter to resource_path
    - Update all references
  - [ ] 3.7 Ensure component tests pass
    - Run: `just test tests/components/`
    - Verify all component tests pass with new parameter name
  - [ ] 3.8 Quality gates
    - Run: `just typecheck`
    - Run: `just fmt`

**Acceptance Criteria:**
- All components use resource_path instead of current_path
- Type hints updated to str (non-optional)
- All component tests pass
- No references to current_path remain in components
- Type checking passes

---

### Task Group 4: View Signature Updates

**Dependencies:** Task Group 3

- [ ] 4.0 Update all view signatures to accept and use resource_path
  - [ ] 4.1 Write 2-8 focused tests for view resource_path handling
    - Test SectionView instantiation with resource_path
    - Test SubjectView instantiation with resource_path
    - Test StoryView instantiation with resource_path
    - Test resource_path passed to Layout in each view
    - Files: Update existing view tests
  - [ ] 4.2 Update SectionView
    - Location: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/section/views.py`
    - Add `resource_path: str` parameter to __init__
    - Store as instance attribute: `self.resource_path = resource_path`
    - Pass to Layout when rendering: `Layout(resource_path=self.resource_path, ...)`
    - Pattern: Extract from section.resource_path
  - [ ] 4.3 Update SubjectView
    - Location: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/subject/views.py`
    - Add `resource_path: str` parameter to __init__
    - Store as instance attribute: `self.resource_path = resource_path`
    - Pass to Layout when rendering: `Layout(resource_path=self.resource_path, ...)`
    - Pattern: Extract from subject.resource_path
  - [ ] 4.4 Update StoryView
    - Location: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/story/views.py`
    - Add `resource_path: str` parameter to __init__
    - Store as instance attribute: `self.resource_path = resource_path`
    - Pass to Layout when rendering: `Layout(resource_path=self.resource_path, ...)`
    - Pattern: Extract from story.resource_path
  - [ ] 4.5 Update CatalogView (verify no changes needed)
    - Location: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/catalog/views.py`
    - Verify that CatalogView does NOT pass resource_path (no breadcrumbs on home)
    - Should pass `resource_path=""` or omit parameter
  - [ ] 4.6 Ensure view tests pass
    - Run: `just test tests/section/` `tests/subject/` `tests/story/` `tests/catalog/`
    - Verify all view tests pass
  - [ ] 4.7 Quality gates
    - Run: `just typecheck`
    - Run: `just fmt`

**Acceptance Criteria:**
- All view __init__ methods accept resource_path: str
- Views store resource_path as instance attribute
- Views pass resource_path to Layout component
- CatalogView does not use breadcrumbs (resource_path="")
- All view tests pass
- Type checking passes

---

### Task Group 5: Build System Integration

**Dependencies:** Task Group 4

- [ ] 5.0 Update build.py to pass resource_path to views
  - [ ] 5.1 Write 2-8 focused tests for build resource_path flow
    - Test _render_all_views passes resource_path to SectionView
    - Test _render_all_views passes resource_path to SubjectView
    - Test _render_all_views passes resource_path to StoryView
    - Test resource_path format matches expected patterns
    - File: `tests/build_test.py` (or create if needed)
  - [ ] 5.2 Update _render_all_views for SectionView
    - Location: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/build.py`
    - Line 60-62: Add resource_path parameter
    - Extract from section object: `section.resource_path`
    - Pass to SectionView: `SectionView(section=section, site=catalog, cached_navigation=cached_nav, resource_path=section.resource_path)`
  - [ ] 5.3 Update _render_all_views for SubjectView
    - Line 68-70: Add resource_path parameter
    - Extract from subject object: `subject.resource_path`
    - Pass to SubjectView: `SubjectView(subject=subject, site=catalog, cached_navigation=cached_nav, resource_path=subject.resource_path)`
  - [ ] 5.4 Update _render_all_views for StoryView
    - Line 77-84: Add resource_path parameter
    - Extract from story object: `story.resource_path`
    - Pass to StoryView: `StoryView(story=story, site=catalog, cached_navigation=cached_nav, with_assertions=with_assertions, resource_path=story.resource_path)`
  - [ ] 5.5 Update NavigationTree calls in build.py
    - Line 41: Update NavigationTree to use resource_path instead of current_path
    - Change: `NavigationTree(sections=catalog.items, resource_path=None)`
  - [ ] 5.6 Ensure build tests pass
    - Run: `just test tests/build_test.py`
    - Verify all 2-8 tests pass
  - [ ] 5.7 Quality gates
    - Run: `just typecheck`
    - Run: `just fmt`

**Acceptance Criteria:**
- _render_all_views extracts resource_path from resource objects
- resource_path passed to all view constructors (Section, Subject, Story)
- NavigationTree updated to use resource_path
- All build tests pass
- Type checking passes

---

### Task Group 6: Template Cleanup (Remove Parent Links)

**Dependencies:** Task Group 5

- [ ] 6.0 Remove Parent links from all view templates
  - [ ] 6.1 Write 2-8 focused tests verifying Parent links removed
    - Test SectionView output does not contain 'href=".."'
    - Test SubjectView output does not contain 'href=".."'
    - Test StoryView output does not contain 'href=".."'
    - Test breadcrumbs component provides navigation instead
    - Files: Update existing view tests
  - [ ] 6.2 Remove Parent link from SectionView
    - Location: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/section/views.py`
    - Find and remove: `<a href="..">Parent</a>` (approximately line 68)
    - Breadcrumbs now provide navigation to parent
  - [ ] 6.3 Remove Parent links from SubjectView
    - Location: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/subject/views.py`
    - Find and remove: `<a href="..">Parent</a>` (approximately lines 64 and 85)
    - May be in multiple locations within template
  - [ ] 6.4 Remove Parent links from StoryView
    - Location: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/story/views.py`
    - Find and remove: `<a href="..">Parent</a>` (approximately lines 158, 170, 194, 208)
    - Check multiple locations within template
  - [ ] 6.5 Ensure view tests pass after cleanup
    - Run: `just test tests/section/` `tests/subject/` `tests/story/`
    - Verify all tests pass without Parent links
  - [ ] 6.6 Quality gates
    - Run: `just typecheck`
    - Run: `just fmt`

**Acceptance Criteria:**
- No `<a href="..">Parent</a>` links in SectionView template
- No `<a href="..">Parent</a>` links in SubjectView template
- No `<a href="..">Parent</a>` links in StoryView template
- Breadcrumbs provide navigation to parent pages
- All view tests pass
- Type checking passes

---

### Task Group 7: Relative Path Conversion

**Dependencies:** Task Group 6

- [ ] 7.0 Convert breadcrumb links to relative paths
  - [ ] 7.1 Write 2-8 focused tests for relative path calculation
    - Test breadcrumbs from Section level (depth 1) uses "../"
    - Test breadcrumbs from Subject level (depth 2) uses "../../"
    - Test breadcrumbs from Story level (depth 3) uses "../../../"
    - Test Home link navigates relatively based on depth
    - Test intermediate links combine upward + forward paths
    - File: `tests/components/breadcrumbs/breadcrumbs_test.py`
  - [ ] 7.2 Add depth calculation helper to Breadcrumbs
    - Location: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/breadcrumbs/breadcrumbs.py`
    - Calculate depth from resource_path: `depth = len([p for p in resource_path.split("/") if p])`
    - Section: depth=1, Subject: depth=2, Story: depth=3
  - [ ] 7.3 Update Home link to use relative path
    - Replace line 38: `<a href="/">Home</a>`
    - With: `<a href="{relative_root}">Home</a>`
    - Calculate relative_root: `"../" * depth`
    - Section: "../", Subject: "../../", Story: "../../../"
  - [ ] 7.4 Update Section link to use relative path
    - Replace line 42: `f"/{section_name}"`
    - With: `f"{relative_root}{section_name}/"`
    - Combine upward traversal with section name
  - [ ] 7.5 Update Subject link to use relative path
    - Replace line 55: `f"/{section_name}/{subject_name}"`
    - With: `f"{relative_root}{section_name}/{subject_name}/"`
    - Calculate relative path from current depth
    - For Story viewing Subject: `"../"`
    - For other depths: calculate accordingly
  - [ ] 7.6 Ensure breadcrumbs tests pass
    - Run: `just test tests/components/breadcrumbs/`
    - Verify all 2-8 tests pass
    - Verify relative paths calculated correctly
  - [ ] 7.7 Quality gates
    - Run: `just typecheck`
    - Run: `just fmt`

**Acceptance Criteria:**
- Breadcrumbs calculate depth from resource_path
- Home link uses relative path based on depth
- Section links use relative paths
- Subject links use relative paths
- No absolute paths (/) in breadcrumb links
- All breadcrumb tests pass
- Type checking passes

---

### Task Group 8: Test Coverage Review & Integration Testing

**Dependencies:** Task Groups 1-7

- [ ] 8.0 Review existing tests and verify breadcrumbs functionality
  - [ ] 8.1 Review tests from Task Groups 1-7
    - Data model tests (Task 1.1): 2-8 tests
    - Tree construction tests (Task 2.1): 2-8 tests
    - Component rename tests (Task 3.1): 2-8 tests
    - View signature tests (Task 4.1): 2-8 tests
    - Build integration tests (Task 5.1): 2-8 tests
    - Template cleanup tests (Task 6.1): 2-8 tests
    - Relative path tests (Task 7.1): 2-8 tests
    - Total existing tests: approximately 14-56 tests
  - [ ] 8.2 Analyze test coverage gaps for breadcrumbs feature
    - Identify critical user workflows lacking coverage:
      - End-to-end: Navigate from Story → Subject → Section → Home
      - Integration: Build system → Views → Layout → Breadcrumbs
      - Edge cases: Empty resource_path handling
    - Focus ONLY on gaps related to breadcrumbs feature
    - Prioritize end-to-end workflows over unit test gaps
  - [ ] 8.3 Write up to 10 additional strategic tests maximum
    - End-to-end breadcrumbs rendering test
    - Integration test: full tree construction → view rendering
    - Test breadcrumbs display on built static pages
    - Test resource_path flow from Catalog → Section → Subject → Story
    - Test breadcrumbs links navigate correctly
    - Maximum 10 new tests to fill critical gaps
  - [ ] 8.4 Run full test suite for breadcrumbs feature
    - Run: `just test`
    - Verify all tests pass (approximately 24-66 tests total)
    - Expected: All feature-specific tests pass
    - Do NOT require entire application test suite to pass
  - [ ] 8.5 Manual verification on built pages
    - Run: `storytime build examples.minimal` (or test catalog)
    - Open built pages in browser
    - Verify breadcrumbs appear on Section/Subject/Story pages
    - Verify breadcrumbs do NOT appear on Catalog/home page
    - Verify breadcrumb links navigate correctly
    - Verify no broken links or console errors
  - [ ] 8.6 Final quality gates
    - Run: `just test` (full suite)
    - Run: `just typecheck` (verify no type errors)
    - Run: `just fmt` (ensure code formatted)
    - All gates must pass

**Acceptance Criteria:**
- All feature-specific tests pass (approximately 24-66 tests total)
- No more than 10 additional tests added for gap coverage
- Breadcrumbs render correctly on built pages
- Breadcrumbs do NOT appear on home page
- Breadcrumb links use relative paths and navigate correctly
- No Parent links remain in templates
- All quality gates pass (test, typecheck, fmt)

---

## Execution Order

Recommended implementation sequence:

1. **Data Model Foundation (Task Group 1)** - Add resource_path to BaseNode
2. **Tree Construction Integration (Task Group 2)** - Populate resource_path during tree building
3. **Component Renaming (Task Group 3)** - Rename current_path → resource_path in all components
4. **View Signature Updates (Task Group 4)** - Update views to accept and use resource_path
5. **Build System Integration (Task Group 5)** - Connect resource_path from models to views
6. **Template Cleanup (Task Group 6)** - Remove obsolete Parent links
7. **Relative Path Conversion (Task Group 7)** - Convert breadcrumb links to relative paths
8. **Test Coverage Review & Integration Testing (Task Group 8)** - Verify complete functionality

## Key Files to Modify

### Core Models
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/nodes.py` (BaseNode)
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/story/models.py` (Story)
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/catalog/helpers.py` (make_catalog)

### Components
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/layout.py` (Layout)
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/main/main.py` (LayoutMain)
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/aside/aside.py` (LayoutAside)
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/breadcrumbs/breadcrumbs.py` (Breadcrumbs)
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/navigation_tree/navigation_tree.py` (NavigationTree)

### Views
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/section/views.py` (SectionView)
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/subject/views.py` (SubjectView)
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/story/views.py` (StoryView)
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/catalog/views.py` (CatalogView - verify)

### Build System
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/build.py` (_render_all_views)

### Tests
- All test files that reference current_path (rename to resource_path)
- Component tests: `tests/components/*/`
- View tests: `tests/section/`, `tests/subject/`, `tests/story/`, `tests/catalog/`
- Build tests: `tests/build_test.py`
- Node tests: `tests/nodes_test.py`

## Testing Strategy

### Test-Driven Approach
- Each task group starts with writing 2-8 focused tests (x.1 sub-task)
- Development follows test requirements
- Each task group ends with running ONLY those tests (verification sub-task)
- Task Group 8 provides final integration verification

### Quality Gates (Run After Each Task Group)
```bash
just test      # Run tests (feature-specific during development, full suite at end)
just typecheck # Verify type hints
just fmt       # Format code
```

### Manual Verification (Task Group 8)
```bash
storytime build examples.minimal
# Open built pages in browser
# Verify breadcrumbs display and navigate correctly
```

## Notes

- **Python 3.14+ Standards**: Use modern type hints (`str | None` syntax, PEP 695 generics)
- **Minimal Testing During Development**: Each group writes only 2-8 tests, focus on critical behaviors
- **Type Safety**: resource_path typed as `str` (non-optional) throughout
- **Backward Compatibility**: Rename current_path → resource_path is a breaking change (acceptable per spec)
- **No Visual Changes**: Breadcrumbs component rendering logic and styling remain unchanged
- **Scope**: Changes affect static build output, not development server functionality
