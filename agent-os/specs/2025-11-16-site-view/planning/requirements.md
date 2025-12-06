# Spec Requirements: SiteView

## Initial Description

**Date:** 2025-11-16

**User's Description:**

SiteView. Replace the current attempt at an IndexView in components/index ... no backwards compatibility needed, just remove it and any tests.

The SiteView should give a listing of its items, with links to visit each.

## Requirements Discussion

### First Round Questions

**Q1:** What information from each item should be displayed in the listing? Should it show just the section names, or also include descriptions, subject counts, story counts, or other metadata?

**Answer:** Only sections (list the sections from Site.items)

**Q2:** What details should be shown for each section? Should it display: title only, title + description, title + number of subjects, or other combinations?

**Answer:** Display: title, description, and link. Counter would be nice (showing number of subjects in each section)

**Q3:** What URL structure should be used for the section links? Should they follow a pattern like `/section/{section_name}`, `/sections/{section_id}`, or something else?

**Answer:** URL structure `/section/{section_name}` is fine

**Q4:** How should the sections be ordered in the listing? Alphabetically by title, by creation order, by a custom sort field, or insertion order?

**Answer:** Insertion order (as they appear in Site.items)

**Q5:** I assume this should follow the dataclass pattern with a `__call__` method returning a Node, similar to other view components. Is that correct?

**Answer:** Yes, dataclass with `__call__` method returning a Node

**Q6:** For the HTML structure, I'm thinking a `<ul>` with `<li>` elements for each section would be semantic. Should we use any specific CSS classes for styling, or keep it simple with basic HTML for now?

**Answer:** `<ul>` is fine for now

**Q7:** Should the SiteView accept a Site instance as a parameter, or should it work differently?

**Answer:** SiteView should accept a Site instance

**Q8:** Are there any features or edge cases you want to explicitly exclude from the initial implementation?

**Answer:** No exclusions from initial implementation

### Existing Code to Reference

**Similar Features Identified:**
- Component: `SectionsListing` - Path: `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/components/sections_listing/__init__.py`
  - Similar pattern: dataclass with `__call__` returning Node
  - Uses tdom html and t-strings for templating
  - Lists sections with nested structure

- Component: `ComponentView` - Path: `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/components/component_view/__init__.py`
  - Shows dataclass pattern with story parameter
  - Uses tdom html templating

- Component: `Layout` - Referenced in ComponentView for page wrapper
  - Path: `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/components/layout/`

### Follow-up Questions

No follow-up questions needed. Requirements are clear and complete.

## Visual Assets

### Files Provided:
No visual assets provided.

### Visual Insights:
No visual assets to analyze.

## Requirements Summary

### Functional Requirements

**Core Functionality:**
- Create a SiteView component that displays a listing of sections from a Site instance
- Each section listing item should show:
  - Section title
  - Section description
  - Link to the section
  - Counter showing number of subjects in the section
- Sections should be displayed in insertion order (as they appear in Site.items)
- Links should follow URL pattern: `/section/{section_name}`

**Component Structure:**
- Dataclass with Site instance as parameter
- `__call__` method that returns a Node
- Uses tdom html and t-strings for templating
- HTML structure: `<ul>` with `<li>` elements

**Cleanup Required:**
- Remove existing IndexView from `components/index/`
- Remove any tests related to IndexView
- No backwards compatibility needed

### Reusability Opportunities

**Existing Components to Reference:**
- `SectionsListing` (`/Users/pauleveritt/projects/t-strings/storyville/src/storyville/components/sections_listing/__init__.py`)
  - Follow same dataclass pattern with `__call__` returning Node
  - Use similar tdom templating approach
  - Reference list rendering structure

- `ComponentView` (`/Users/pauleveritt/projects/t-strings/storyville/src/storyville/components/component_view/__init__.py`)
  - Example of dataclass view component pattern
  - Shows tdom html usage

**Data Models:**
- `Site` class (`/Users/pauleveritt/projects/t-strings/storyville/src/storyville/site/models.py`)
  - Has `items: dict[str, Section]` attribute
  - Extends BaseNode

- `Section` class (`/Users/pauleveritt/projects/t-strings/storyville/src/storyville/section/models.py`)
  - Has `title` attribute (inherited from BaseNode)
  - Has `description: str | None` attribute
  - Has `items: dict[str, Subject]` attribute (for counting subjects)

### Scope Boundaries

**In Scope:**
- SiteView component creation with dataclass pattern
- Listing all sections from Site.items
- Displaying title, description, link, and subject count for each section
- Using insertion order for sections
- URL pattern `/section/{section_name}`
- HTML structure with `<ul>` and `<li>` elements
- Removal of IndexView and its tests

**Out of Scope:**
- Styling with specific CSS classes (keeping it simple for now)
- Sorting options (using insertion order only)
- Filtering or search functionality
- Pagination
- Subject or story level details in this view

### Technical Considerations

**Technology Stack:**
- Python 3.14+ with modern type hints
- tdom for templating using t-strings
- dataclass pattern for component definition
- Type hints using PEP 604 syntax (`X | Y`)

**Integration Points:**
- Works with Site model from `storyville.site.models`
- Accesses Section instances from Site.items dict
- May integrate with Layout component for full page rendering

**Existing System Constraints:**
- Follow tdom templating conventions
- Use html() function and t-strings for markup
- Return Node type from `__call__` method
- Follow dataclass pattern established in codebase

**Code Patterns to Follow:**
- Dataclass with `__call__` method returning Node
- Type annotations on all fields and methods
- tdom html templating with t-strings
- List comprehensions for rendering collections
