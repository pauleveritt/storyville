# Specification: Story/Subject/Section Description Fields

## Goal
Display description fields for Section, Subject, and Story entities in their respective views, with plain text rendering and automatic HTML escaping.

## User Stories
- As a component developer, I want to see section descriptions to understand the purpose and organization of each section
- As a component developer, I want to see subject descriptions to understand what each component does before viewing its stories
- As a story viewer, I want to see story descriptions in default layouts to understand the purpose and context of each variant

## Specific Requirements

**SectionView Description Rendering**
- Display `Section.description` field after the section title (`<h1>`)
- Wrap description in a `<p>` tag for proper semantic HTML
- Skip rendering entirely if description is `None` or empty string (no empty tags)
- Use tdom's automatic HTML escaping for text content (already built-in)
- Place description before the subject list and parent link

**SubjectView Description Rendering**
- Display `Subject.description` field after the subject title (`<h1>`)
- Insert description before the "Target: X" line for proper information hierarchy
- Wrap description in a `<p>` tag matching SectionView pattern
- Skip rendering entirely if description is `None` or empty string
- Maintain consistent placement pattern with SectionView

**StoryView Description Rendering - Mode Detection**
- Display `Story.description` only in Mode B (Default Layout) and Mode C (Themed Iframe)
- Do NOT display description in Mode A (Custom Template) - custom templates handle their own content
- Place description above the Props line (`<p>Props: <code>...</code></p>`)
- Position after title/badges but before props for prominence
- Skip rendering if description is `None` or empty string

**StoryView Mode B Implementation**
- Add description `<p>` tag between the story header div and Props line
- Maintain existing badge rendering logic and flexbox header layout
- Support both with-badges and without-badges rendering paths
- Ensure description appears consistently in both paths

**StoryView Mode C Implementation**
- Add description `<p>` tag between the story header div and Props line
- Place before the iframe element that loads themed_story.html
- Support both with-badges and without-badges rendering paths
- Keep description outside the iframe (in parent StoryView)

**Text Rendering and Safety**
- Render all descriptions as plain text (no Markdown processing)
- Rely on tdom's built-in HTML escaping for safety (already automatic)
- Display full description text without truncation or "read more" functionality
- Allow descriptions of any length to render completely

**Styling Approach**
- Use default PicoCSS paragraph styling (no custom classes needed)
- Maintain consistent visual hierarchy with existing paragraph elements
- No additional CSS or special styling required

**Conditional Rendering Pattern**
- Check for `None` or empty string before rendering
- Use inline conditional expressions: `description_p = html(t"<p>{description}</p>") if description else ""`
- Insert conditional result directly into template markup
- Ensure no empty `<p></p>` tags are rendered

## Visual Design
No visual assets provided.

## Existing Code to Leverage

**SectionView Conditional Rendering Pattern (lines 38-42)**
- Uses inline conditional: `description_p = html(t"<p>{description}</p>") if condition else ""`
- Inserts variable directly into tdom template
- Already implements the exact pattern needed for this feature
- Reuse this pattern in SubjectView and StoryView

**tdom HTML Template Escaping**
- tdom automatically escapes interpolated strings in `t""` templates
- Any `{variable}` inserted into tdom templates is safe by default
- No manual escaping needed for description text
- Safety is built into the templating system

**StoryView Mode Detection Logic (lines 118-119, 124-125)**
- Line 118: `if self.story.template is not None:` detects Mode A
- Line 125: `if self.site.themed_layout is not None:` detects Mode C
- Line 160: else clause handles Mode B (Default Layout)
- Leverage this existing branching structure to add descriptions only in Modes B and C

**StoryView Header Layout Structure**
- Lines 167-174 (Mode B with badges): flexbox header with title left, badges right
- Lines 135-142 (Mode C with badges): identical header structure
- Lines 153-154 (Mode C without badges): simple title + props + iframe
- Lines 187-188 (Mode B without badges): simple title + props + instance
- Insert description `<p>` tag after header div, before Props line in all four paths

**Layout Component Integration Pattern**
- All views wrap content in `<{Layout}>` component with standard props
- Layout handles site-wide structure (navigation, styling, depth)
- Views focus on entity-specific content rendering
- Description fields fit naturally into this separation of concerns

## Out of Scope
- Markdown or rich text formatting support for descriptions
- Text truncation, ellipsis, or "read more" functionality
- Custom CSS classes or special styling for description paragraphs
- Description field for Site entity (only Section, Subject, Story)
- Editing or managing description content through the UI
- Description display in StoryView Mode A (custom templates control their own content)
- Backend changes to add description fields (already exist on models)
- Migration or database schema changes (description fields already defined)
- Validation or character limits on description content
- i18n or localization of descriptions
