# Task Breakdown: Refactor Layout Component with CSS Grid

## Overview
Total Tasks: 23 (organized into 4 task groups)

This refactoring will extract 4 components from the monolithic Layout component (LayoutHeader, LayoutAside, LayoutMain, LayoutFooter), update Layout to compose these components, and implement CSS Grid with template areas for a cleaner, more maintainable layout structure.

## Task List

### Component Extraction Layer

#### Task Group 1: Extract and Test Layout Sub-Components
**Dependencies:** None

- [ ] 1.0 Complete component extraction
  - [ ] 1.1 Write 2-8 focused tests for extracted components
    - Test LayoutHeader renders with site_title and depth props
    - Test LayoutHeader generates correct relative paths at different depths
    - Test LayoutAside handles cached_navigation HTML using Markup
    - Test LayoutAside renders NavigationTree when no cached navigation provided
    - Test LayoutMain renders children and Breadcrumbs
    - Test LayoutFooter renders with year and optional text props
    - Skip exhaustive edge case testing at this stage
  - [ ] 1.2 Create LayoutHeader component at `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/layout_header.py`
    - Use `@dataclass` decorator
    - Props: `site_title: str`, `depth: int = 0`
    - Calculate relative paths using `"../" * (depth + 1)` pattern
    - Return `<header>` with container, hgroup, and nav elements
    - Include Home, About, Debug navigation links
    - Follow pattern from layout.py lines 74-87
    - Import necessary types: `Node`, `html` from tdom
  - [ ] 1.3 Create LayoutAside component at `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/layout_aside.py`
    - Use `@dataclass` decorator
    - Props: `sections: dict[str, Section]`, `current_path: str | None = None`, `cached_navigation: str | None = None`
    - Return `<aside>` with "Sections" label
    - If cached_navigation provided, use `Markup(cached_navigation)`
    - Otherwise render `NavigationTree(sections=sections, current_path=current_path)()`
    - Follow pattern from layout.py lines 89-92 and 50-58
    - Import: `Node`, `html` from tdom; `Section` from storytime.section.models; `NavigationTree` from storytime.components.navigation_tree
    - Import `Markup` from markupsafe conditionally when needed
  - [ ] 1.4 Create LayoutMain component at `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/layout_main.py`
    - Use `@dataclass` decorator
    - Props: `current_path: str | None = None`, `children: Element | Fragment | Node | None = None`
    - Return `<main>` containing Breadcrumbs component and children
    - Follow pattern from layout.py lines 93-96
    - Import: `Element`, `Fragment`, `Node`, `html` from tdom; `Breadcrumbs` from storytime.components.breadcrumbs
  - [ ] 1.5 Create LayoutFooter component at `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/layout_footer.py`
    - Use `@dataclass` decorator
    - Props: `year: str | int = 2025`, `text: str = "Storytime"`
    - Return `<footer>` with centered paragraph containing `{year} {text}`
    - Follow pattern from layout.py lines 98-100
    - Import: `Node`, `html` from tdom
  - [ ] 1.6 Ensure component-level tests pass
    - Run ONLY the 2-8 tests written in 1.1
    - Command: `just test /Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/layout_header_test.py`
    - Command: `just test /Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/layout_aside_test.py`
    - Command: `just test /Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/layout_main_test.py`
    - Command: `just test /Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/layout_footer_test.py`
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 1.1 pass
- All four component files created with proper dataclass structure
- Components return `Node` type from `__call__` method
- Components match current Layout structure exactly
- Type hints use modern Python 3.14+ syntax

### Integration Layer

#### Task Group 2: Update Layout Component to Use Extracted Components
**Dependencies:** Task Group 1

- [ ] 2.0 Complete Layout component refactoring
  - [ ] 2.1 Write 2-8 focused integration tests
    - Test Layout renders all four components (header, aside, main, footer)
    - Test Layout passes correct props to each component
    - Test Layout preserves existing functionality (title logic, depth calculation, cached navigation)
    - Test Layout body structure no longer has `<div class="grid">` wrapper
    - Test components are direct children of body element
    - Skip redundant testing of component internals already tested in Group 1
  - [ ] 2.2 Update Layout component at `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/layout.py`
    - Add imports: `from storytime.components.layout.layout_header import LayoutHeader`
    - Add imports: `from storytime.components.layout.layout_aside import LayoutAside`
    - Add imports: `from storytime.components.layout.layout_main import LayoutMain`
    - Add imports: `from storytime.components.layout.layout_footer import LayoutFooter`
    - Keep existing imports for Site, Element, Fragment, Node, html
    - Remove direct imports of Breadcrumbs and NavigationTree (now used by sub-components)
    - Remove `<div class="grid">` wrapper from body
    - Replace inline header HTML with `<{LayoutHeader} site_title={self.site.title} depth={self.depth} />`
    - Replace inline aside HTML with `<{LayoutAside} sections={self.site.items} current_path={self.current_path} cached_navigation={self.cached_navigation} />`
    - Replace inline main HTML with `<{LayoutMain} current_path={self.current_path} children={self.children} />`
    - Replace inline footer HTML with `<{LayoutFooter} year={2025} text={"Storytime"} />`
    - Keep head section unchanged (meta tags, title, stylesheets, script)
    - Preserve title_text concatenation logic
    - Preserve static_prefix calculation logic (used in head)
    - Remove navigation_html variable (moved to LayoutAside)
  - [ ] 2.3 Ensure Layout integration tests pass
    - Run ONLY the 2-8 tests written in 2.1
    - Command: `just test /Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/layout_integration_test.py`
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 2.1 pass
- Layout component successfully composes all four sub-components
- Layout renders components as direct children of body (no grid div wrapper)
- All existing Layout props still work (view_title, site, children, depth, current_path, cached_navigation)
- Layout maintains same external API and behavior

### CSS Grid Implementation Layer

#### Task Group 3: Implement CSS Grid with Template Areas
**Dependencies:** Task Group 2

- [ ] 3.0 Complete CSS Grid implementation
  - [ ] 3.1 Write 2-8 focused visual/structural tests
    - Test body element has CSS Grid applied (check for grid display in rendered output)
    - Test header, aside, main, footer elements exist as direct children of body
    - Test grid template areas structure is correct
    - Test responsive behavior on mobile (single column stack)
    - Skip pixel-perfect visual testing or screenshot comparison
  - [ ] 3.2 Update storytime.css at `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/static/storytime.css`
    - Remove existing `body > div.grid` styles (lines 11-17)
    - Add CSS Grid to body element:
      ```css
      body {
        display: grid;
        grid-template-areas:
          "header header"
          "aside main"
          "footer footer";
        grid-template-columns: 11rem 1fr;
        grid-template-rows: auto 1fr auto;
        column-gap: 3rem;
        row-gap: 2rem;
        align-items: start;
      }
      ```
    - Add grid-area to header: `header { grid-area: header; }`
    - Add grid-area to aside: `aside { grid-area: aside; }`
    - Add grid-area to main: `main { grid-area: main; }`
    - Add grid-area to footer: `footer { grid-area: footer; }`
    - Update aside positioning from `body > div.grid > aside` to just `aside`
    - Keep aside sticky positioning: `position: sticky; top: calc(...);`
    - Keep aside overflow: `max-height: calc(...); overflow-y: auto;`
  - [ ] 3.3 Implement responsive mobile layout
    - Update `@media (max-width: 768px)` section
    - Remove `body > div.grid` mobile styles
    - Add mobile body styles:
      ```css
      body {
        grid-template-areas:
          "header"
          "aside"
          "main"
          "footer";
        grid-template-columns: 1fr;
      }
      ```
    - Update aside mobile positioning from `body > div.grid > aside` to just `aside`
    - Keep aside mobile behavior: `position: static; max-height: none;`
  - [ ] 3.4 Ensure CSS Grid tests pass
    - Run ONLY the 2-8 tests written in 3.1
    - Verify layout visually in browser if needed
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 3.1 pass
- CSS Grid applied to body element with template areas
- Header spans full width at top
- Aside fixed at 11rem width, main flexible (1fr)
- Footer spans full width at bottom
- Mobile responsive: stacks vertically with single column
- Visual appearance matches original layout

### Testing and Validation Layer

#### Task Group 4: Test Review and Quality Checks
**Dependencies:** Task Groups 1-3

- [ ] 4.0 Review existing tests and validate refactoring
  - [ ] 4.1 Review tests from Task Groups 1-3
    - Review the 2-8 tests written for component extraction (Task 1.1)
    - Review the 2-8 tests written for Layout integration (Task 2.1)
    - Review the 2-8 tests written for CSS Grid (Task 3.1)
    - Total existing tests: approximately 6-24 tests
  - [ ] 4.2 Run existing Layout tests to verify backward compatibility
    - Run all tests in `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/layout_test.py`
    - These tests cover the original Layout behavior and should still pass
    - Expected: All existing tests pass without modification
    - Fix any breaking changes to maintain API compatibility
  - [ ] 4.3 Analyze test coverage gaps for this refactoring only
    - Identify critical workflows that lack coverage (e.g., depth calculation edge cases, cached navigation with None sections)
    - Focus ONLY on gaps related to the Layout refactoring
    - Prioritize integration workflows over unit test gaps
    - Do NOT assess entire application test coverage
  - [ ] 4.4 Write up to 10 additional strategic tests maximum
    - Add maximum of 10 new tests to fill identified critical gaps
    - Focus on component composition and integration points
    - Test edge cases: None children, empty sections dict, depth boundary values
    - Test cached_navigation integration with LayoutAside
    - Do NOT write comprehensive coverage for all scenarios
    - Skip visual regression tests
  - [ ] 4.5 Run feature-specific tests only
    - Run all Layout component tests: `just test /Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/`
    - Expected total: approximately 16-34 tests plus existing layout_test.py tests
    - Verify all tests pass
    - Do NOT run the entire application test suite yet
  - [ ] 4.6 Run full quality checks per CLAUDE.md
    - Run full test suite: `just test`
    - Run type checking: `just typecheck`
    - Run formatting: `just fmt`
    - All checks must pass
    - Fix any issues that arise
  - [ ] 4.7 Verify CSS file is copied to var/static/
    - Check that updated storytime.css exists at `/Users/pauleveritt/projects/pauleveritt/storytime/var/static/storytime.css`
    - Ensure changes are reflected in the built output
    - Run build command if necessary to copy static assets

**Acceptance Criteria:**
- All feature-specific tests pass (approximately 16-34 new tests total)
- All existing Layout tests continue to pass
- No more than 10 additional tests added when filling in testing gaps
- Full test suite passes (`just test`)
- Type checking passes (`just typecheck`)
- Code formatting passes (`just fmt`)
- CSS Grid applied correctly and visible in built output

## Execution Order

Recommended implementation sequence:
1. Component Extraction Layer (Task Group 1) - Extract LayoutHeader, LayoutAside, LayoutMain, LayoutFooter
2. Integration Layer (Task Group 2) - Update Layout to compose extracted components
3. CSS Grid Implementation (Task Group 3) - Remove div.grid wrapper and implement CSS Grid
4. Testing and Validation (Task Group 4) - Verify backward compatibility and run quality checks

## Implementation Notes

**File Locations:**
- New components: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/`
- Component test files: Same directory as components, named `{component}_test.py`
- CSS file: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/static/storytime.css`
- Built CSS: `/Users/pauleveritt/projects/pauleveritt/storytime/var/static/storytime.css`

**Type Hints:**
- Use modern Python 3.14+ syntax: `str | None` instead of `Union[str, None]`
- Use built-in generics: `dict[str, Section]` instead of `Dict[str, Section]`
- All component `__call__` methods must return `Node` type

**Testing Strategy:**
- Write 2-8 focused tests per task group during development
- Run only newly written tests after each task group completion
- Run all Layout tests after integration (Task Group 2)
- Run full test suite only in final validation (Task Group 4)
- Maximum 10 additional tests when filling gaps in Task Group 4

**CSS Grid Strategy:**
- Remove `<div class="grid">` wrapper in Layout component first
- Update CSS to target body element directly
- Maintain visual appearance using grid-template-areas
- Preserve responsive behavior for mobile devices
- Keep aside sticky positioning and overflow behavior

**Preservation Requirements:**
- All existing Layout props must continue to work
- Title concatenation logic must remain unchanged
- Relative path calculation (depth) must work correctly
- Cached navigation optimization must be preserved
- Breadcrumbs and NavigationTree integration must work
- All existing tests in layout_test.py must pass without modification
