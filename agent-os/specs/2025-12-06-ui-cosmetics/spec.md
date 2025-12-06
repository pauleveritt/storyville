# Specification: UI Cosmetics

## Goal
Enhance visual aesthetics and user experience by improving background colors, integrating FontAwesome icons, adding a collapsible sidebar with persistent state, and implementing automatic navigation tree expansion based on the current URL.

## User Stories
- As a user, I want a softer main area background color so that the interface is less harsh on the eyes during extended use
- As a user, I want to toggle the sidebar to maximize screen space for content when needed, with my preference remembered across page loads
- As a user, I want the navigation tree to automatically expand to show my current location so that I can easily understand where I am in the documentation hierarchy

## Specific Requirements

**Main Area Background Color**
- Use Pico CSS variable `--pico-card-background-color` for the main element background (already defined in Pico CSS as a gray-ish color in dark mode)
- Apply background color to the `<main>` element in the CSS
- Ensure color provides good contrast with existing text colors
- Maintain consistency with Pico CSS theming system

**FontAwesome Integration**
- Install `@fortawesome/fontawesome-free` package via npm as a dependency
- Use web fonts approach (CSS + font files) rather than SVG/JavaScript
- Include FontAwesome CSS in the Layout component's head section
- Copy FontAwesome webfonts to static output directory during build
- Use `fa-bars` icon for the sidebar toggle button

**Sidebar Toggle Button**
- Add button in far left position of the header, before site title
- Use FontAwesome `fa-bars` icon within the button
- Button remains visible and functional when sidebar is collapsed or expanded
- Apply Pico CSS button styles for consistency
- Position button using existing header container layout without modifying overall structure

**Sidebar Collapse/Expand Functionality**
- Implement CSS class `.sidebar-collapsed` on body element to control sidebar visibility
- Use CSS transitions with 300ms duration for smooth animation
- Toggle class via JavaScript click handler on the toggle button
- When collapsed, hide aside element and expand main area to full width
- Update grid-template-columns from `11rem 1fr` to `0 1fr` when collapsed
- Apply transition to grid-template-columns for smooth resize

**LocalStorage State Persistence**
- Read localStorage key `storyville.sidebar.collapsed` on page load
- Apply `.sidebar-collapsed` class to body if value is `true`
- Save state to localStorage when toggle button is clicked
- Handle missing localStorage gracefully (default to expanded state)

**Responsive Auto-Collapse**
- Use Pico CSS breakpoint `max-width: 768px` to auto-collapse sidebar on mobile
- Apply `.sidebar-collapsed` class automatically below mobile breakpoint
- Ensure toggle button remains functional on mobile devices
- Maintain localStorage state preference when resizing between breakpoints

**Automatic Navigation Tree Expansion**
- Add JavaScript that runs on page load to parse `window.location.pathname`
- Match pathname to navigation items by comparing href attributes
- Find all ancestor `<details>` elements of the matching navigation link
- Set `open` attribute on all ancestor details elements to expand the tree
- Handle cases where no matching navigation item is found (fail silently)

**Navigation List Item Padding Reduction**
- Update CSS selector `aside > nav > details > ul > li` padding from current values
- Change `padding-top` and `padding-bottom` from 10 units to 4 units
- Maintain existing horizontal padding values
- Apply to all nested levels of navigation list items

## Visual Design

No visual mockups provided. Implementation should follow existing Pico CSS design patterns and maintain visual consistency with current layout.

## Existing Code to Leverage

**Layout Component (`src/storyville/components/layout/layout.py`)**
- Extend head section to include FontAwesome CSS link after Pico CSS
- Add sidebar toggle button to LayoutHeader component before site title
- Add new JavaScript file reference for sidebar and tree expansion logic
- Maintain existing depth-based path rewriting for static assets

**LayoutHeader Component (`src/storyville/components/header/header.py`)**
- Insert toggle button as first element in header container before hgroup
- Use tdom to render button with FontAwesome icon class
- Add appropriate ARIA attributes for accessibility

**CSS Grid Layout (`var/static/components/layout/static/storyville.css`)**
- Grid layout already defined with `grid-template-columns: 11rem 1fr`
- Existing responsive layout at `@media (max-width: 768px)` changes to single column
- Leverage existing CSS transitions pattern (200ms ease used for iframe-reloading)
- Copy transition pattern for sidebar collapse animation at 300ms

**WebSocket JavaScript (`var/static/components/layout/static/ws.js`)**
- Follow existing IIFE pattern for encapsulation
- Use similar DOM query patterns (`document.querySelector`)
- Apply consistent error handling approach (try-catch with graceful fallback)
- Store functions in similar variable patterns for reusability

**NavigationTree Component (`src/storyville/components/navigation_tree/navigation_tree.py`)**
- Navigation uses `<details>` and `<summary>` elements for collapsible sections
- Links have href format `/{section}/{subject}/story-{idx}/index.html`
- Server-side already handles `open` attribute based on current resource_path
- JavaScript should complement server-side expansion by ensuring all ancestors are open

## Out of Scope
- Keyboard shortcuts for sidebar toggle (no keyboard navigation enhancements in this spec)
- Changing header layout structure beyond adding the toggle button
- Modifying colors other than main area background
- Advanced tree navigation features like search or filtering
- Scrolling active navigation item into view (nice-to-have but not required)
- Theme switching or color scheme modifications
- Mobile gesture controls for sidebar
- Sidebar resize/drag functionality
- Animation preferences based on prefers-reduced-motion
- Adding icons to navigation tree items beyond the toggle button
