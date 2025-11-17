# Task Breakdown: Pico Layout

## Overview
Total Tasks: 40+ sub-tasks across 5 major task groups

## Task List

### Core Layout Structure

#### Task Group 1: Layout Component Redesign
**Dependencies:** None

- [x] 1.0 Complete core layout structure
  - [x] 1.1 Write 2-8 focused tests for layout structure
    - Limit to 2-8 highly focused tests maximum
    - Test header navigation rendering with Home/About/Debug links
    - Test footer rendering with copyright text
    - Test main grid structure (header/aside/main/footer)
    - Test current_path parameter acceptance
    - Skip exhaustive testing of all layout variations
  - [x] 1.2 Update Layout component signature
    - Add current_path parameter (str | None = None)
    - Keep existing parameters: view_title, site, children, depth
    - Preserve type hints: children as Element | Fragment | Node | None
  - [x] 1.3 Implement header navigation
    - Replace existing header nav structure
    - Add Home link (href="/")
    - Add About link (href="/about")
    - Add Debug link (href="/debug")
    - Use PicoCSS nav structure with `<ul>` lists
    - Keep "Storytime" branding in first `<ul>`
  - [x] 1.4 Implement footer element
    - Add `<footer>` element at bottom of layout
    - Include centered copyright text: "2025 Storytime"
    - Use default PicoCSS footer styling (no custom CSS)
  - [x] 1.5 Update main grid structure
    - Use PicoCSS grid system for layout
    - Structure: header > main.container > div.grid > (aside + article) > footer
    - Maintain existing `<article>` for children content
    - Preserve depth-based static asset path calculation
  - [x] 1.6 Ensure layout structure tests pass
    - Run ONLY the 2-8 tests written in 1.1
    - Verify header/footer render correctly
    - Verify grid structure matches PicoCSS patterns
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 1.1 pass
- Header contains Home, About, Debug links
- Footer displays copyright text
- Grid layout follows PicoCSS structure
- Existing Layout parameters preserved (backward compatibility)

### Navigation Components

#### Task Group 2: Hierarchical Sidebar Navigation
**Dependencies:** Task Group 1

- [x] 2.0 Complete sidebar navigation
  - [x] 2.1 Write 2-8 focused tests for sidebar navigation
    - Limit to 2-8 highly focused tests maximum
    - Test three-level hierarchy rendering (Section > Subject > Story)
    - Test `<details>` elements render with correct structure
    - Test current_path controls which details have `open` attribute
    - Test stories render as simple `<li><a>` elements (not collapsible)
    - Skip exhaustive testing of all navigation scenarios
  - [x] 2.2 Create NavigationTree component
    - New component: src/storytime/components/navigation_tree/__init__.py
    - Accept parameters: sections (dict[str, Section]), current_path (str | None)
    - Return type: Node
    - Use dataclass pattern matching existing components
    - Follow tdom html t-string syntax pattern
  - [x] 2.3 Implement section-level details rendering
    - Iterate over sections from site.items.values()
    - Render each section as `<details>` element
    - Use `<summary>` for section title
    - Parse current_path to determine if section should have `open` attribute
    - Section gets `open` if current_path starts with section name
  - [x] 2.4 Implement subject-level details rendering (nested)
    - For each section, iterate over section.items.values() (subjects)
    - Render each subject as nested `<details>` inside section
    - Use `<summary>` for subject title
    - Subject gets `open` if current_path matches "section/subject" pattern
    - Nest subject details inside section's `<ul>`
  - [x] 2.5 Implement story-level links
    - For each subject, iterate over subject.items (stories list)
    - Render each story as simple `<li><a href="...">story.title</a></li>`
    - Stories are NOT collapsible (no `<details>`)
    - Use proper URL construction for story links
    - Nest story links inside subject's `<ul>`
  - [x] 2.6 Implement current_path parsing logic
    - Create helper function to parse "section/subject/story" format
    - Return tuple: (section_name | None, subject_name | None, story_name | None)
    - Use structural pattern matching for clean parsing
    - Handle None/empty path gracefully (all details closed)
  - [x] 2.7 Integrate NavigationTree into Layout
    - Replace existing SectionsListing with NavigationTree
    - Pass site.items and current_path to NavigationTree
    - Update `<aside>` structure to wrap NavigationTree
    - Keep "Sections" heading or remove based on visual design
  - [x] 2.8 Ensure sidebar navigation tests pass
    - Run ONLY the 2-8 tests written in 2.1
    - Verify three-level hierarchy renders correctly
    - Verify current_path controls `open` attributes
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 2.1 pass
- NavigationTree renders three-level hierarchy
- Sections and subjects are collapsible (`<details>`)
- Stories are simple links (not collapsible)
- current_path correctly controls which details are open
- All details closed by default when current_path is None

#### Task Group 3: Breadcrumb Navigation
**Dependencies:** Task Group 1, Task Group 2

- [ ] 3.0 Complete breadcrumb navigation
  - [ ] 3.1 Write 2-8 focused tests for breadcrumbs
    - Limit to 2-8 highly focused tests maximum
    - Test breadcrumb generation from current_path
    - Test separator rendering (" > ")
    - Test current page renders as plain text (not link)
    - Test all ancestor levels render as clickable links
    - Skip exhaustive testing of all path combinations
  - [ ] 3.2 Create Breadcrumbs component
    - New component: src/storytime/components/breadcrumbs/__init__.py
    - Accept parameter: current_path (str | None)
    - Return type: Node
    - Use dataclass pattern
    - Follow tdom html t-string syntax
  - [ ] 3.3 Implement breadcrumb generation logic
    - Parse current_path by splitting on "/"
    - Build breadcrumb items: ["Home", section_name, subject_name, story_name]
    - Generate URLs for each level: /, /section/, /section/subject/, etc.
    - Use list comprehension for clean rendering
  - [ ] 3.4 Implement breadcrumb rendering
    - Render "Home" as first item (always a link unless current page is home)
    - Render each path component as link except the last (current page)
    - Use " > " as separator between items
    - Apply default PicoCSS link styling (no custom CSS)
    - Wrap in semantic HTML (`<nav>` with aria-label="Breadcrumb")
  - [ ] 3.5 Integrate Breadcrumbs into Layout
    - Place breadcrumbs between `<aside>` and `<article>`
    - Pass current_path to Breadcrumbs component
    - Ensure breadcrumbs only render when current_path is provided
    - Position within grid layout appropriately
  - [ ] 3.6 Ensure breadcrumb tests pass
    - Run ONLY the 2-8 tests written in 3.1
    - Verify breadcrumbs generate correctly from paths
    - Verify separators and link behavior
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 3.1 pass
- Breadcrumbs generate from current_path
- Separator " > " renders between items
- Current page is plain text, ancestors are links
- Breadcrumbs positioned between sidebar and main content

### New Routes and Views

#### Task Group 4: About and Debug Views
**Dependencies:** Task Group 1

- [ ] 4.0 Complete new views
  - [ ] 4.1 Write 2-8 focused tests for new views
    - Limit to 2-8 highly focused tests maximum
    - Test AboutView renders and wraps in Layout
    - Test DebugView renders and wraps in Layout
    - Test both views use depth=0
    - Skip exhaustive content testing (static placeholder content)
  - [ ] 4.2 Create AboutView component
    - New file: src/storytime/views/about_view.py
    - Use dataclass with site parameter
    - Implement __call__() -> Node pattern
    - Wrap content in Layout with view_title="About"
    - Set depth=0 for root-level view
    - Include static HTML placeholder content (project description)
  - [ ] 4.3 Create DebugView component
    - New file: src/storytime/views/debug_view.py
    - Use dataclass with site parameter
    - Implement __call__() -> Node pattern
    - Wrap content in Layout with view_title="Debug"
    - Set depth=0 for root-level view
    - Include static HTML placeholder content (debug info)
  - [ ] 4.4 Register /about route
    - Update route registration in application/ASGI app
    - Map /about URL to AboutView
    - Follow existing route pattern from site/section/subject views
    - Pass site instance to view
  - [ ] 4.5 Register /debug route
    - Update route registration in application/ASGI app
    - Map /debug URL to DebugView
    - Follow existing route pattern
    - Pass site instance to view
  - [ ] 4.6 Ensure new view tests pass
    - Run ONLY the 2-8 tests written in 4.1
    - Verify views render correctly
    - Verify Layout integration works
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 4.1 pass
- AboutView renders with Layout wrapper
- DebugView renders with Layout wrapper
- Both views accessible at /about and /debug routes
- Both views use depth=0

### Styling and Polish

#### Task Group 5: CSS Styling
**Dependencies:** Task Groups 1-4

- [ ] 5.0 Complete CSS styling
  - [ ] 5.1 Add custom layout styles to storytime.css
    - File: src/storytime/components/layout/static/storytime.css
    - Add grid layout spacing rules if needed
    - Add aside navigation spacing/indentation for hierarchy
    - Add breadcrumb inline layout styles if needed
    - Keep minimal - rely on PicoCSS defaults
    - Do NOT add responsive overrides (trust PicoCSS)
  - [ ] 5.2 Test visual rendering in browser
    - No automated tests for this sub-task
    - Manual verification only
    - Check header navigation alignment
    - Verify sidebar hierarchy indentation is clear
    - Verify breadcrumbs display inline with separators
    - Check footer placement and centering
  - [ ] 5.3 Verify responsive behavior
    - No automated tests for this sub-task
    - Manual verification only
    - Test on mobile viewport (320px-768px)
    - Test on tablet viewport (768px-1024px)
    - Test on desktop viewport (1024px+)
    - Trust PicoCSS defaults to handle layout changes
  - [ ] 5.4 Verify accessibility
    - No automated tests for this sub-task
    - Manual verification only
    - Check semantic HTML usage (header, nav, aside, main, article, footer)
    - Verify details/summary keyboard navigation works
    - Check breadcrumb navigation has proper ARIA labels
    - Ensure color contrast meets standards (trust PicoCSS defaults)

**Acceptance Criteria:**
- storytime.css contains minimal custom styles
- Visual hierarchy is clear in sidebar navigation
- Breadcrumbs display inline with readable separators
- Footer is centered and positioned at bottom
- Layout is responsive without custom media queries
- Semantic HTML and keyboard navigation work correctly

### Integration Testing

#### Task Group 6: End-to-End Testing and Gap Analysis
**Dependencies:** Task Groups 1-5

- [ ] 6.0 Review existing tests and fill critical gaps only
  - [ ] 6.1 Review tests from Task Groups 1-4
    - Review the 2-8 tests written for layout structure (Task 1.1)
    - Review the 2-8 tests written for sidebar navigation (Task 2.1)
    - Review the 2-8 tests written for breadcrumbs (Task 3.1)
    - Review the 2-8 tests written for new views (Task 4.1)
    - Total existing tests: approximately 8-32 tests
  - [ ] 6.2 Analyze test coverage gaps for THIS feature only
    - Identify critical user workflows lacking test coverage
    - Focus on integration between components (e.g., Layout + NavigationTree + Breadcrumbs)
    - Identify DOM interaction scenarios requiring pytest-playwright
    - Do NOT assess entire application test coverage
    - Prioritize end-to-end workflows over unit test gaps
  - [ ] 6.3 Write up to 10 additional strategic tests maximum
    - Add maximum of 10 new tests to fill identified critical gaps
    - Focus on playwright tests for DOM interactions:
      - Clicking collapsed section expands it
      - Clicking expanded section collapses it
      - Clicking nested subject expands/collapses correctly
      - Navigation links navigate to correct routes
      - Breadcrumb links navigate correctly
    - Mark all playwright tests with @pytest.mark.slow
    - Use pytest-playwright fixtures from conftest.py
    - Do NOT write comprehensive coverage for all scenarios
    - Skip edge cases unless business-critical
  - [ ] 6.4 Run feature-specific tests only
    - Run ONLY tests related to this spec's feature
    - Expected total: approximately 18-42 tests maximum
    - Do NOT run the entire application test suite
    - Verify critical workflows pass:
      - Layout renders with all new components
      - Navigation hierarchy expands/collapses correctly
      - Breadcrumbs navigate properly
      - New routes are accessible
  - [ ] 6.5 Verify all quality checks pass
    - Run: just test (for feature-specific tests)
    - Run: just typecheck (verify type hints are correct)
    - Run: just fmt (ensure code formatting is consistent)
    - All checks must pass before considering task complete

**Acceptance Criteria:**
- All feature-specific tests pass (approximately 18-42 tests total)
- Critical user workflows for this feature are covered
- No more than 10 additional tests added when filling in testing gaps
- DOM interaction tests use pytest-playwright and marked as @pytest.mark.slow
- All quality checks pass (test, typecheck, fmt)

## Execution Order

Recommended implementation sequence:

1. **Task Group 1: Core Layout Structure** (Foundation)
   - Update Layout component with new structure
   - Add header navigation and footer
   - Establish grid layout

2. **Task Group 2: Hierarchical Sidebar Navigation** (Critical component)
   - Create NavigationTree component
   - Implement three-level collapsible hierarchy
   - Integrate current_path logic

3. **Task Group 4: About and Debug Views** (Can run in parallel with TG2)
   - Create new view components
   - Register routes
   - (Independent of sidebar navigation)

4. **Task Group 3: Breadcrumb Navigation** (Depends on TG1 + TG2)
   - Create Breadcrumbs component
   - Implement path parsing and link generation
   - Integrate into Layout

5. **Task Group 5: CSS Styling** (Polish after functionality complete)
   - Add minimal custom styles
   - Manual visual verification
   - Responsive testing

6. **Task Group 6: Integration Testing** (Final validation)
   - Review all tests from previous groups
   - Add playwright tests for DOM interactions
   - Run quality checks

## Component File Structure

New files to create:
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/navigation_tree/__init__.py`
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/breadcrumbs/__init__.py`
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/views/about_view.py`
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/views/debug_view.py`

Modified files:
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/layout.py`
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/static/storytime.css`
- Application routing file (location TBD based on existing route registration pattern)

Test files to create/modify:
- `/Users/pauleveritt/projects/pauleveritt/storytime/tests/components/test_layout.py` (modify existing)
- `/Users/pauleveritt/projects/pauleveritt/storytime/tests/components/test_navigation_tree.py` (new)
- `/Users/pauleveritt/projects/pauleveritt/storytime/tests/components/test_breadcrumbs.py` (new)
- `/Users/pauleveritt/projects/pauleveritt/storytime/tests/views/test_about_view.py` (new)
- `/Users/pauleveritt/projects/pauleveritt/storytime/tests/views/test_debug_view.py` (new)
- `/Users/pauleveritt/projects/pauleveritt/storytime/tests/test_pico_layout_integration.py` (new, for playwright tests)

## Technical Notes

**Python Standards Compliance:**
- Use Python 3.14+ features throughout
- Structural pattern matching for current_path parsing
- Modern type hints: `str | None` instead of `Optional[str]`
- Type aliases using `type` statement if needed
- PEP 695 syntax for generic functions if applicable

**tdom Usage:**
- All components return `Node` type
- Use `html(t"...")` for template strings
- Leverage tdom's component composition with `<{Component} prop={value} />`
- Follow Fragment/Element patterns from existing components

**Testing Strategy:**
- Minimal tests during development (2-8 per task group)
- Use aria_testing utilities for DOM queries (existing pattern)
- pytest-playwright for DOM interactions (marked @pytest.mark.slow)
- Focus on behavior, not implementation
- Test core user flows only

**CSS Philosophy:**
- Minimal custom styles in storytime.css
- Trust PicoCSS framework for responsive behavior
- Use PicoCSS grid system and semantic HTML
- No custom media queries or breakpoints
- Follow PicoCSS documentation patterns

**URL Structure:**
- Home: /
- About: /about
- Debug: /debug
- Sections: /section/{name}/ (existing)
- Subjects: /section/{section}/subject/{name}/ (existing)
- Stories: /section/{section}/subject/{subject}/story/{name}.html (existing)

**current_path Format:**
- String format: "section/subject/story"
- Examples:
  - "getting-started" (section page)
  - "getting-started/installation" (subject page)
  - "getting-started/installation/quick-start" (story page)
- None for pages without hierarchy (home, about, debug)
