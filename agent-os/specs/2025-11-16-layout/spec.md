# Specification: Layout Component

## Goal

Create a shared Layout component that provides consistent HTML structure (html, head, body) for all views, with
configurable page titles and content insertion via a main element.

## User Stories

- As a developer, I want all views to share common HTML boilerplate so that pages have consistent structure
- As a developer, I want page titles to combine view-specific and site-wide titles so that browser tabs show meaningful
  information

## Specific Requirements

**Layout Component Signature**

- Create Layout as a dataclass in `src/storyville/components/layout/layout.py` (move from
  `components/layout/__init__.py`)
- Create a component test (aria-testing) in `components/layout/layout_test.py`
- Accept three parameters: `view_title: str | None`, `site: Site`, `children: Element | Fragment | None`
- Return type is `Node` via `__call__()` method
- Use modern Python type hints with PEP 604 union syntax

**HTML Structure Generation**

- Generate complete `<html>` document with proper `<head>` and `<body>` tags
- Include `<meta charset="utf-8">` and viewport meta tag in head
- Create `<title>` tag that concatenates view_title with site.title as: `{view_title} - {site.title}`
- When view_title is None, use only site.title (no hyphen)
- Link to stylesheet at `../static/bulma.css` in head
- Include navigation bar with site branding and menu items

**Content Placement**

- Insert children parameter content into `<main>` element within body
- Main element should be inside a Bulma columns layout (existing pattern)
- Preserve existing sidebar with SectionsListing component showing site sections
- Children content goes in the main column (not the sidebar column)

**Static Assets Organization**

- Move `src/storyville/static/` directory to `src/storyville/components/layout/static/`
- Move `bulma.css` file from old static location to new layout static location
- Update Layout's CSS link href to reference new static directory location
- Update Site model's `__post_init__` to look for static dir at new location (
  `PACKAGE_DIR / "components" / "layout" / "static"`)

**SiteView Integration**

- Update SiteView to wrap its content with Layout component
- Pass site object and appropriate view_title to Layout
- SiteView's current rendered content (div with h1 and section cards) becomes children parameter
- Use view_title of "Home" or similar for site index page

**SectionView Integration**

- Update SectionView to wrap its content with Layout component
- Pass section.title as view_title parameter
- Pass site object (needs to be accessible from section's parent chain)
- SectionView's current rendered content (div with h1, description, subjects) becomes children parameter

**SubjectView Integration**

- Update SubjectView to wrap its content with Layout component
- Pass subject.title as view_title parameter
- Pass site object (needs to be accessible from subject's parent chain)
- SubjectView's current rendered content (div with h1, target info, stories) becomes children parameter

**Type Safety**

- Import Element and Fragment from tdom package
- Use union type `Element | Fragment | None` for children parameter
- Maintain type guard patterns in tests (verify result is Element when needed)
- Ensure Layout satisfies View Protocol by implementing `__call__() -> Node`

**Component Reusability**

- Layout accesses site.items.values() to get sections for sidebar
- SectionsListing component remains imported and used in Layout
- Layout becomes the single source of truth for page structure
- All views delegate HTML wrapper to Layout, focusing only on their content

**Navigation and Links**

- Layout contains navbar with "Storyville" branding linking to "/"
- Navbar includes "Home" and "Components" navigation items
- Sidebar menu shows sections using existing SectionsListing component
- Views maintain their existing internal links (parent links, section links, etc.)

**Testing Requirements**

- Test that static asset paths (e.g., in `<link>` or `<img>` tags) in rendered pages point to valid destinations in `static` directory
- Verify that stylesheet links resolve correctly from pages at different path depths
- Ensure asset path resolution works for both site root pages and nested section/subject pages

## Visual Design

No visual mockups provided.

## Existing Code to Leverage

**Current Layout Component (src/storyville/components/layout/__init__.py)**

- Already defines dataclass with title, children, site parameters
- Contains complete HTML structure with navbar, sidebar, and main content area
- Uses tdom t-string templating for HTML generation
- Integrates SectionsListing component for sidebar navigation
- Should be moved to `layout.py` file and updated with new signature

**View Pattern (SiteView, SectionView, SubjectView)**

- All views are dataclasses implementing `__call__() -> Node`
- All use tdom html() function with t-string templates
- All return Node type satisfying View Protocol
- Tests verify results with `isinstance(result, Element)` type guards
- New Layout integration should wrap existing view content, not replace view logic

**Site Model Static Directory Discovery**

- Site.__post_init__ currently looks for static dir at `PACKAGE_DIR / "static"`
- Sets self.static_dir when directory exists
- build.py copies static_dir to output during build
- Update path to check `PACKAGE_DIR / "components" / "layout" / "static"`

**SectionsListing Component**

- Renders list of sections in sidebar menu
- Already imported and used in current Layout
- No changes needed to this component
- Continue using in new Layout implementation

**tdom Templating Pattern**

- Use `html(t'''...''')` for template strings
- Interpolate variables with `{variable_name}` syntax
- Interpolate components with `<{ComponentName} prop={value} />`
- Lists of elements can be interpolated directly with `{[items]}`

## Out of Scope

- Build-time copying of static assets to output directory (already implemented in build.py)
- Multiple layout variations or theming support
- Layout nesting capabilities for hierarchical page structures
- Navigation menu customization or dynamic menu generation
- Mobile-responsive navigation menu toggle functionality
- Footer component or footer content in layout
- Breadcrumb navigation beyond simple parent links
- SEO meta tags beyond basic charset and viewport
- Custom CSS or styling beyond Bulma framework
- JavaScript or interactive behavior in layout
