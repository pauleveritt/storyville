# Spec Requirements: Story/Subject/Section Description Fields

## Initial Description
Add into the rendered HTML the `description` field on `Story`, `Subject`, and `Section`.

**Context**: This is roadmap item #9. The system already has a structure with Site → Section → Subject → Story hierarchy. This feature will enhance the web-based component browser by displaying description fields that are already defined on these entities.

## Requirements Discussion

### First Round Questions

**Q1: SubjectView description placement** - Where should the description appear in SubjectView?
**Answer:** Place it after the title and before "Target: X" line, wrapped in a `<p>` tag (consistent with SectionView)

**Q2: StoryView description rendering modes** - Which rendering modes should display descriptions?
**Answer:** Display descriptions in Mode B (Default Layout) and Mode C (Themed Iframe) only. NOT in Mode A (Custom Template).

**Q3: Markdown support** - Should descriptions support Markdown formatting?
**Answer:** Plain text only - no Markdown rendering needed. Use tdom's automatic HTML escaping.

**Q4: Handling None/empty descriptions** - How should None or empty descriptions be handled?
**Answer:** Don't render anything (no empty `<p>` tags)

**Q5: CSS styling** - What CSS styling should be applied to descriptions?
**Answer:** Use plain PicoCSS paragraph styling - no special CSS classes needed

**Q6: Story description placement** - Where should the description appear in StoryView?
**Answer:** Above the Props line (more prominent position)

**Q7: Long descriptions** - Should there be any truncation or "read more" functionality for long descriptions?
**Answer:** No truncation or "read more" functionality needed - display at full length

### Existing Code to Reference

No similar existing features identified for reference.

### Follow-up Questions

No follow-up questions were needed.

## Visual Assets

### Files Provided:
No visual assets provided.

### Visual Insights:
No visual assets to analyze.

## Requirements Summary

### Functional Requirements

**SectionView:**
- Display `Section.description` field in the rendered HTML
- Placement: After section title, wrapped in `<p>` tag
- Rendering: Plain text with automatic HTML escaping (tdom default behavior)
- Empty handling: Skip rendering if None or empty string

**SubjectView:**
- Display `Subject.description` field in the rendered HTML
- Placement: After the title and before "Target: X" line, wrapped in `<p>` tag
- Rendering: Plain text with automatic HTML escaping (tdom default behavior)
- Empty handling: Skip rendering if None or empty string
- Consistency: Follow same pattern as SectionView

**StoryView:**
- Display `Story.description` field in the rendered HTML
- Placement: Above the Props line (more prominent position)
- Rendering modes: Display in Mode B (Default Layout) and Mode C (Themed Iframe) ONLY
- Mode exclusion: Do NOT display in Mode A (Custom Template)
- Rendering: Plain text with automatic HTML escaping (tdom default behavior)
- Empty handling: Skip rendering if None or empty string

**Text Rendering:**
- Plain text only - no Markdown processing required
- Rely on tdom's automatic HTML escaping for safety
- No truncation or "read more" functionality
- Display full description text at any length

**Styling:**
- Use plain PicoCSS paragraph styling
- No special CSS classes needed
- Consistent with existing paragraph elements in the application

### Reusability Opportunities

No existing similar features were identified for code reuse. This feature establishes new patterns for displaying description metadata throughout the component browser hierarchy.

### Scope Boundaries

**In Scope:**
- Rendering `description` field for Section, Subject, and Story entities
- Plain text display with HTML escaping
- Conditional rendering (skip if None/empty)
- Integration into existing view templates (SectionView, SubjectView, StoryView)
- Mode-specific rendering for StoryView (Modes B and C only)

**Out of Scope:**
- Markdown or rich text formatting
- Text truncation or "read more" functionality
- Special CSS styling or custom classes
- Description field for Site entity
- Editing or managing description content (assumes descriptions are already defined in the data model)
- Description display in StoryView Mode A (Custom Template)

### Technical Considerations

**Integration Points:**
- SectionView template rendering
- SubjectView template rendering
- StoryView template rendering with mode detection
- Existing tdom HTML escaping mechanism

**Existing System Constraints:**
- Must use tdom for rendering (framework-independent templating)
- Must follow PicoCSS styling conventions
- Must maintain consistency with existing view patterns
- Mode-based rendering logic already exists in StoryView (Modes A, B, C)

**Technology Preferences:**
- Python 3.14+ with modern type hints
- tdom templating system
- PicoCSS for styling
- No additional dependencies for text rendering

**Implementation Considerations:**
- Description fields are assumed to already exist on Story, Subject, and Section data models
- Empty/None checks should be done before rendering to avoid empty paragraph tags
- HTML escaping is handled automatically by tdom - no manual escaping needed
- StoryView mode detection logic needs to be leveraged to conditionally render descriptions
- Placement consistency: All three views should follow similar visual hierarchy patterns
