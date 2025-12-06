# Spec Requirements: Pico Layout

## Initial Description

Using the page at https://picocss.com/docs/group as a guide, implement a layout in Layout that matches this look:
- Navigation at the top in <header>
- Left aside that shows the tree of sections, subjects, and stories
    - All menus are collapsed
    - Except the current node
    - Do this without JavaScript
    - See the `<aside>` below for a PicoCSS example that doesn't need JS for collapse/expand
- In the middle a breadcrumbs area with the path to the current view
- The <main> area that shows the current view
- A footer with a copyright
- Put custom styling in storyville.css
- We already have the CSS from that site in pico-docs.css
- Use pytest-playwright for tests that require DOM interaction such as clicking
- But mark these tests as slow

Example aside structure provided:
```html
<aside>
  <nav>
    <details>
      <summary>Section 1</summary>
      <ul>
        <li><a href="#link1">Link 1</a></li>
        <li><a href="#link2">Link 2</a></li>
        <li><a href="#link3">Link 3</a></li>
      </ul>
    </details>
    <details>
      <summary>Section 2</summary>
      <ul>
        <li><a href="#link4">Link 4</a></li>
        <li><a href="#link5">Link 5</a></li>
      </ul>
    </details>
    <details open>
      <summary>Section 3 (Open by default)</summary>
      <ul>
        <li><a href="#link6">Link 6</a></li>
        <li><a href="#link7">Link 7</a></li>
      </ul>
    </details>
  </nav>
</aside>
```

## Requirements Discussion

### First Round Questions

**Q1: Navigation Links - What should the header navigation links do?**
I'm assuming the header navigation should include links like "Home", "About", "Debug" as simple anchor tags. Should these:
- Link to actual routes we need to create (AboutView, DebugView, etc.)?
- Or just be placeholder links for now with href="#"?

**Answer:** Yes, create new routes for "About" and "Debug", pointed to an AboutView and a DebugView. For now just have static HTML in there, but wrap in the Layout.

**Q2: Collapsible Tree Nesting - How deep does the hierarchy go?**
Based on the raw idea, the left aside shows "sections, subjects, and stories". I'm assuming:
- Sections are top-level `<details>` elements
- Subjects are nested `<details>` inside sections
- Stories are `<li><a>` items inside subjects

Is this correct, or are stories also collapsible (three levels of nesting)?

**Answer:** Stories are not collapsible (just simple `<li><a>` items).

**Q3: Current Node Parameter - How is "current node" determined?**
For the logic "all menus are collapsed except the current node", I'm thinking the Layout component should:
- Accept a `current_path` parameter (e.g., "section1/subject2/story3")
- Parse this to determine which `<details>` elements should have the `open` attribute

Should we use a path string like that, or would you prefer passing section/subject/story objects?

**Answer:** Try a path string first.

**Q4: Breadcrumb Styling - What styling should breadcrumbs use?**
For the breadcrumbs area, I'm assuming we should:
- Use simple link elements separated by " > " or " / "
- Style them as inline elements with default link colors
- Make the current page non-clickable (just text, not a link)

Do you have a preference for the separator or styling approach?

**Answer:** Default link styling with `>` as separator.

**Q5: CSS Organization - Where should custom styles go?**
You mentioned putting custom styling in storyville.css and that pico-docs.css already exists. I'm thinking:
- storyville.css for layout-specific overrides (grid layout, spacing, breadcrumb formatting)
- Keep pico-docs.css as-is since it's imported from PicoCSS docs

Should we create any additional CSS modules or keep everything in storyville.css?

**Answer:** Keep everything in storyville.css.

**Q6: Playwright Tests - What interactions should we test?**
For the pytest-playwright tests marked as slow, I'm assuming we should test:
- Clicking a collapsed section expands it
- Clicking an expanded section collapses it
- Navigation links work correctly
- Breadcrumb links navigate properly

Are there other DOM interactions you want covered, or should we skip any of these?

**Answer:** Test all of those interactions.

**Q7: Responsive Behavior - Should the layout adapt for mobile?**
Looking at the PicoCSS docs reference, I'm thinking:
- Keep desktop layout as-is (header top, aside left, main center)
- For mobile, should the aside become a collapsible menu or stay visible but stacked?

What's your preference for mobile/tablet viewports?

**Answer:** Follow PicoCSS responsive defaults for now, don't override.

**Q8: Footer Content - What goes in the footer?**
You mentioned "a footer with a copyright". Should it be:
- Simple centered text like "© 2025 Storyville"
- Or include additional links (Privacy, Terms, GitHub, etc.)?

**Answer:** Just simple copyright text for now.

**Q9: Out of Scope - Anything we should explicitly NOT include?**
Are there features from the PicoCSS docs page we should skip for this implementation? For example:
- Version selector dropdown
- Search functionality
- Theme switcher
- Social media links

What should we leave out of this initial implementation?

**Answer:** Skip all of those - just focus on the core layout structure.

### Existing Code to Reference

**Similar Features Identified:**
No existing navigation or tree rendering components to match.

## Visual Assets

### Files Provided:
No visual files found in the visuals folder.

### Design Reference:
User referenced the PicoCSS documentation page at https://picocss.com/docs/group as the design guide.

### Visual Insights from Referenced Page:

**Page Layout:**
- Sidebar on the left with hierarchical documentation navigation
- Main content area on the right with detailed component documentation
- Top navigation bar with version selector and external links
- Footer with additional site links and metadata

**Navigation Patterns:**
- Sidebar uses a nested, tree-like structure
- Organized into logical sections: "Getting Started", "Customization", "Layout", etc.
- Active/current section highlighted
- Semantic grouping of related documentation topics

**Breadcrumb/Navigation:**
- Minimal breadcrumb implementation
- Current page shown at top of main content area
- Inline section anchors for quick navigation

**Responsive Considerations:**
- Mobile behavior for components
- Flexible layout suggesting responsive design
- Compact navigation structure

**Visual Hierarchy:**
- Clear typographic differentiation between headings and content
- Code examples prominently displayed
- Consistent spacing and alignment

**Link Styling:**
- Minimal, clean link presentation
- External links clearly differentiated
- Inline code and documentation links

**Design Philosophy:**
- Emphasizes clarity and semantic structure
- Developer-friendly documentation presentation
- Clean, minimal aesthetic

## Requirements Summary

### Functional Requirements

**Layout Structure:**
- **Header**: Top navigation with links to Home, About, and Debug routes
- **Left Aside**: Collapsible tree showing sections, subjects, and stories
  - Two-level hierarchy: Sections contain subjects (collapsible), subjects contain stories (simple links)
  - Use HTML `<details>` and `<summary>` elements for collapse/expand without JavaScript
  - Automatically expand the section/subject containing the current page
  - All other sections/subjects collapsed by default
- **Breadcrumbs Area**: Path display showing navigation from root to current page
  - Format: Home > Section > Subject > Story
  - Links for all levels except current page (plain text)
  - Separator: " > "
  - Default link styling
- **Main Content**: Area for rendering the current view (HomePage, AboutView, DebugView, etc.)
- **Footer**: Simple copyright text (e.g., "© 2025 Storyville")

**New Routes to Create:**
- AboutView route at `/about`
  - Static HTML content
  - Wrapped in Layout component
- DebugView route at `/debug`
  - Static HTML content
  - Wrapped in Layout component

**Current Node Detection:**
- Layout accepts a `current_path` parameter (string format, e.g., "section1/subject2/story3")
- Parse the path to determine which `<details>` elements should have `open` attribute
- Use this for both aside expansion and breadcrumb generation

**Breadcrumb Generation Logic:**
- Parse `current_path` string to extract hierarchy levels
- Generate clickable links for each ancestor level
- Current page rendered as plain text (non-clickable)
- Use " > " as separator between levels

### Reusability Opportunities
No similar existing features identified for reference.

### Scope Boundaries

**In Scope:**
- Core layout structure (header, aside, breadcrumbs, main, footer)
- Header navigation with Home, About, Debug links
- AboutView and DebugView routes with static content
- Two-level collapsible tree (sections > subjects > stories)
- CSS-only collapse/expand using `<details>` elements
- Auto-expansion of current node's hierarchy
- Breadcrumb generation from current_path
- Custom styling in storyville.css
- Playwright tests for DOM interactions (marked as slow)
- Following PicoCSS responsive defaults

**Out of Scope:**
- Version selector dropdown
- Search functionality
- Theme switcher
- Social media links
- Three-level nesting (stories are not collapsible)
- Custom responsive overrides (use PicoCSS defaults)
- Additional footer links beyond copyright
- JavaScript-based interactions

### Technical Considerations

**CSS Organization:**
- Use existing pico-docs.css (already imported from PicoCSS docs)
- Add custom styling to storyville.css for:
  - Grid layout structure
  - Spacing and positioning
  - Breadcrumb formatting
  - Any layout-specific overrides
- Do not create additional CSS modules

**Testing Strategy:**
- Use pytest-playwright for DOM interaction tests
- Mark all playwright tests as slow
- Test coverage should include:
  - Clicking collapsed sections expands them
  - Clicking expanded sections collapses them
  - Navigation links work correctly
  - Breadcrumb links navigate properly
  - Current node auto-expansion works
  - Footer renders correctly

**Responsive Behavior:**
- Follow PicoCSS responsive defaults
- Do not add custom responsive overrides
- Trust PicoCSS framework to handle mobile/tablet layouts

**HTML Structure:**
- Use semantic HTML5 elements
- Leverage `<details>` and `<summary>` for JavaScript-free collapse/expand
- Use `<nav>` for navigation areas
- Maintain accessibility with proper heading hierarchy and ARIA attributes where needed

**Integration Points:**
- Layout component should be reusable across all views
- current_path parameter passed from route handlers
- Static views (About, Debug) wrapped in Layout
- Existing CSS framework (PicoCSS) must be preserved
