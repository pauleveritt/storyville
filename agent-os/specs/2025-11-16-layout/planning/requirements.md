# Spec Requirements: Layout

## Initial Description
Layout. All the views should use a common component called components/layout. This layout wraps the contents of that view, providing the full `<html>`, `<head>`, and `<body>`. The contents of the view should go in `<main>` in the layout. The view should pass a prop to the layout for what to put in the `<title>`, which will concat with the Site.title such as `<title>{view_title} - {self.title}</title>`.

Layouts will also have an `assets` directory. This asset directory should be copied to the root of the output directory during building, which we will do in the next feature.

## Requirements Discussion

### First Round Questions

**Q1:** Should the Layout component be named "Layout" or "LayoutView"?
**Answer:** Just "Layout" (not "LayoutView")

**Q2:** For the children parameter that contains view content going into `<main>`, should Layout accept:
- Option A: `children: str` (simple string of HTML)
- Option B: `children: Element | Fragment | None` (tdom types for type safety)
- Option C: `children: Node` (broader tdom type)
**Answer:** Option B: `Element | Fragment | None`

**Q3:** Where should the Layout component live?
- Option A: `storyville/components/layout/__init__.py` (as a module)
- Option B: `storyville/components/layout.py` (as a single file)
**Answer:** Move from current location at `components/layout/__init__.py` to `components/layout.py`

**Q4:** The layout will need access to the Site object to get `site.title`. Should Layout accept a `site` prop explicitly?
**Answer:** Yes, Layout accepts both `view_title` prop and `site` prop

**Q5:** How should Layout handle the title when view_title is None?
**Answer:** Handle None sensibly (implementation detail for spec-writer to determine best practice)

**Q6:** For the static assets directory, should we:
- Option A: Keep using `storyville.static` as currently exists
- Option B: Move to `storyville.components.layout.static` for better organization
**Answer:** Option B - move from `storyville.static` to `storyville.components.layout.static` and move `bulma.css` there

**Q7:** Should we implement the build-time copying of static assets to output directory in this spec?
**Answer:** No, OUT OF SCOPE for this spec. Only create the static directory structure. The build-time copying logic comes in the next feature.

**Q8:** Which views need to be updated to use the new Layout component?
**Answer:** SiteView, SectionView, and SubjectView should all send `children` to Layout, which inserts them in `<main>`

**Q9:** Are there plans for multiple layouts or layout nesting?
**Answer:** Future consideration, ignore for now. This spec focuses on a single shared Layout component.

### Existing Code to Reference

**Similar Features Identified:**
No similar existing features identified for reference. This is a new foundational component.

### Follow-up Questions
No follow-up questions were necessary.

## Visual Assets

### Files Provided:
No visual files found.

### Visual Insights:
No visual assets provided.

## Requirements Summary

### Functional Requirements
- Create a Layout component at `storyville/components/layout.py`
- Layout provides full `<html>`, `<head>`, and `<body>` structure
- Layout accepts two props:
  - `view_title: str | None` - the view-specific title
  - `site: Site` - the site object for accessing site.title
- Layout creates title tag: `<title>{view_title} - {site.title}</title>` with sensible None handling
- Layout accepts `children: Element | Fragment | None` parameter
- Layout inserts children content into `<main>` element
- Update SiteView, SectionView, and SubjectView to use Layout component
- Views pass their content as `children` to Layout
- Move static directory from `storyville.static` to `storyville.components.layout.static`
- Move `bulma.css` file to new static directory location
- Create proper static directory structure for layouts

### Reusability Opportunities
No reusability opportunities identified. This is a foundational component that other views will consume.

### Scope Boundaries

**In Scope:**
- Creating Layout component with proper type hints
- Updating all three views (SiteView, SectionView, SubjectView) to use Layout
- Moving and organizing static assets directory
- Setting up static directory structure
- Title concatenation with site title
- Handling None for view_title parameter

**Out of Scope:**
- Build-time copying of static assets to output directory (next feature)
- Multiple layout support or layout variations
- Layout nesting capabilities
- Any layout themes or customization beyond single shared layout

### Technical Considerations
- Use modern Python type hints: `Element | Fragment | None` (PEP 604 union syntax)
- Leverage tdom templating for component structure
- Follow existing Storyville component patterns
- Maintain type safety throughout component and view updates
- Static assets organization supports future build-time copying feature
- Component signature: `Layout(view_title: str | None, site: Site, children: Element | Fragment | None)`

## Product Context

### Alignment with Product Mission
This Layout component aligns with Storyville's mission of component-driven development by:
- Establishing a reusable, framework-independent layout component
- Following the pattern of building composable UI components
- Demonstrating tdom-based component composition
- Supporting the visual catalog browser feature from the roadmap

### Roadmap Integration
This feature supports roadmap item #3 (Web-Based Component Browser) by providing the HTML structure that wraps the component catalog views. It establishes the foundation for consistent page layouts across the browsing experience.

### Tech Stack Compliance
- Uses tdom templating engine as specified
- Follows Python 3.14+ standards with modern type hints
- Uses PEP 604 union syntax (`Element | Fragment | None`)
- Maintains framework-independent core architecture
- Organizes code following `src/storyville/` structure
