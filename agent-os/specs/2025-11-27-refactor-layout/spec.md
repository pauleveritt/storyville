# Specification: Refactor Layout Component with CSS Grid

## Goal
Refactor the Layout component to use modern CSS Grid layout with template areas instead of a simple grid div, and extract header, aside, main, and footer into standalone, reusable components.

## User Stories
- As a developer, I want Layout to use CSS Grid template areas so that the layout is more maintainable and follows modern CSS patterns
- As a developer, I want header, aside, main, and footer as separate components so that they can be reused, tested independently, and composed cleanly

## Specific Requirements

**Extract LayoutHeader Component**
- Create `components/header/header.py` with a `LayoutHeader` dataclass component
- Accept props: `site_title` (str), `depth` (int) for relative path calculation
- Return header element with container, hgroup with site branding, and nav with Home/About/Debug links
- Use relative path calculation for link hrefs based on depth
- Match current structure from lines 74-87 of layout.py

**Extract LayoutAside Component**
- Create `components/aside/aside.py` with a `LayoutAside` dataclass component
- Accept props: `sections` (dict[str, Section]), `current_path` (str | None), `cached_navigation` (str | None)
- Return aside element with "Sections" label and NavigationTree component
- Handle cached navigation HTML using Markup when provided, otherwise render NavigationTree fresh
- Match current structure from lines 89-92 of layout.py

**Extract LayoutMain Component**
- Create `components/main/main.py` with a `LayoutMain` dataclass component
- Accept props: `current_path` (str | None), `children` (Element | Fragment | Node | None)
- Return main element containing Breadcrumbs component and children content
- Match current structure from lines 93-96 of layout.py

**Extract LayoutFooter Component**
- Create `components/footer/footer.py` with a `LayoutFooter` dataclass component
- Accept props: `year` (str or int), optional `text` (str) for copyright message
- Return footer element with centered paragraph containing copyright text
- Default text should be "2025 Storytime" if not provided
- Match current structure from lines 98-100 of layout.py

**Update Layout Component Structure**
- Remove `<div class="grid">` wrapper from body
- Import all four new components: LayoutHeader, LayoutAside, LayoutMain, LayoutFooter
- Render as direct children of body: `<{LayoutHeader} />`, `<{LayoutAside} />`, `<{LayoutMain} />`, `<{LayoutFooter} />`
- Pass appropriate props to each component using calculated values (depth, static_prefix, etc.)
- Keep existing head section unchanged (meta tags, title, stylesheets, script)

**Implement CSS Grid with Template Areas**
- Update `storytime.css` to apply CSS Grid to body element
- Define grid-template-areas: "header header", "aside main", "footer footer"
- Set grid-template-columns: 250px 1fr (aside fixed width, main flexible)
- Set grid-template-rows: auto 1fr auto (header auto, content fills, footer auto)
- Apply grid-area properties to header, aside, main, footer elements
- Remove existing `body > div.grid` styles as they will no longer apply

**Responsive Grid Behavior**
- Add media query for mobile (max-width: 768px)
- Stack all areas vertically: "header", "aside", "main", "footer"
- Change grid-template-columns to 1fr (single column)
- Adjust aside positioning from sticky to static on mobile
- Ensure proper spacing and readability on small screens

**Component Type Signatures**
- All component `__call__` methods must return `Node` type
- Use dataclass with appropriate type hints for all props
- Follow pattern from PicoLayout reference: function-style components returning Node
- Import necessary types from tdom: Element, Fragment, Node, html

**Maintain Existing Functionality**
- Keep relative path calculation logic for static assets based on depth
- Preserve title concatenation (view_title + site.title or just site.title)
- Keep cached navigation optimization when provided
- Maintain current_path parameter for breadcrumb and navigation state
- Ensure all existing props work as before

## Visual Design

No visual mockups provided. The refactored layout should maintain the current visual appearance while using a cleaner CSS Grid implementation underneath.

## Existing Code to Leverage

**PicoLayout from tdom-sphinx**
- Shows pattern of importing separate components (Head, PicoHeader, Footer, PageAside, SiteAside)
- Demonstrates component invocation syntax: `<{ComponentName} prop1={value1} prop2={value2} />`
- Uses function-style components that accept keyword arguments and return Node
- Provides example of clean composition in body element

**PicoHeader component**
- Demonstrates dataclass-free function component pattern with keyword arguments
- Shows header structure with container, branding, and navigation
- Illustrates how to calculate and use relative paths
- Pattern for building navigation links dynamically

**SiteAside component**
- Shows aside element with role="complementary" and aria-label
- Demonstrates header within aside with title and close button
- Uses sticky nav with class="is-sticky-above-lg"
- Renders navigation tree using details/summary pattern

**Footer component**
- Simple footer pattern with container and section
- Shows navigation links structure in footer
- Uses datetime.now().year for current year

**Breadcrumbs component**
- Already exists and works correctly
- Uses dataclass pattern with `__call__` returning Node
- Accepts current_path as optional parameter
- Import from storytime.components.breadcrumbs

## Out of Scope
- Changing the content or visual appearance of header, aside, main, or footer elements
- Adding new navigation links or features
- Implementing a theming system
- Adding JavaScript interactivity to components
- Mobile hamburger menu or drawer patterns
- Advanced responsive breakpoints beyond mobile/desktop
- Performance optimizations beyond cached navigation
- Accessibility improvements beyond maintaining current aria labels
- Component testing frameworks or visual regression tests
- Documentation or README files for the components
