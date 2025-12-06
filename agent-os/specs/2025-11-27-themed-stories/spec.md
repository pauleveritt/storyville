# Specification: Themed Stories

## Goal

Enable stories to be rendered within custom-themed layouts, shown in iframes for visual isolation, with a
site-configurable ThemedLayout component.

## User Stories

- As a component library developer, I want to preview my components within my project's custom layout so that I can see
  them in their actual design context
- As a site administrator, I want to define a ThemedLayout once at the site level so that all stories automatically use
  my brand's styling

## Specific Requirements

**Site ThemedLayout Configuration**

- Add optional `themed_layout` property to Site dataclass accepting a callable component (with `__call__()` method)
- If `themed_layout` is None, fall back to standard Storyville Layout component
- ThemedLayout must render full HTML structure (DOCTYPE, html, head, body tags)
- Property type should be `Callable[..., Node] | None` following existing callable patterns

**ThemedStory Component**

- Create new component accepting `story_title` (str) and `children` (Node) as props
- Component wraps children in the site's configured ThemedLayout
- Follows dataclass structure with `__call__() -> Node` pattern like existing Layout
- Passes full HTML structure through ThemedLayout for complete document rendering
- Uses modern type hints (`str | None`, `Node | None`) per Python 3.14+ standards

**Dual HTML File Generation**

- Generate two files per story in `story-X/` directory: `index.html` and `themed_story.html`
- `index.html` contains StoryView with iframe pointing to `./themed_story.html` (relative path)
- `themed_story.html` contains ThemedStory rendering with full HTML document
- iframe element styled with sensible defaults (100% width, min-height, border)
- Maintain existing story directory naming convention (`story-0`, `story-1`, etc.)

**Build Integration**

- Modify `build.py` to generate both HTML files during Phase 3 (Writing)
- ThemedStory rendering happens after StoryView rendering in Phase 2
- Pass `story.title` and `story.instance` to ThemedStory component
- Check `site.themed_layout` and use it if present, otherwise use standard Layout
- No performance impact on existing single-file story rendering

**Example ThemedLayout Implementation**

- Create at `examples/minimal/themed_layout/themed_layout.py`
- Implement as dataclass with `story_title` and `children` props
- Render complete HTML with custom head (CSS links, meta tags) and body structure
- Demonstrate full HTML document pattern with DOCTYPE and lang attribute
- Show how to pass through children content while wrapping in custom layout
- Include minimal CSS styling to demonstrate theming capability

## Existing Code to Leverage

**Site Dataclass (`src/storyville/site/models.py`)**

- Use existing Site dataclass structure with `parent`, `items`, `static_dir` fields
- Add new optional field `themed_layout: Callable[..., Node] | None = None`
- Follow existing `__post_init__` pattern for initialization logic
- Maintain compatibility with existing Site construction

**Layout Component (`src/storyville/components/layout/layout.py`)**

- Reference dataclass structure with `view_title`, `site`, `children`, `depth` parameters
- Follow `__call__() -> Node` rendering pattern
- Use tdom html t-string templates for markup generation
- Replicate full HTML document structure (DOCTYPE, html, head, body)
- Apply similar static asset path calculation if needed in themed layouts

**StoryView (`src/storyville/story/views.py`)**

- Leverage existing dual-mode rendering pattern (custom template vs default layout)
- Add third mode for iframe rendering when themed_layout is configured
- Wrap iframe in existing StoryView layout structure with breadcrumbs
- Maintain assertion badge rendering in parent StoryView (not in iframe)

**Build Process (`src/storyville/build.py`)**

- Extend `_write_html()` helper for writing both story files
- Add themed story rendering after existing story rendering in Phase 2
- Write themed_story.html files in same loop as story index.html files in Phase 3
- Maintain three-phase architecture (Reading, Rendering, Writing)

**Story Model (`src/storyville/story/models.py`)**

- Use existing `story.title` property for ThemedStory title prop
- Use existing `story.instance` property for ThemedStory children content
- Leverage `story.target` and `story.props` for component instantiation
- No modifications needed to Story dataclass itself

## Out of Scope

- Multiple theme support or theme switching UI (roadmap item #20)
- Theme inheritance or composition patterns
- Theme configuration via external files or JSON
- Per-section or per-subject theme overrides
- Theme preview selector in story viewer
- Advanced iframe communication or resize handling
- Custom iframe styling beyond basic defaults
- Theme marketplace or sharing features
