# Spec Requirements: Subject Package

## Initial Description

A Subject is an entity that collects a group of Story entries about a component, a view, or some other visible part of
the system. It should have a parent, a target (the callable component or view etc.) and stories as a list of Story
instances. It should be a Python package with models.py and views.py. We have a start of this in subject.py. Tests
should go in `tests/subject/`. The SubjectView will render some markup then the list of Story objects via StoryView. If
a Story does not have a component, and the Subject does, it can pass in the Subject to the StoryView.

## Requirements Discussion

### First Round Questions

**Q1:** I assume the parent-child hierarchy is: Site → Section → Subject → Story. Is that correct?
**Answer:** YES

**Q2:** I'm thinking the package should be located at `src/storytime/subject/` with `models.py` and `views.py` inside.
Should we follow this structure?
**Answer:** YES - follow the `src/storytime/story/` pattern with models.py and views.py

**Q3:** For the `target` attribute (the callable component/view), should both Subject and Story have this field, with
Story optionally inheriting from Subject if not specified?
**Answer:** See follow-up answer below regarding terminology

**Q4:** For SubjectView rendering, should it follow a similar pattern to StoryView (showing subject metadata/title, then
rendering each story)?
**Answer:** YES - similar pattern to StoryView

**Q5:** Should we keep the Story.post_update() protocol where Story checks for parent.target if it doesn't have its own
target?
**Answer:** YES - keep this protocol (will use `self.parent.target` after terminology change)

**Q6:** For rendering stories in SubjectView, should we use simple story cards with basic metadata (title, link) rather
than full StoryView rendering?
**Answer:** YES - simple cards, NO StoryView, NO custom templates

**Q7:** If a Subject has no stories yet, should we show an empty state message like "No stories defined for this
component"?
**Answer:** YES - show empty state message

**Q8:** Are there any features we should explicitly exclude from this initial implementation (e.g., filtering stories,
inline editing, reordering)?
**Answer:** YES - exclude filtering/search, inline editing, and reordering

### Existing Code to Reference

**Similar Features Identified:**

- Feature: Story package - Path: `src/storytime/story/`
- Components to potentially reuse: Follow the same package structure pattern (models.py, views.py)
- Backend logic to reference: Story.post_update() protocol for inheritance

### Follow-up Questions

**Follow-up 1:** Should we rename the `component` attribute to `target` in BOTH Subject and Story classes for
consistency?
**Answer:** YES - rename `component` to `target` in BOTH Subject and Story classes. This means:

- Subject.target (the component/view/callable that stories are about)
- Story.target (inherited from Subject.target if Story doesn't specify one)
- Story.post_update() checks `self.parent.target` instead of `self.parent.component`

## Visual Assets

### Files Provided:

No visual assets provided.

### Visual Insights:

No visual assets provided.

## Requirements Summary

### Functional Requirements

- Create Subject class as a data model that:
    - Has a parent relationship to Section (hierarchy: Site → Section → Subject → Story)
    - Has a `target` attribute (renamed from `component`) for the component/view/callable
    - Contains a list of Story instances
    - Follows the same package structure as Story (`src/storytime/subject/` with `models.py` and `views.py`)

- Create SubjectView that:
    - Renders subject metadata/title
    - Displays stories as simple cards with basic metadata (title, link)
    - Shows empty state message when no stories exist: "No stories defined for this component"
    - Does NOT use StoryView for rendering individual stories
    - Does NOT use custom templates for story cards

- Update Story class to:
    - Rename `component` attribute to `target`
    - Keep post_update() protocol that checks `self.parent.target` (instead of `self.parent.component`)
    - Allow Story.target to inherit from Subject.target if not specified

- Tests should be placed in `tests/subject/`

### Reusability Opportunities

- Package structure: Follow `src/storytime/story/` pattern (models.py and views.py split)
- Inheritance protocol: Keep Story.post_update() pattern for target inheritance
- Empty state pattern: Similar approach to other views in the application

### Scope Boundaries

**In Scope:**

- Subject package creation with models.py and views.py
- Subject class with parent, target, and stories attributes
- SubjectView with basic rendering of subject and story cards
- Terminology change: rename `component` to `target` in both Subject and Story
- Story.post_update() protocol update to use `self.parent.target`
- Empty state handling
- Test coverage in tests/subject/

**Out of Scope:**

- Filtering or searching stories
- Inline editing of stories from SubjectView
- Reordering stories
- Full StoryView rendering within SubjectView
- Custom templates for story cards

### Technical Considerations

- Package location: `src/storytime/subject/` with `models.py` and `views.py`
- Test location: `tests/subject/`
- Parent-child hierarchy: Site → Section → Subject → Story
- Attribute naming: Use `target` (not `component`) for both Subject and Story
- Inheritance protocol: Story.post_update() checks `self.parent.target`
- Rendering approach: Simple cards with metadata, no StoryView nesting
- Similar code patterns to follow: `src/storytime/story/` package structure
