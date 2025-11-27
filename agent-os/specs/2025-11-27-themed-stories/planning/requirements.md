# Spec Requirements: Themed Stories

## Initial Description

Show a rendering of the story as a full HTML file, shown in an `<iframe>` in the story view. This `ThemedStory` should
use a `ThemedLayout` that is defined on the `Site`.

## Requirements Discussion

### First Round Questions

**Q1:** For the ThemedStory component, should it receive props like `story_title` and `children` (where children
contains the story content), or should it have access to the full Story dataclass?
**Answer:** It should receive `story_title` and `children` as props. `children` will come with the nested children style
of components.

**Q2:** For the file rendering logic - when writing story-0/index.html and the themed version, should the themed version
be in a file like `story-0/themed_story.html` that the iframe points to with a relative path like `./themed_story.html`?
**Answer:** Yes, point using a relative path of `./themed_story.html`

**Q3:** For the example ThemedLayout component - should it be placed in a new example folder like
`examples/themed_layout/` to demonstrate the feature, or would you prefer it elsewhere?
**Answer:** Change the path to `examples/minimal/themed_layout/themed_layout.py`

**Q4:** Should the ThemedLayout be configurable at the site level (e.g., `Site.themed_layout`), and if so, should it be
optional with a default fallback to the standard Storytime Layout?
**Answer:** Yes, `Site.themed_layout`. It is optional; if None, defaults to Storytime `Layout`.

**Q5:** Are there any exclusions or features we should explicitly NOT include in this initial implementation?
**Answer:** No multiple themes for now (roadmap item #20 is out of scope).

### Existing Code to Reference

**Similar Features Identified:**

- Feature: Current Layout component - Path: `src/storytime/layout.py`
- Feature: Story rendering logic - Path: `src/storytime/writer.py`
- Components to potentially reuse: The existing Layout component structure and rendering patterns
- Backend logic to reference: The current story writing logic in writer.py

### Follow-up Questions

**Follow-up 1:** Should the example ThemedLayout render full HTML structure (DOCTYPE, html, head, body tags) or just the
body content?
**Answer:** Full HTML structure (DOCTYPE, html, head, body) for examples.

**Follow-up 2:** For the Site dataclass modification - should `themed_layout` be a new property that accepts a callable
component class?
**Answer:** Yes, new property on Site dataclass: `themed_layout`. ThemedLayout is a callable (like a component class
with `__call__()`) assigned to `Site.themed_layout`.

## Visual Assets

### Files Provided:

No visual assets provided.

## Requirements Summary

### Functional Requirements

- Create a ThemedStory component that renders story content within a ThemedLayout
- ThemedStory component receives `story_title` (string) and `children` (nested components style) as props
- ThemedLayout is a callable component (with `__call__()` method) that can be assigned to `Site.themed_layout`
- ThemedLayout renders full HTML structure (DOCTYPE, html, head, body)
- When writing story files, generate two HTML files:
    - `story-X/index.html`: Contains the iframe pointing to themed version
    - `story-X/themed_story.html`: Contains the themed story rendering
- iframe uses relative path: `./themed_story.html`
- Add `themed_layout` property to Site dataclass (optional, defaults to None)
- If `Site.themed_layout` is None, fall back to standard Storytime Layout component
- Create example ThemedLayout at `examples/minimal/themed_layout/themed_layout.py`

### Reusability Opportunities

- Reference existing Layout component structure: `src/storytime/layout.py`
- Follow patterns from current story writing logic: `src/storytime/writer.py`
- Reuse component rendering patterns and callable component structure
- Model ThemedLayout after existing Layout component design

### Scope Boundaries

**In Scope:**

- ThemedStory component implementation
- ThemedLayout as configurable site property
- Dual HTML file generation (index.html with iframe + themed_story.html)
- Example ThemedLayout component
- Site dataclass modification to add `themed_layout` property
- Default fallback to standard Layout when no themed layout provided
- Full HTML structure rendering in themed version

**Out of Scope:**

- Multiple theme support (roadmap item #20)
- Theme switching UI
- Theme inheritance or composition
- Advanced theming features beyond single layout override

### Technical Considerations

- ThemedLayout must be a callable (component class with `__call__()`)
- Children prop uses nested children style of components
- Iframe isolation between story viewer and themed story content
- File path handling for relative iframe src
- Integration with existing writer.py rendering logic
- Site dataclass schema modification (adding optional property)
- Default behavior when `themed_layout` is None
