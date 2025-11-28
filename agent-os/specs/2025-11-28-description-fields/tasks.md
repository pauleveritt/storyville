# Task Breakdown: Story/Subject/Section Description Fields

## Overview
Total Task Groups: 3
Estimated Total Tasks: ~20 focused tasks

This feature adds description field rendering to SectionView, SubjectView, and StoryView. The implementation follows the existing conditional rendering pattern from SectionView (lines 38-42) and leverages tdom's automatic HTML escaping for safety.

## Task List

### View Components - SectionView

#### Task Group 1: SectionView Description Rendering (Already Complete)
**Dependencies:** None

- [x] 1.0 SectionView description rendering (already implemented)
  - [x] 1.1 Description field already renders after section title
  - [x] 1.2 Conditional rendering pattern already in place (lines 38-42)
  - [x] 1.3 Uses tdom automatic HTML escaping
  - [x] 1.4 Skips rendering if description is None or empty

**Status:** COMPLETE - SectionView already implements the description rendering pattern correctly. This serves as the reference implementation for SubjectView and StoryView.

**Reference Code:** `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/section/views.py` (lines 38-42)

### View Components - SubjectView

#### Task Group 2: SubjectView Description Rendering
**Dependencies:** None (uses existing pattern from SectionView)

- [ ] 2.0 Add description rendering to SubjectView
  - [ ] 2.1 Write 2-4 focused tests for SubjectView description rendering
    - Test description renders after title and before "Target: X" line
    - Test description skipped when None or empty string
    - Test HTML escaping with dangerous characters (e.g., `<script>`)
    - Use aria-testing functions: `get_by_tag_name()`, `get_text_content()`
    - Test file: `tests/subject/test_subject_view.py` (or existing test file location)
  - [ ] 2.2 Add conditional description rendering to SubjectView.__call__()
    - Copy pattern from SectionView lines 38-42:
      ```python
      description_p = (
          html(t"<p>{self.subject.description}</p>")
          if self.subject.description is not None
          else ""
      )
      ```
    - Insert `{description_p}` after `<h1>{self.subject.title}</h1>`
    - Place before `<p>Target: {target_name}</p>` line
    - Apply to BOTH rendering paths (with items and empty state)
  - [ ] 2.3 Ensure SubjectView description tests pass
    - Run ONLY the 2-4 tests written in 2.1
    - Verify description renders in correct position
    - Verify None/empty handling works
    - Verify HTML escaping is automatic
    - Do NOT run entire test suite at this stage

**Acceptance Criteria:**
- The 2-4 tests written in 2.1 pass
- Description renders after title and before "Target: X" line
- No rendering when description is None or empty
- HTML content is automatically escaped by tdom
- Pattern matches SectionView implementation

**Files to Modify:**
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/subject/views.py`
- Test file (location depends on project structure)

### View Components - StoryView

#### Task Group 3: StoryView Description Rendering (Mode B & Mode C Only)
**Dependencies:** None (uses existing pattern from SectionView)

- [ ] 3.0 Add description rendering to StoryView (Modes B and C only)
  - [ ] 3.1 Write 4-6 focused tests for StoryView description rendering
    - Test description renders in Mode B (Default Layout) above Props line
    - Test description renders in Mode C (Themed Iframe) above Props line
    - Test description NOT rendered in Mode A (Custom Template)
    - Test description skipped when None or empty string in Mode B
    - Test HTML escaping with dangerous characters in Mode B
    - Test both with-badges and without-badges rendering paths
    - Use aria-testing functions: `get_by_tag_name()`, `get_text_content()`
    - Test file: `tests/story/test_story_view.py` (or existing test file location)
  - [ ] 3.2 Add conditional description rendering to Mode C (Themed Iframe)
    - Apply to Mode C block (lines 125-158)
    - Copy pattern from SectionView lines 38-42:
      ```python
      description_p = (
          html(t"<p>{self.story.description}</p>")
          if self.story.description is not None
          else ""
      )
      ```
    - Insert `{description_p}` after header div, before `<p>Props:` line
    - Apply to BOTH paths: with badges (lines 132-147) and without badges (lines 150-158)
  - [ ] 3.3 Add conditional description rendering to Mode B (Default Layout)
    - Apply to Mode B block (lines 160-194)
    - Use same conditional pattern from step 3.2
    - Insert `{description_p}` after header div, before `<p>Props:` line
    - Apply to BOTH paths: with badges (lines 164-181) and without badges (lines 184-194)
  - [ ] 3.4 Verify Mode A (Custom Template) does NOT render description
    - Mode A returns early at line 119
    - No changes needed to Mode A logic
    - Custom templates control their own content
  - [ ] 3.5 Ensure StoryView description tests pass
    - Run ONLY the 4-6 tests written in 3.1
    - Verify description renders in Mode B above Props line
    - Verify description renders in Mode C above Props line
    - Verify description NOT rendered in Mode A
    - Verify None/empty handling works in both modes
    - Verify HTML escaping is automatic
    - Do NOT run entire test suite at this stage

**Acceptance Criteria:**
- The 4-6 tests written in 3.1 pass
- Description renders in Mode B above Props line (both badge paths)
- Description renders in Mode C above Props line (both badge paths)
- Description NOT rendered in Mode A (custom templates)
- No rendering when description is None or empty
- HTML content is automatically escaped by tdom
- Pattern matches SectionView implementation

**Files to Modify:**
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/story/views.py`
- Test file (location depends on project structure)

**Implementation Notes:**
- StoryView has 4 rendering paths total (Mode C with/without badges, Mode B with/without badges)
- Description must be added to all 4 paths consistently
- Mode A (Custom Template) intentionally excluded - no changes needed

### Quality Assurance & Integration

#### Task Group 4: Quality Checks and Integration Testing
**Dependencies:** Task Groups 2 and 3

- [ ] 4.0 Run quality checks and integration tests
  - [ ] 4.1 Run focused feature tests
    - Run SubjectView description tests (from 2.1)
    - Run StoryView description tests (from 3.1)
    - Verify all new tests pass (approximately 6-10 tests total)
    - Do NOT run entire test suite yet
  - [ ] 4.2 Run full test suite
    - Execute: `just test`
    - Ensure no regressions in existing tests
    - Verify all tests pass (new + existing)
    - Fix any breaking changes if needed
  - [ ] 4.3 Run type checking
    - Execute: `just typecheck`
    - Ensure no type errors introduced
    - Verify modern Python type hints used correctly
    - Fix any type issues
  - [ ] 4.4 Run code formatting
    - Execute: `just fmt`
    - Ensure consistent code style
    - Verify formatting applied to all modified files
  - [ ] 4.5 Manual verification in browser
    - Build the site to generate HTML
    - Verify SectionView description renders correctly
    - Verify SubjectView description renders after title, before "Target: X"
    - Verify StoryView description renders in Mode B above Props
    - Verify StoryView description renders in Mode C above Props (if themed layout configured)
    - Verify no empty `<p></p>` tags when description is None/empty
    - Test HTML escaping by adding description with `<script>alert('test')</script>`

**Acceptance Criteria:**
- All feature tests pass (6-10 tests from Task Groups 2-3)
- Full test suite passes with no regressions
- Type checking passes with no errors
- Code formatting applied successfully
- Manual browser testing confirms correct rendering
- HTML escaping verified with dangerous content

**Quality Commands:**
```bash
# Run tests
just test

# Run type checking
just typecheck

# Run formatting
just fmt
```

## Execution Order

Recommended implementation sequence:

1. **Task Group 1: SectionView** (COMPLETE - already implemented)
2. **Task Group 2: SubjectView** - Add description rendering using SectionView pattern
3. **Task Group 3: StoryView** - Add description rendering to Mode B and Mode C only
4. **Task Group 4: Quality Checks** - Run tests, type checking, formatting, and manual verification

## Implementation Strategy

### Code Reuse Pattern

All three views follow the same conditional rendering pattern from SectionView:

```python
description_p = (
    html(t"<p>{self.{entity}.description}</p>")
    if self.{entity}.description is not None
    else ""
)
```

Then insert `{description_p}` at the appropriate location in the template.

### Testing Strategy

- Write 2-6 focused tests per view (total ~10 tests maximum)
- Test critical behaviors: rendering, None handling, HTML escaping
- Use aria-testing library functions (`get_by_tag_name()`, `get_text_content()`)
- Run feature tests first, then full test suite
- Skip exhaustive edge case testing

### HTML Escaping

- tdom automatically escapes interpolated strings in `t""` templates
- No manual escaping needed - safety is built-in
- Test with dangerous content (e.g., `<script>`) to verify

### Placement Positions

- **SectionView**: After `<h1>`, before subject list (ALREADY DONE)
- **SubjectView**: After `<h1>`, before `<p>Target: X</p>`
- **StoryView Mode B**: After header div, before `<p>Props: ...</p>`
- **StoryView Mode C**: After header div, before `<p>Props: ...</p>`

## Technical Considerations

### Modern Python Standards

- Use Python 3.14+ features
- Use modern type hints: `str | None` instead of `Optional[str]`
- Use built-in generics: `list[str]` instead of `List[str]`
- Follow PEP 604 union syntax
- Use structural pattern matching (`match`/`case`) if appropriate

### File Paths

**Views to Modify:**
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/subject/views.py`
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/story/views.py`

**Reference Implementation:**
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/section/views.py` (lines 38-42)

**Test Files:**
- Location depends on project test structure (verify actual paths)
- Use aria-testing library for DOM queries
- Follow single test file per component pattern

### Dependencies

- No new dependencies required
- Uses existing tdom templating system
- Uses existing PicoCSS styling
- Uses existing aria-testing for tests

## Out of Scope

- Markdown or rich text formatting for descriptions
- Text truncation or "read more" functionality
- Custom CSS classes or special styling
- Description field for Site entity
- Editing or managing description content through UI
- Backend changes (description fields already exist on models)
- Database migrations (description fields already defined)
- Validation or character limits
- i18n or localization
