# Task Breakdown: Layout Component

## Overview

Total Tasks: 4 task groups with 17 sub-tasks

This feature creates a shared Layout component that provides consistent HTML structure (html, head, body) for all views
with configurable page titles and content insertion via a main element.

## Task List

### Component Layer

#### Task Group 1: Layout Component Implementation

**Dependencies:** None

- [x] 1.0 Complete Layout component
    - [x] 1.1 Write 2-8 focused tests for Layout component
        - Test: Layout renders complete HTML structure with html, head, body tags
        - Test: Layout includes meta charset and viewport tags in head
        - Test: Layout title concatenates view_title and site.title correctly (e.g., "Home - My Site")
        - Test: Layout title uses only site.title when view_title is None (no hyphen)
        - Test: Layout inserts children content into main element
        - Test: Layout includes navigation bar with site branding
        - Test: Layout includes sidebar with SectionsListing component
        - Test: Layout satisfies View Protocol (__call__() -> Node)
        - Create tests in:
          `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/layout_test.py`
        - Use aria-testing library pattern from
          `/Users/pauleveritt/projects/pauleveritt/storytime/tests/site/test_site_views.py`
        - Import: `from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name`
        - Use type guard pattern: `assert isinstance(result, Element)`
    - [x] 1.2 Move Layout from `__init__.py` to `layout.py`
        - Move existing Layout class from
          `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/__init__.py`
        - Create new file: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/layout.py`
        - Keep existing HTML structure (navbar, sidebar, main content area) from current implementation
    - [x] 1.3 Update Layout component signature
        - Change from: `Layout(title: str, children: list[Node], site: Site)`
        - Change to: `Layout(view_title: str | None, site: Site, children: Element | Fragment | None)`
        - Add imports: `from tdom import Element, Fragment, Node, html`
        - Use PEP 604 union syntax for type hints
        - Maintain `__call__(self) -> Node` method to satisfy View Protocol
    - [x] 1.4 Implement title concatenation logic
        - Update title tag from hardcoded "Hello Bulma!" to: `<title>{title_text}</title>`
        - When view_title is not None: `title_text = f"{view_title} - {self.site.title}"`
        - When view_title is None: `title_text = self.site.title`
        - Reference line 21 in current
          `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/__init__.py`
    - [x] 1.5 Update CSS link path for new static directory location
        - Change href from: `../static/bulma.css`
        - Change to: `../static/bulma.css` (path remains same, but static dir will move)
        - Reference line 22 in current
          `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/__init__.py`
    - [x] 1.6 Ensure children content placement in main element
        - Verify children interpolation at line 56: `{self.children}`
        - Ensure main element is inside Bulma columns layout (existing pattern is correct)
        - Children go in main column, not sidebar column (already correct in existing code)
    - [x] 1.7 Update `__init__.py` to export Layout from new location
        - Update `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/__init__.py`
        - Change to: `from storytime.components.layout.layout import Layout`
        - Add: `__all__ = ["Layout"]`
    - [x] 1.8 Ensure Layout component tests pass
        - Run ONLY the 2-8 tests written in 1.1
        - Command:
          `pytest /Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/layout_test.py -v`
        - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**

- The 2-8 tests written in 1.1 pass
- Layout component file exists at `layout/layout.py`
- Layout accepts correct parameters with modern type hints
- Title concatenation works correctly for both None and non-None view_title
- Layout satisfies View Protocol
- Component renders complete HTML structure

### Static Assets Layer

#### Task Group 2: Static Assets Organization

**Dependencies:** Task Group 1

- [x] 2.0 Complete static assets reorganization
    - [x] 2.1 Create new static directory structure
        - Create directory: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/static/`
        - Use `mkdir -p` to create directory structure
    - [x] 2.2 Move bulma.css to new location
        - Move from: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/static/bulma.css`
        - Move to: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/static/bulma.css`
        - Use `mv` command or `shutil.move` in Python
    - [x] 2.3 Remove old static directory
        - Remove: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/static/`
        - Only after confirming bulma.css was successfully moved
    - [x] 2.4 Update Site model's __post_init__ method
        - File: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/site/models.py`
        - Update line 31: Change `sd = PACKAGE_DIR / "static"`
        - Change to: `sd = PACKAGE_DIR / "components" / "layout" / "static"`
        - Keep rest of logic unchanged (lines 32-33)
    - [x] 2.5 Verify static assets are discovered correctly
        - Run existing tests to ensure Site.static_dir is set correctly
        - Command: `pytest /Users/pauleveritt/projects/pauleveritt/storytime/tests/site/ -v -k static`
        - Verify build.py can still copy static directory (line 25-26 in build.py)

**Acceptance Criteria:**

- Static directory exists at new location: `components/layout/static/`
- bulma.css file is in new static directory
- Old static directory is removed
- Site.__post_init__ discovers static_dir at new path
- Build process can still copy static assets to output

### View Integration Layer

#### Task Group 3: View Updates to Use Layout

**Dependencies:** Task Groups 1, 2

- [x] 3.0 Complete view integration with Layout
    - [x] 3.1 Update SiteView to use Layout component
        - File: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/site/views.py`
        - Import Layout: `from storytime.components.layout import Layout`
        - Wrap existing content (lines 69-72) as children parameter
        - Update `__call__()` method to:
          ```python
          def __call__(self) -> Node:
              # Existing content generation logic (lines 36-67)
              content = html(t"""<div>
          <h1>{self.site.title}</h1>
          {content}
          </div>""")

              # Wrap with Layout
              layout = Layout(view_title="Home", site=self.site, children=content)
              return layout()
          ```
        - Use view_title="Home" for site index page
    - [x] 3.2 Update SectionView to use Layout component
        - File: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/section/views.py`
        - Import Layout: `from storytime.components.layout import Layout`
        - Import Site type: `from storytime.site import Site`
        - Add site parameter to SectionView: `site: Site`
        - Wrap existing content (lines 53-58) as children parameter
        - Update `__call__()` method to:
          ```python
          def __call__(self) -> Node:
              # Existing content generation logic (lines 34-51)
              content = html(t"""<div>
          <h1>{self.section.title}</h1>
          {description_p}
          {content}
          <a href="..">Parent</a>
          </div>""")

              # Wrap with Layout
              layout = Layout(view_title=self.section.title, site=self.site, children=content)
              return layout()
          ```
        - Use section.title as view_title
    - [x] 3.3 Update SubjectView to use Layout component
        - File: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/subject/views.py`
        - Import Layout: `from storytime.components.layout import Layout`
        - Import Site type: `from storytime.site import Site`
        - Add site parameter to SubjectView: `site: Site`
        - Wrap existing content (lines 41-46 and 56-63) as children parameter
        - Update `__call__()` method to:
          ```python
          def __call__(self) -> Node:
              # Existing content generation logic (lines 33-63)
              if not self.subject.items:
                  content = html(t"""<div>
          <h1>{self.subject.title}</h1>
          <p>Target: {target_name}</p>
          <p>No stories defined for this component</p>
          <a href="..">Parent</a>
          </div>""")
              else:
                  content = html(t"""<div>
          <h1>{self.subject.title}</h1>
          <p>Target: {target_name}</p>
          <ul>
          {story_items}
          </ul>
          <a href="..">Parent</a>
          </div>""")

              # Wrap with Layout
              layout = Layout(view_title=self.subject.title, site=self.site, children=content)
              return layout()
          ```
        - Use subject.title as view_title
    - [x] 3.4 Update view instantiations to pass site parameter
        - Search codebase for SectionView and SubjectView instantiations
        - Add site parameter to each instantiation
        - Check files: `build.py`, `app.py`, any other files that create view instances
        - Note: Section and Subject models may need parent chain access to get site
    - [x] 3.5 Verify all view tests still pass
        - Run view tests: `pytest /Users/pauleveritt/projects/pauleveritt/storytime/tests/site/test_site_views.py -v`
        - Run view tests:
          `pytest /Users/pauleveritt/projects/pauleveritt/storytime/tests/section/test_section_views.py -v`
        - Run view tests:
          `pytest /Users/pauleveritt/projects/pauleveritt/storytime/tests/subject/test_subject_views.py -v`
        - Tests may need updates to pass site parameter to views
        - Tests should verify full HTML structure now includes html, head, body tags

**Acceptance Criteria:**

- SiteView wraps content with Layout
- SectionView wraps content with Layout and passes section.title as view_title
- SubjectView wraps content with Layout and passes subject.title as view_title
- All views delegate HTML wrapper to Layout
- All view tests pass (may need test updates for new signatures)
- Views maintain their existing internal logic and links

### Testing & Verification

#### Task Group 4: Test Review & Final Verification

**Dependencies:** Task Groups 1-3

- [x] 4.0 Review existing tests and verify integration
    - [x] 4.1 Review tests from Task Groups 1-3
        - Review the 2-8 tests written for Layout component (Task 1.1)
        - Review any test updates made for view integration (Task 3.5)
        - Total existing tests: approximately 8-12 tests
    - [x] 4.2 Analyze test coverage gaps for Layout feature only
        - Identify critical Layout integration workflows that lack test coverage
        - Focus on:
            - Full page rendering with Layout wrapper in all three views
            - Title concatenation edge cases (empty strings, special characters)
            - Layout with None children parameter
            - Layout CSS link resolves correctly
        - Do NOT assess entire application test coverage
        - Prioritize end-to-end rendering workflows
    - [x] 4.3 Write up to 6 additional strategic tests maximum
        - Add maximum of 6 new tests to fill identified critical gaps
        - Suggested tests:
            - Test: SiteView renders full HTML document with proper head/body structure
            - Test: SectionView title appears in browser title tag correctly
            - Test: SubjectView includes navigation and sidebar in rendered output
            - Test: Layout handles None children gracefully
            - Test: Layout CSS link href is correct and points to valid destination in static directory
            - Test: Static asset paths in rendered pages (link, img tags) resolve correctly at different path depths
            - Test: All three views produce valid HTML documents
        - Add tests to appropriate test files (view test files or layout test file)
        - Do NOT write comprehensive coverage for all scenarios
        - IMPORTANT: Include test verifying static asset paths point to valid destinations
    - [x] 4.4 Run feature-specific tests only
        - Run Layout component tests:
          `pytest /Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/layout_test.py -v`
        - Run SiteView tests:
          `pytest /Users/pauleveritt/projects/pauleveritt/storytime/tests/site/test_site_views.py -v`
        - Run SectionView tests:
          `pytest /Users/pauleveritt/projects/pauleveritt/storytime/tests/section/test_section_views.py -v`
        - Run SubjectView tests:
          `pytest /Users/pauleveritt/projects/pauleveritt/storytime/tests/subject/test_subject_views.py -v`
        - Expected total: approximately 14-18 tests maximum
        - Do NOT run the entire application test suite
        - Verify critical workflows pass
    - [x] 4.5 Run quality checks
        - Type checking: `just typecheck` (verify all type hints are correct)
        - Formatting: `just fmt` (ensure code formatting is consistent)
        - All quality checks must pass
    - [x] 4.6 Manual verification
        - Build the site: `python -m storytime build . output`
        - Open `output/index.html` in browser
        - Verify:
            - Page has proper HTML structure
            - Browser tab shows correct title (e.g., "Home - Storytime")
            - Navigation bar appears with site branding
            - Sidebar shows sections
            - Main content area shows site content
            - Bulma CSS is loaded (check styling)
        - Check browser console for any errors

**Acceptance Criteria:**

- All feature-specific tests pass (approximately 14-18 tests total)
- Critical Layout integration workflows are covered by tests
- No more than 6 additional tests added when filling in testing gaps
- Testing focused exclusively on Layout feature requirements
- Type checking passes with no errors
- Code formatting is consistent
- Manual browser verification shows correct rendering

## Execution Order

Recommended implementation sequence:

1. Component Layer (Task Group 1) - Create and test Layout component
2. Static Assets Layer (Task Group 2) - Move static files to new location
3. View Integration Layer (Task Group 3) - Update all views to use Layout
4. Testing & Verification (Task Group 4) - Verify integration and add strategic tests

## Notes

### Existing Patterns to Follow

**tdom Templating Pattern:**

- Use `html(t'''...''')` for template strings (see existing Layout __init__.py)
- Interpolate variables: `{variable_name}`
- Interpolate components: `<{ComponentName} prop={value} />`
- Lists of elements: `{[items]}`

**View Protocol Pattern:**

- All views implement `__call__(self) -> Node`
- Tests use type guard: `assert isinstance(result, Element)`
- Views are dataclasses with `@dataclass` decorator
- See examples in: `site/views.py`, `section/views.py`, `subject/views.py`

**Test Pattern (aria-testing):**

- Import: `from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name`
- Import: `from tdom import Element`
- Use type guards: `assert isinstance(result, Element)`
- Query elements: `h1 = get_by_tag_name(result, "h1")`
- Get text: `get_text_content(h1)`
- See example: `/Users/pauleveritt/projects/pauleveritt/storytime/tests/site/test_site_views.py`

### Type Safety Requirements

- Use PEP 604 union syntax: `str | None` (not `Optional[str]`)
- Use modern generics: `list[str]` (not `List[str]`)
- Import types from tdom: `Element`, `Fragment`, `Node`
- Type hint all function parameters and return values
- Layout children parameter: `Element | Fragment | None`

### Important Constraints

- Do NOT modify SectionsListing component (no changes needed)
- Do NOT implement build-time static asset copying (already done in build.py)
- Do NOT add multiple layout variations or theming
- Do NOT add footer, breadcrumbs, or SEO meta tags beyond basic ones
- Maintain existing view content logic (only wrap with Layout)
- Keep existing internal links and navigation in views

### File Organization

**Component Structure:**

```
src/storytime/components/layout/
├── __init__.py          # Export Layout class
├── layout.py            # Layout component implementation
├── layout_test.py       # Layout component tests
└── static/
    └── bulma.css        # Bulma CSS framework
```

**View Structure:**

```
src/storytime/
├── site/
│   └── views.py         # SiteView (needs update)
├── section/
│   └── views.py         # SectionView (needs update)
└── subject/
    └── views.py         # SubjectView (needs update)
```
