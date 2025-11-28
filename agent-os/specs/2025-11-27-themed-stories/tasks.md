# Task Breakdown: Themed Stories

## Overview
Total Tasks: 4 task groups with 22 sub-tasks

## Task List

### Data Models

#### Task Group 1: Site Model Extension
**Dependencies:** None

- [x] 1.0 Extend Site dataclass with themed_layout property
  - [x] 1.1 Write 2-4 focused tests for Site.themed_layout functionality
    - Test Site with themed_layout=None (default behavior)
    - Test Site with themed_layout=callable (custom ThemedLayout)
    - Test Site.themed_layout type validation (accepts Callable[..., Node] | None)
    - Skip exhaustive edge case testing
  - [x] 1.2 Add themed_layout field to Site dataclass
    - Type: `Callable[..., Node] | None = None`
    - Import Callable from typing and Node from tdom
    - Follow existing optional field pattern like static_dir
    - Place after static_dir field in dataclass definition
  - [x] 1.3 Ensure Site model tests pass
    - Run ONLY the 2-4 tests written in 1.1
    - Verify Site instantiation with and without themed_layout
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-4 tests written in 1.1 pass
- Site dataclass accepts optional themed_layout parameter
- Type hints follow Python 3.14+ standards (X | Y union syntax)
- Backward compatibility maintained (themed_layout defaults to None)

### Component Layer

#### Task Group 2: ThemedStory Component
**Dependencies:** Task Group 1

- [x] 2.0 Create ThemedStory component
  - [x] 2.1 Write 3-6 focused tests for ThemedStory component
    - Test ThemedStory renders with custom ThemedLayout callable
    - Test ThemedStory falls back to Layout when themed_layout=None
    - Test ThemedStory passes story_title and children props correctly
    - Test ThemedStory returns full HTML structure (DOCTYPE, html, head, body)
    - Skip exhaustive testing of all component states
  - [x] 2.2 Create ThemedStory component file at src/storytime/components/themed_story/themed_story.py
    - Implement as dataclass with fields: story_title (str), children (Node), site (Site)
    - Add __call__() -> Node method following Layout pattern
    - Check if site.themed_layout exists, use it if present
    - If site.themed_layout is None, instantiate and use Layout component
    - Pass story_title and children to themed_layout callable
    - Use modern type hints (str | None, Node | None)
  - [x] 2.3 Create __init__.py for themed_story module
    - Export ThemedStory component
    - Follow existing component module pattern
  - [x] 2.4 Ensure ThemedStory component tests pass
    - Run ONLY the 3-6 tests written in 2.1
    - Verify rendering with both themed_layout modes
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 3-6 tests written in 2.1 pass
- ThemedStory component follows dataclass + __call__() pattern
- Component correctly delegates to site.themed_layout or Layout
- Full HTML document structure returned
- Type hints use modern Python 3.14+ syntax

### Build Integration

#### Task Group 3: Dual HTML File Generation
**Dependencies:** Task Group 2

- [x] 3.0 Modify build process to generate themed_story.html files
  - [x] 3.1 Write 3-5 focused tests for dual file generation
    - Test build generates both index.html and themed_story.html per story
    - Test index.html contains iframe with src="./themed_story.html"
    - Test themed_story.html contains ThemedStory rendering
    - Test iframe element has sensible default styles (width: 100%, min-height, border)
    - Skip exhaustive testing of all build scenarios
  - [x] 3.2 Modify StoryView to render iframe when themed_layout exists
    - Check if site.themed_layout is not None
    - If True, wrap story content in iframe pointing to ./themed_story.html
    - If False, use existing StoryView rendering (Mode A/B unchanged)
    - Add iframe with default styles: width: 100%, min-height: 600px, border: 1px solid #ccc
    - Keep assertion badges in parent StoryView (not in iframe)
  - [x] 3.3 Add ThemedStory rendering in build.py Phase 2 (Rendering)
    - Import ThemedStory component
    - After rendering stories (line ~119), add loop to render themed stories
    - For each story, instantiate ThemedStory(story_title=story.title, children=story.instance, site=site)
    - Call ThemedStory() to get Node, convert to string
    - Store in rendered_themed_stories list: (section_key, subject_key, story_idx, themed_story_html)
    - Only render if site.themed_layout is not None
  - [x] 3.4 Add themed_story.html file writing in build.py Phase 3 (Writing)
    - After writing story index.html files (line ~149), add loop for themed stories
    - For each (section_key, subject_key, story_idx, themed_story_html) in rendered_themed_stories
    - Write to path: story_dir / "themed_story.html"
    - Use existing _write_html() helper
  - [x] 3.5 Ensure build integration tests pass
    - Run ONLY the 3-5 tests written in 3.1
    - Verify both files generated correctly
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 3-5 tests written in 3.1 pass
- Build generates story-X/index.html and story-X/themed_story.html
- index.html contains iframe with relative path ./themed_story.html
- themed_story.html contains full HTML document from ThemedStory
- Three-phase architecture maintained (Reading, Rendering, Writing)
- No performance impact when site.themed_layout is None

### Example Implementation

#### Task Group 4: Example ThemedLayout
**Dependencies:** Task Groups 1, 2, 3

- [x] 4.0 Create example ThemedLayout implementation
  - [x] 4.1 Write 2-3 focused tests for example ThemedLayout
    - Test ThemedLayout renders full HTML document structure
    - Test ThemedLayout passes through children content
    - Test ThemedLayout includes custom CSS styling
    - Skip exhaustive testing of visual styling
  - [x] 4.2 Create example ThemedLayout at examples/minimal/themed_layout/themed_layout.py
    - Implement as dataclass with fields: story_title (str | None), children (Node | None)
    - Add __call__() -> Node method returning tdom html t-string
    - Render full HTML: DOCTYPE, html lang="EN", head, body
    - In head: meta charset, viewport, title (use story_title if present)
    - In head: link to custom CSS (can be inline style tag for example)
    - In body: wrapper div with custom styling, render children inside
    - Include minimal CSS to demonstrate theming (e.g., custom colors, fonts)
    - Use tdom html t-string templates following Layout pattern
  - [x] 4.3 Create __init__.py for themed_layout example module
    - Export ThemedLayout from themed_layout.py
  - [x] 4.4 Update example Site configuration to use ThemedLayout
    - Locate examples/minimal site construction (likely in __init__.py or stories.py)
    - Import ThemedLayout from examples.minimal.themed_layout
    - Pass themed_layout=ThemedLayout to Site constructor
    - Verify example builds with themed stories
  - [x] 4.5 Ensure example ThemedLayout tests pass
    - Run ONLY the 2-3 tests written in 4.1
    - Verify full HTML structure rendered
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-3 tests written in 4.1 pass
- Example ThemedLayout renders complete HTML document
- Example demonstrates custom CSS styling capability
- Example Site successfully configured with themed_layout
- Build generates themed_story.html files for example stories

### Testing & Quality

#### Task Group 5: Test Review & Quality Checks
**Dependencies:** Task Groups 1-4

- [x] 5.0 Review existing tests and run quality checks
  - [x] 5.1 Review tests from Task Groups 1-4
    - Review the 2-4 tests written for Site model (Task 1.1)
    - Review the 3-6 tests written for ThemedStory component (Task 2.1)
    - Review the 3-5 tests written for build integration (Task 3.1)
    - Review the 2-3 tests written for example ThemedLayout (Task 4.1)
    - Total existing tests: approximately 10-18 tests
  - [x] 5.2 Analyze test coverage gaps for Themed Stories feature only
    - Identify critical user workflows that lack test coverage
    - Focus ONLY on gaps related to themed stories feature
    - Do NOT assess entire application test coverage
    - Prioritize integration workflows (site -> build -> HTML output)
  - [x] 5.3 Write up to 5 additional strategic tests maximum
    - Add maximum of 5 new tests to fill identified critical gaps
    - Focus on end-to-end workflow: Site with themed_layout -> build -> dual HTML files
    - Test iframe rendering in StoryView when themed_layout exists
    - Test backward compatibility: build without themed_layout (existing behavior unchanged)
    - Skip edge cases, performance tests, accessibility tests unless business-critical
  - [x] 5.4 Run feature-specific tests only
    - Run ONLY tests related to themed stories feature
    - Expected total: approximately 15-23 tests maximum
    - Do NOT run the entire application test suite
    - Verify critical workflows pass
  - [x] 5.5 Run quality checks
    - Run: just test (themed stories tests only)
    - Run: just typecheck (verify type hints)
    - Run: just fmt (format code)
    - All checks must pass

**Acceptance Criteria:**
- All feature-specific tests pass (approximately 15-23 tests total)
- No more than 5 additional tests added when filling gaps
- Type checking passes (mypy/pyright)
- Code formatting passes (ruff/black)
- Critical user workflows covered: Site configuration, component rendering, dual file generation
- Backward compatibility verified (no themed_layout = existing behavior)

## Execution Order

Recommended implementation sequence:
1. Data Models (Task Group 1) - Extend Site dataclass
2. Component Layer (Task Group 2) - Create ThemedStory component
3. Build Integration (Task Group 3) - Modify build process for dual HTML generation
4. Example Implementation (Task Group 4) - Create example ThemedLayout
5. Testing & Quality (Task Group 5) - Review tests and run quality checks

## Key Technical Decisions

**Type Hints:**
- Use Python 3.14+ modern syntax: `X | Y` instead of `Union[X, Y]`
- Use `Callable[..., Node]` for themed_layout type
- Use built-in generics: `dict[str, Section]` not `Dict[str, Section]`

**Component Pattern:**
- Follow dataclass + `__call__() -> Node` pattern like Layout
- Use tdom html t-string templates for markup generation
- Return full HTML document structure (DOCTYPE, html, head, body)

**Build Architecture:**
- Maintain three-phase architecture (Reading, Rendering, Writing)
- Render ThemedStory in Phase 2 after StoryView rendering
- Write themed_story.html in Phase 3 with existing _write_html() helper
- Only generate themed files when site.themed_layout is not None

**Backward Compatibility:**
- Site.themed_layout defaults to None (opt-in feature)
- When None, existing behavior unchanged (no iframe, single index.html)
- StoryView checks site.themed_layout before rendering iframe
- No performance impact when feature not used

**Testing Strategy:**
- Write 2-8 focused tests per task group during development
- Test only critical behaviors, not exhaustive coverage
- Run only newly written tests during development (not full suite)
- Final test review adds maximum 5 strategic tests for gaps
- Use aria-testing library for DOM queries (get_by_tag_name, get_text_content)
- Single test file per component (no separate integration test files)
