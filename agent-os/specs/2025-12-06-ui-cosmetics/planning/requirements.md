# Spec Requirements: UI Cosmetics

## Initial Description

Make the `<main>` area a slightly-less black background color. Bring in a local copy of FontAwesome icons. Add a button in the far left of the Header to toggle the LayoutAside and give more room to Main. Use a FontAwesome icon for that. Add some JavaScript that looks at the URL and correctly expands the current node. Remove more top/bottom padding in the LayoutAside `aside > nav > details > ul > li` which has 10 units of padding top/bottom.

## Requirements Discussion

### First Round Questions

**Q1:** For the main area background color, I assume we should use a subtle gray that maintains good contrast with text while being less stark than black. Should we use a Pico CSS variable (like `--pico-background-color` or similar) or define a custom shade?
**Answer:** Prefer existing Pico CSS variable if there's one that is gray-ish (investigate Pico's color variables).

**Q2:** For FontAwesome, I'm thinking we should use the free version and include it as a local npm dependency rather than a CDN link. Should we use the web fonts approach or the SVG/JavaScript approach?
**Answer:** Use the web fonts approach with npm dependency.

**Q3:** For the sidebar toggle button, I assume it should persist its state (collapsed/expanded) across page loads using localStorage. Is that correct, and if so, what should the localStorage key be named?
**Answer:** Use `storyville.sidebar.collapsed` as the localStorage key.

**Q4:** When you mention "correctly expands the current node" - I'm assuming this means: (a) parse the current URL path, (b) find the matching navigation item, and (c) expand all parent `<details>` elements in the tree. Should the expansion also scroll the active item into view?
**Answer:** Yes, expand all ancestor nodes up to the root. Scrolling into view would be nice but is not required for this spec.

**Q5:** For the sidebar toggle, should we add smooth CSS transitions for the collapse/expand animation? If yes, what duration feels appropriate (200ms, 300ms, etc.)?
**Answer:** 300ms animation duration.

**Q6:** When the sidebar is collapsed, should the toggle button remain visible (floating or in the header), or should there be another way to re-expand it?
**Answer:** Keep the toggle button in the header; it remains visible when collapsed.

**Q7:** For the reduced padding in `aside > nav > details > ul > li`, you mentioned it currently has 10 units top/bottom. What should the new padding be?
**Answer:** Reduce to 4 units top/bottom.

**Q8:** Should the sidebar collapse be responsive? For example, should it auto-collapse on mobile devices below a certain breakpoint?
**Answer:** Use Pico CSS's existing breakpoint variables - auto-collapse on mobile.

**Q9:** Is there anything we should NOT include in this spec? For example: changing colors beyond the main background, modifying the header layout beyond adding the toggle button, or adding keyboard shortcuts for the sidebar toggle?
**Answer:** Do not change header layout beyond adding the toggle button. No keyboard shortcuts in this spec.

### Existing Code to Reference

No similar existing features identified for reference.

The user has not provided information about existing code patterns for localStorage, sidebar, or CSS transitions.

### Follow-up Questions

**Follow-up 1:** For the tree expansion logic, should we expand only the direct path to the current item, or expand all ancestor nodes including siblings at each level?
**Answer:** Expand all ancestor nodes up to the root.

## Visual Assets

### Files Provided:

No visual assets provided.

## Requirements Summary

### Functional Requirements

**Visual Refinements:**
- Update `<main>` background color to use an existing Pico CSS gray variable
- Reduce padding in `aside > nav > details > ul > li` from 10 units to 4 units top/bottom

**FontAwesome Integration:**
- Install FontAwesome free version as local npm dependency
- Use web fonts approach (not SVG/JavaScript)
- Use icons in the toggle button

**Sidebar Toggle:**
- Add toggle button in far left of header
- Use FontAwesome icon for the button
- Button remains visible in header when sidebar is collapsed
- Implement smooth CSS transition (300ms duration)
- Persist collapsed/expanded state in localStorage with key `storyville.sidebar.collapsed`
- Auto-collapse sidebar on mobile using Pico CSS breakpoint variables

**Automatic Tree Expansion:**
- Parse current URL path on page load
- Find matching navigation item in tree
- Expand all ancestor `<details>` elements up to root
- Scroll active item into view (nice-to-have, not required)

### Reusability Opportunities

No existing similar features identified. Implementation will need to create new patterns for:
- localStorage state management
- Sidebar collapse/expand behavior
- CSS transitions for layout changes
- URL-based tree navigation

### Scope Boundaries

**In Scope:**
- Main area background color update using Pico CSS variable
- FontAwesome local installation and setup
- Sidebar toggle button with icon in header
- Sidebar collapse/expand with animation
- localStorage persistence of sidebar state
- Responsive auto-collapse on mobile
- URL-based automatic tree expansion
- Reduced padding in navigation list items

**Out of Scope:**
- Changing header layout beyond adding toggle button
- Keyboard shortcuts for sidebar toggle
- Changing other colors beyond main background
- Modifying header structure
- Advanced tree navigation features
- Scrolling active item into view (nice-to-have but not required)

### Technical Considerations

**Technology Stack:**
- Pico CSS variables for colors and breakpoints
- FontAwesome free version via npm
- localStorage for state persistence
- CSS transitions for animations
- JavaScript for tree expansion logic

**Integration Points:**
- Existing Pico CSS theming system
- Current layout structure (Header, LayoutAside, Main)
- Existing navigation tree markup (`<details>` elements)
- URL routing system

**Design Decisions:**
- localStorage key: `storyville.sidebar.collapsed`
- Animation duration: 300ms
- Padding reduction: 10 units → 4 units
- Use Pico CSS variables for consistency
- Web fonts approach for FontAwesome

**Responsive Behavior:**
- Use Pico CSS breakpoint variables
- Auto-collapse sidebar below mobile breakpoint
- Toggle button always visible in header
