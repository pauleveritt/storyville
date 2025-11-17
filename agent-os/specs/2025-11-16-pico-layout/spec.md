# Specification: Pico Layout

## Goal
Redesign the Layout component to match PicoCSS documentation structure with hierarchical navigation, breadcrumbs, and new About/Debug views.

## User Stories
- As a site visitor, I want to see a hierarchical navigation sidebar so that I can browse sections, subjects, and stories efficiently
- As a developer, I want collapsible navigation that auto-expands to show the current page so that users maintain context while navigating

## Specific Requirements

**Header Navigation**
- Place top navigation in `<header>` element with Home, About, and Debug links
- Home link navigates to site root (/)
- About link navigates to /about route pointing to AboutView
- Debug link navigates to /debug route pointing to DebugView
- Use existing PicoCSS nav structure with `<ul>` lists for alignment

**Left Sidebar Tree Navigation**
- Implement three-level hierarchy in `<aside>`: Sections (collapsible) > Subjects (collapsible) > Stories (links)
- Use HTML `<details>` and `<summary>` elements for JavaScript-free collapse/expand
- Sections are top-level `<details>` containing subjects
- Subjects are nested `<details>` inside sections containing story links
- Stories are simple `<li><a>` items (not collapsible)
- All details elements closed by default except those in the current path
- Auto-expand mechanism controlled by current_path parameter

**Current Path Detection**
- Layout accepts current_path string parameter (format: "section/subject/story")
- Parse path to determine which `<details>` elements receive `open` attribute
- Section details get `open` if current_path starts with section name
- Subject details get `open` if current_path matches section/subject pattern
- Use this mechanism for both sidebar expansion and breadcrumb generation

**Breadcrumb Navigation**
- Place breadcrumbs between sidebar and main content showing Home > Section > Subject > Story
- Generate from current_path parameter by splitting on "/" separator
- Render each level as clickable link except current page (plain text)
- Use " > " as separator between breadcrumb items
- Apply default link styling without custom overrides

**Main Content Area**
- Render main content in `<article>` element within grid layout
- Accept children parameter (Element | Fragment | Node | None) for view content
- Maintain depth parameter for static asset path calculation
- Keep existing pattern where views wrap themselves in Layout

**Footer**
- Add `<footer>` element with simple copyright text: "2025 Storytime"
- Place footer at bottom of page layout
- Use centered text alignment with default styling

**AboutView Route**
- Create new AboutView at /about with static HTML content
- Wrap content in Layout component
- Include basic project information as placeholder
- Use depth=0 for root-level view

**DebugView Route**
- Create new DebugView at /debug with static HTML content
- Wrap content in Layout component
- Show debug information as placeholder (can be enhanced later)
- Use depth=0 for root-level view

**CSS Organization**
- Add all custom layout styling to existing storytime.css file
- Use PicoCSS grid system for header/aside/main/footer layout
- Preserve existing pico-docs.css import (already available)
- Do not create additional CSS files
- Follow PicoCSS patterns for spacing and semantic HTML styling

**Responsive Behavior**
- Rely on PicoCSS responsive defaults without custom overrides
- Do not add media queries or breakpoint-specific styles
- Trust framework to handle mobile/tablet layout transformations

## Visual Design

**Reference: https://picocss.com/docs/group**
- Clean documentation layout with sidebar navigation on left
- Main content area on right with clear typography hierarchy
- Top navigation bar with project branding and utility links
- Collapsible tree structure using details/summary elements
- Minimal, semantic HTML structure matching PicoCSS philosophy
- Active navigation states highlighted automatically by framework
- Breadcrumb trail showing current location in hierarchy
- Footer with minimal metadata and links

## Existing Code to Leverage

**Layout Component (`src/storytime/components/layout/layout.py`)**
- Reuse existing Layout dataclass structure with view_title, site, children, depth parameters
- Keep title concatenation logic: "{view_title} - {site.title}"
- Preserve static asset path calculation using depth (e.g., "../static/" at depth 0)
- Maintain existing CSS file imports: pico-main.css, pico-docs.css, storytime.css
- Follow pattern where views self-wrap in Layout component

**SectionsListing Component (`src/storytime/components/sections_listing/__init__.py`)**
- Reference existing pattern of rendering sections as list items
- Adapt list comprehension approach for nested details/summary structure
- Use similar dataclass structure for new sidebar navigation component
- Follow tdom html template string (t"") pattern for markup generation

**Site/Section/Subject Models**
- Use existing Site.items dict containing Section instances keyed by name
- Use Section.items dict containing Subject instances keyed by name
- Use Subject.items list containing Story instances
- Leverage parent relationships for path construction
- Access title and description attributes from all node types

**View Pattern (SiteView, SectionView, SubjectView)**
- Follow dataclass structure with __call__() -> Node return type
- Use tdom html t-string templates for markup
- Pass depth parameter based on view level (Site=0, Section=1, Subject=2)
- Use existing URL pattern: sections as /section/{key}, subjects as relative {key}

**CSS Files (`src/storytime/components/layout/static/`)**
- storytime.css currently empty, ready for custom layout styles
- pico-docs.css already imported with PicoCSS documentation styles
- pico-main.css provides base framework styling

## Out of Scope
- Version selector dropdown functionality
- Search/filter functionality in sidebar navigation
- Theme switcher or dark mode toggle
- Social media links or external service integrations
- Three-level collapsible nesting (stories remain as simple links only)
- Custom responsive breakpoints or mobile-specific overrides
- JavaScript-based interactions or dynamic state management
- Additional footer links beyond copyright text
- User authentication or personalized navigation states
- Keyboard navigation enhancements beyond browser defaults
