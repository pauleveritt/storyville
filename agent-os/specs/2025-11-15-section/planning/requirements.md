# Spec Requirements: Section

## Initial Description
A Section is a unit of organization that collects Subject instances. It's basically a folder. It has a title, description, and items as a dict of str/Subjects. A Section follows the same layout as Story and Subject: models.py and views.py, corresponding tests.

## Requirements Discussion

### First Round Questions

**Q1:** For the hierarchy, I'm assuming Section.parent is Site (so the hierarchy is Site → Section → Subject → Story). Is that correct, or does Section have a different parent?
**Answer:** YES - Section.parent is Site. The hierarchy is Site → Section → Subject → Story.

**Q2:** I notice you mentioned "items as a dict of str/Subjects". Should we keep this dict structure, or would you prefer to convert to a list like we did with Story.subjects (list[Subject])?
**Answer:** Keep `items: dict[str, Subject]` - do NOT convert to list.

**Q3:** For the description field, I'm thinking it should be optional (str | None = None) and render as a <p> element after the title in SectionView. Is that the right approach?
**Answer:** YES - `description: str | None = None`, rendered in `<p>` after title.

**Q4:** For SectionView rendering, I'm assuming we should: Display the title as <h1>, show description in a <p>, list the Subject items (probably as clickable cards/links), and include a parent link back to the Site. Does that match your vision?
**Answer:** YES - Title as `<h1>`, description in `<p>`, list of Subject cards, parent link.

**Q5:** Since Section is migrating from an existing section.py file, should we expect a straightforward refactoring from the existing code, or are there significant changes planned?
**Answer:** Straightforward refactoring - move from `section.py` to package structure.

**Q6:** For the BaseNode inheritance, I assume Section should continue inheriting from BaseNode["Section"] like the other nodes. Should Section override the post_update() method like Story does, or use the inherited implementation like Subject does?
**Answer (Follow-up):** NO - Section should NOT override `post_update()` method. It will use the inherited BaseNode implementation, like Subject does.

**Q7:** For the test structure, should we follow the same pattern as Story with tests/section/test_section_models.py and tests/section/test_section_views.py?
**Answer:** YES - `tests/section/test_section_models.py` and `tests/section/test_section_views.py`.

**Q8:** When rendering the items (dict[str, Subject]), should we iterate over items.values() to create a list of clickable cards/links using each Subject's title?
**Answer:** YES - Iterate over `items.values()`, create link cards using Subject's title.

**Q9:** Are there any aspects of Section functionality that should be explicitly excluded from this initial implementation?
**Answer:** Not specified - assume minimal viable implementation.

### Existing Code to Reference

**Similar Features Identified:**
- Feature: Story package - Path: `src/storytime/story/`
- Feature: Subject package - Path: `src/storytime/subject/`
- Existing Section implementation - Path: `src/storytime/section.py` (to be migrated)
- Components to potentially reuse: BaseNode inheritance pattern, view rendering patterns from Story and Subject
- Backend logic to reference: Story and Subject model structures, view templates

### Follow-up Questions

**Follow-up 1:** For the BaseNode inheritance, I assume Section should continue inheriting from BaseNode["Section"] like the other nodes. Should Section override the post_update() method like Story does, or use the inherited implementation like Subject does?
**Answer:** NO - Section should NOT override `post_update()` method. It will use the inherited BaseNode implementation, like Subject does.

## Visual Assets

### Files Provided:
No visual assets provided.

### Visual Insights:
No visual assets to analyze.

## Requirements Summary

### Functional Requirements
- Section acts as an organizational container that collects Subject instances
- Section has a title (required), description (optional), and items (dict of str/Subject pairs)
- Section.parent is Site, establishing hierarchy: Site → Section → Subject → Story
- SectionView renders: title as `<h1>`, description in `<p>`, list of Subject cards/links, parent link to Site
- Section inherits from BaseNode["Section"] without overriding `post_update()` method
- Items are rendered by iterating over `items.values()` to create clickable cards using Subject titles
- Migration involves moving existing `section.py` code to package structure (models.py, views.py)

### Reusability Opportunities
- BaseNode inheritance pattern established by Story and Subject
- View rendering patterns from Story and Subject packages
- Model structure conventions from existing Story and Subject implementations
- Test structure patterns from Story package (separate test files for models and views)
- Existing Section implementation in `src/storytime/section.py` provides migration starting point

### Scope Boundaries

**In Scope:**
- Migrating Section from single file to package structure
- Creating models.py with Section class inheriting from BaseNode["Section"]
- Creating views.py with SectionView for rendering
- Adding optional description field with `<p>` rendering
- Maintaining dict[str, Subject] structure for items
- Rendering Subject items as clickable cards/links
- Including parent link to Site in view
- Creating comprehensive tests in tests/section/ directory

**Out of Scope:**
- Converting items dict to list structure
- Overriding `post_update()` method (using inherited implementation)
- Advanced Section features beyond basic organizational functionality
- Complex item ordering or filtering logic

### Technical Considerations
- Follow same package structure as Story: models.py, views.py, __init__.py
- Inherit from BaseNode["Section"] using same pattern as Story and Subject
- Use inherited `post_update()` implementation from BaseNode (like Subject does)
- Maintain dict[str, Subject] structure for items attribute
- Test structure mirrors Story: separate files for models and views
- Description field is optional: `description: str | None = None`
- View renders title, description, Subject cards, and parent link
- Migration from existing `src/storytime/section.py` should be straightforward refactoring
