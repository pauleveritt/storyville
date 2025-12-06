# Task Breakdown: SiteView Component

## Overview
Total Tasks: 11
Estimated Time: 2-3 hours

## Task List

### Cleanup Phase

#### Task Group 1: Remove IndexView and Related Files
**Dependencies:** None

- [x] 1.0 Remove IndexView component and tests
  - [x] 1.1 Delete IndexView component file
    - Remove: `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/views/index_view.py`
  - [x] 1.2 Delete index component directory
    - Remove directory: `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/components/index/`
    - Remove all files: `__init__.py`, `stories.py`, and any other files
  - [x] 1.3 Search for and remove test files referencing IndexView
    - Search for test files containing "IndexView" or "index_view"
    - Remove identified test files
  - [x] 1.4 Search for imports and references to IndexView
    - Check `__init__.py` files for IndexView exports
    - Check other modules for IndexView imports
    - Remove any references found

**Acceptance Criteria:**
- IndexView file deleted
- Index component directory deleted
- No test files reference IndexView
- No import errors when running existing tests
- `just test` passes (existing tests still work)

### Component Implementation Phase

#### Task Group 2: Create SiteView Component
**Dependencies:** Task Group 1

- [x] 2.0 Implement SiteView component
  - [x] 2.1 Create views directory if needed
    - Check if `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/views/` exists
    - Create directory if needed with `__init__.py`
  - [x] 2.2 Write 2-8 focused tests for SiteView component
    - Limit to 2-8 highly focused tests maximum
    - Test file: `/Users/pauleveritt/projects/t-strings/storyville/tests/views/test_site_view.py`
    - Test SiteView returns a Node when called
    - Test rendering with empty Site (no sections)
    - Test rendering with single section
    - Test rendering with multiple sections in correct insertion order
    - Test subject count display (calculated from `len(section.items)`)
    - Test section descriptions appear when present, omitted when None
    - Test URL generation follows `/section/{section_name}` pattern
    - Use aria_testing helpers for DOM assertions (get_by_tag_name, query_all_by_tag_name, get_text_content)
    - Follow pattern from existing test: `/Users/pauleveritt/projects/t-strings/storyville/tests/site/test_site_views.py`
  - [x] 2.3 Implement SiteView dataclass
    - File: `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/views/site_view.py`
    - Import: `from dataclasses import dataclass`
    - Import: `from tdom import html, Node`
    - Import: `from storyville.site.models import Site`
    - Use `@dataclass` decorator
    - Add `site: Site` parameter
    - Follow pattern from SectionsListing and ComponentView
  - [x] 2.4 Implement `__call__` method
    - Return type: `Node` from tdom
    - Use tdom html templating with t-strings
    - Render sections in insertion order from `site.items.items()`
  - [x] 2.5 Build section listing with required information
    - Use `<ul>` structure with `<li>` elements
    - For each section display:
      - Title (wrapped in `<a>` tag)
      - Link href: `/section/{section_name}` where section_name is the key from Site.items
      - Description (only if `section.description` is not None)
      - Subject count: `len(section.items)` formatted as "(X subjects)"
    - Handle empty site case (no sections)
  - [x] 2.6 Apply modern Python type hints
    - Use PEP 604 syntax: `str | None` instead of `Optional[str]`
    - Use built-in generics: `dict[str, Section]`
    - Ensure Python 3.14+ compatibility
  - [x] 2.7 Run component tests only
    - Run ONLY the 2-8 tests written in 2.2
    - Command: `pytest /Users/pauleveritt/projects/t-strings/storyville/tests/views/test_site_view.py -v`
    - Verify all component tests pass
    - Do NOT run entire test suite at this stage

**Acceptance Criteria:**
- SiteView component created at correct location
- Implements dataclass pattern matching existing components
- `__call__` method returns Node type
- Sections displayed in insertion order
- Section links follow `/section/{section_name}` pattern
- Subject counts calculated correctly
- Descriptions conditionally rendered
- All 2-8 component tests pass
- Modern Python 3.14+ type hints used throughout

### Quality Assurance Phase

#### Task Group 3: Testing and Quality Checks
**Dependencies:** Task Group 2

- [x] 3.0 Run comprehensive quality checks
  - [x] 3.1 Run full test suite
    - Command: `just test`
    - Verify all tests pass including new SiteView tests
    - Verify no broken tests from IndexView removal
  - [x] 3.2 Run type checking
    - Command: `just typecheck`
    - Verify no type errors in SiteView implementation
    - Verify modern type hints are recognized correctly
  - [x] 3.3 Run code formatting
    - Command: `just fmt`
    - Verify code follows project style guidelines
    - Auto-format if needed
  - [x] 3.4 Manual verification checklist
    - [x] Verify SiteView works with empty Site
    - [x] Verify sections appear in insertion order
    - [x] Verify subject counts are accurate
    - [x] Verify descriptions appear/disappear based on presence
    - [x] Verify URLs follow `/section/{section_name}` pattern
    - [x] Verify no IndexView references remain in codebase

**Acceptance Criteria:**
- `just test` passes with all tests
- `just typecheck` passes with no type errors
- `just fmt` passes with consistent formatting
- Manual verification checklist complete
- No IndexView references remain
- SiteView fully functional

## Execution Order

Recommended implementation sequence:
1. **Cleanup Phase** (Task Group 1): Remove IndexView and related files
2. **Component Implementation** (Task Group 2): Create and test SiteView component
3. **Quality Assurance** (Task Group 3): Run comprehensive quality checks

## Notes

**Key Design Decisions:**
- SiteView created in `/src/storyville/views/` (new location, different from existing `/src/storyville/site/views.py`)
- Section display order: insertion order from `site.items.items()` (dict maintains insertion order in Python 3.7+)
- URL pattern: `/section/{section_name}` where section_name is the dict key
- Subject count: calculated as `len(section.items)` where items is dict[str, Subject]
- Conditional rendering: descriptions only shown when `section.description is not None`

**Existing Patterns to Follow:**
- Dataclass pattern from: `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/components/sections_listing/__init__.py`
- Testing pattern from: `/Users/pauleveritt/projects/t-strings/storyville/tests/site/test_site_views.py`
- tdom t-string usage from: ComponentView and SectionsListing examples

**Testing Constraints:**
- Task Group 2: Write 2-8 focused tests maximum
- Task Group 2: Run only new component tests (not full suite)
- Task Group 3: Run full test suite for integration verification
- Use aria_testing helpers for DOM queries and assertions
- Follow existing test style and patterns

**Standards Compliance:**
- Modern Python 3.14+ features (type hints, PEP 604 syntax)
- tdom html templating with t-strings
- Dataclass-based component pattern
- Type safety with Node return type
- Quality checks: test, typecheck, fmt (per CLAUDE.md)
