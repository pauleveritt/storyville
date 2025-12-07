# Architecture

This document explains the key architectural decisions and design patterns in Storyville.

## Overview

Storyville is built around a tree-based component catalog system with hot reloading capabilities, powered by Python 3.14+ subinterpreters and modern async patterns.

## Core Architecture Patterns

### Tree-Based Hierarchy

The component catalog follows a hierarchical tree structure:

```
Catalog (root)
  ├─ Section (optional grouping)
  │   └─ Subject (component)
  │       └─ Story (variation)
  └─ Subject (top-level component)
      └─ Story (variation)
```

**Design Decisions:**

- **BaseNode Pattern**: All tree nodes inherit from `BaseNode` providing parent/child relationships
- **TreeNode Protocol**: Defines common interface for traversable nodes (Catalog, Section, Subject)
- **Auto-discovery**: Stories are discovered by scanning for `stories.py` files using `Path.rglob()`
- **Dotted Path Navigation**: Use `find_path(catalog, ".section.subject.story")` for traversal

**Benefits:**

- Clean separation of concerns (catalog organization vs component definition)
- Flexible hierarchy (sections are optional)
- Easy navigation and programmatic access to any node

### Component Rendering System

Components are rendered using the tdom library with automatic safety and type handling.

**Key Classes:**

- **Story**: Represents a component variation with props and assertions
- **Story.instance**: Property that renders the component with given props
- **StoryView**: Default template for displaying stories in the browser

**Rendering Modes:**

1. **Mode A (Custom Template)**: Story has custom `template` callable
2. **Mode B (Default Layout)**: Standard StoryView with PicoCSS styling
3. **Mode C (Themed Iframe)**: Story rendered in custom ThemedLayout within iframe

**Type Safety:**

- All rendering goes through tdom's Node system
- Automatic HTML escaping for strings
- Support for Node, Markup, and string types
- Type hints enforce correct usage

## Hot Reload Architecture

### Subinterpreter Pool

Storyville uses Python 3.14+ `InterpreterPoolExecutor` for true module reloading without process restarts.

**Pool Design:**

- Pool size: 2 subinterpreters
- 1 active (running current build)
- 1 standby (pre-warmed and ready)

**Lifecycle:**

1. Application starts → Create pool of 2 interpreters
2. File change detected → Pull standby interpreter
3. Execute build in pulled interpreter
4. Discard used interpreter (single-use only)
5. Immediately warm up replacement interpreter

**Pre-warming Strategy:**

Standby interpreters pre-import core modules to reduce latency:

```python
def _warmup_interpreter():
    import storyville
    import tdom
```

This reduces first-build latency from ~500ms to ~100ms overhead.

**Why Not Reuse Interpreters?**

- Fresh imports guarantee no stale module cache
- Prevents subtle bugs from persisted state
- Memory is freed after each build
- Simplifies error recovery

### File Watching

Uses `watchfiles` library for efficient file change detection.

**Architecture:**

- Async watcher runs in background task
- Debouncing prevents rapid rebuild on multiple saves
- Watches Python files recursively in package directory
- Only rebuilds on actual file modifications (not access/metadata changes)

**Integration with Subinterpreters:**

```python
# In watch_and_rebuild
async def rebuild_callback():
    # Run build in subinterpreter via thread pool
    await asyncio.to_thread(
        pool.submit(build_catalog, package_location, output_dir)
    )
```

The watcher uses `asyncio.to_thread` to bridge async event loop with synchronous subinterpreter execution.

**Error Handling:**

- Build errors are logged but don't stop watching
- Browser keeps current (working) version on build failure
- WebSocket only broadcasts reload on successful build

### Granular Change Detection

The hot reload system implements intelligent change detection that tracks currently-viewed pages, filters changes by story relevance, and uses either iframe reload or DOM morphing based on what changed.

#### Page Tracking System

**WebSocket Connection State:**

When a browser connects via WebSocket, it immediately sends page metadata to the server:

```javascript
// Client-side: ws.mjs
{
  type: "page_info",
  page_url: "/components/heading/story-0/index.html",
  page_type: "story",  // or "non_story"
  story_id: "components/heading/story-0"
}
```

**Server-Side Connection Metadata:**

```python
# websocket.py
_connection_metadata: dict[WebSocket, PageMetadata] = {}

@dataclass
class PageMetadata:
    page_url: str
    page_type: PageType  # STORY, STORY_CONTAINER, NON_STORY
    story_id: str | None = None
```

The server maintains a mapping of each WebSocket connection to its page metadata, allowing targeted broadcasts.

**Page Type Classification:**

- **STORY**: Story pages with iframe (Mode C) - receives story-specific and global updates
- **STORY_CONTAINER**: The themed_story.html content within iframe - not tracked separately
- **NON_STORY**: Documentation, section indexes, catalog pages - receives non-story updates only

#### Change Classification System

When files change, the watcher classifies them into three categories:

**1. Global Assets** (affects all story pages):
- `themed_story.html` - the template wrapper for all story content
- CSS files in `static/` directories (e.g., `static/bundle.css`)
- JavaScript files in `static/` directories (e.g., `static/ws.mjs`)

**2. Story-Specific** (affects individual stories):
- Individual story `index.html` files (e.g., `components/heading/story-0/index.html`)
- Story identifier extracted from path: `components/heading/story-0`

**3. Non-Story** (affects documentation and indexes):
- Documentation pages (e.g., `docs/getting-started.html`)
- Section index pages (e.g., `components/index.html`)
- Catalog index page (`index.html`)

**Classification Logic:**

```python
# watchers.py
def classify_change(changed_path: Path) -> tuple[ChangeType, str | None]:
    # Check for themed_story.html
    if changed_path.name == "themed_story.html":
        return ChangeType.GLOBAL_ASSET, None

    # Check for CSS/JS in static directories
    if "static" in parts and suffix in {".css", ".js", ".mjs"}:
        return ChangeType.GLOBAL_ASSET, None

    # Check for story-specific index.html
    if changed_path.name == "index.html" and "story-" in path:
        story_id = extract_story_id_from_path(changed_path)
        return ChangeType.STORY_SPECIFIC, story_id

    # Everything else is non-story content
    return ChangeType.NON_STORY, None
```

#### Targeted Broadcast System

The server sends different reload messages based on change classification:

**WebSocket Message Protocol:**

```python
@dataclass
class ReloadMessage:
    type: str  # Always "reload"
    change_type: str  # "iframe_reload", "morph_html", or "full_reload"
    story_id: str | None = None  # Present for story-specific changes
    html: str | None = None  # Present for morph_html changes
```

**Broadcast Targeting:**

1. **Story-Specific Changes** → `broadcast_story_reload(story_id, html)`
   - Filters: Only connections viewing the affected story
   - Message type: `morph_html`
   - Includes: Full HTML content for morphing

2. **Global Asset Changes** → `broadcast_global_reload()`
   - Filters: All connections with `page_type == STORY`
   - Message type: `iframe_reload`
   - No HTML payload needed

3. **Non-Story Changes** → `broadcast_full_reload()`
   - Filters: All connections with `page_type == NON_STORY`
   - Message type: `full_reload`
   - Triggers full page reload

**Filtering Logic:**

```python
# websocket.py
def broadcast_story_reload(story_id: str, html_content: str) -> None:
    """Broadcast story-specific reload to clients viewing that story."""
    message = ReloadMessage(
        type="reload",
        change_type="morph_html",
        story_id=story_id,
        html=html_content
    )

    for websocket, metadata in _connection_metadata.items():
        # Only send to clients viewing this specific story
        if metadata.page_type == PageType.STORY and metadata.story_id == story_id:
            websocket.send_text(message.to_json())
```

#### Client-Side Reload Strategies

The browser handles three types of reload messages:

**1. DOM Morphing** (`morph_html`):
- Used for: Story-specific HTML changes
- Preserves: Scroll position, interactive state
- Library: idiomorph (bundled locally in `static/idiomorph.js`)
- Target: Iframe content document body

```javascript
// ws.mjs
function morphDOM(html, storyId) {
    const iframe = document.querySelector('iframe[src="./themed_story.html"]');
    const iframeDoc = iframe.contentDocument;

    // Capture scroll position
    const scrollState = captureIframeScroll(iframe);

    // Parse new HTML
    const newDoc = new DOMParser().parseFromString(html, 'text/html');

    // Morph iframe body content
    Idiomorph.morph(iframeDoc.body, newDoc.body, {
        morphStyle: 'innerHTML'
    });

    // Restore scroll position
    restoreIframeScroll(iframe, scrollState);
}
```

**2. Iframe Reload** (`iframe_reload`):
- Used for: Global asset changes (CSS, JS, themed_story.html)
- Preserves: Scroll position via capture/restore
- Visual feedback: `.iframe-reloading` CSS class
- Target: Only the story iframe, not the full page

**3. Full Page Reload** (`full_reload`):
- Used for: Non-story pages, or as fallback
- Simple: `window.location.reload()`
- No state preservation

**Fallback Chain:**

Each reload strategy has fallbacks for resilience:

1. **Morph attempt fails** → Fall back to iframe reload
2. **Iframe reload fails** → Fall back to full page reload
3. **Unknown message type** → Fall back to full page reload

```javascript
// ws.mjs
function handleMorphHtml(html, storyId) {
    const morphSuccess = morphDOM(html, storyId);

    if (!morphSuccess) {
        if (!reloadIframe()) {
            window.location.reload();  // Final fallback
        }
    }
}
```

#### Change Detection Flow Diagram

```
File Change Detected (watchers.py)
    ↓
Classify Change (classify_change)
    ├─ Global Asset → broadcast_global_reload()
    │     ↓
    │  Filter: page_type == STORY
    │     ↓
    │  Send: {change_type: "iframe_reload"}
    │     ↓
    │  Client: reloadIframe()
    │
    ├─ Story-Specific → broadcast_story_reload(story_id, html)
    │     ↓
    │  Read HTML (read_story_html)
    │     ↓
    │  Filter: page_type == STORY && story_id matches
    │     ↓
    │  Send: {change_type: "morph_html", html: "..."}
    │     ↓
    │  Client: morphDOM(html)
    │     ├─ Success: Scroll preserved
    │     └─ Failure: Fallback to reloadIframe()
    │
    └─ Non-Story → broadcast_full_reload()
          ↓
       Filter: page_type == NON_STORY
          ↓
       Send: {change_type: "full_reload"}
          ↓
       Client: window.location.reload()
```

#### Logging and Debugging

**Server-Side Logging:**

```python
# Change classification
logger.debug("Change classified as STORY_SPECIFIC: story %s at %s", story_id, path)

# Broadcast targeting
logger.info("Broadcasting story reload to %d connections for story %s", count, story_id)

# Connection state
logger.debug("Stored page metadata for connection: %s", metadata)
```

**Client-Side Logging:**

```javascript
// Page info sent
console.log('[Storyville] Sending page info:', {page_url, page_type, story_id});

// Reload message received
console.log('[Storyville] Processing reload message:', {change_type, story_id});

// Morph operations
console.log('[Storyville] DOM morphing completed successfully');

// Fallback decisions
console.log('[Storyville] Morphing failed, falling back to iframe reload');
```

**Timestamp Correlation:**

All log messages include timestamps (automatically via Python's logging framework and JavaScript's console timestamps), allowing correlation of server-side change detection with client-side reload operations.

**Example Debug Session:**

```
# Server logs
[2025-12-06 10:15:23] Change classified as STORY_SPECIFIC: story components/heading/story-0
[2025-12-06 10:15:23] Broadcasting story reload to 1 connections

# Client logs
[10:15:23.456] [Storyville] WebSocket message received
[10:15:23.458] [Storyville] Processing reload message: {change_type: "morph_html", story_id: "components/heading/story-0"}
[10:15:23.462] [Storyville] DOM morphing completed successfully
```

#### Benefits of Granular Change Detection

**Performance:**
- Story-specific changes morph without full reload (instant, preserves state)
- Only affected clients receive updates (reduces unnecessary work)
- Scroll position and interactive state maintained

**Developer Experience:**
- Stay focused on the story you're editing
- No distraction from unrelated changes
- Instant visual feedback for story content changes
- Smooth transitions (no flash from full page reload)

**Reliability:**
- Multiple fallback levels ensure updates always work
- Connection state cleanup prevents memory leaks
- Graceful degradation if libraries fail to load

### WebSocket Live Reload

Browser connects to WebSocket endpoint for instant reload notifications.

**Flow:**

1. Browser opens WebSocket connection to `/ws/reload`
2. Browser sends page metadata (URL, type, story ID)
3. File watcher detects changes
4. Build executes in subinterpreter
5. On success, server classifies change and broadcasts targeted reload
6. Browser receives message and triggers appropriate reload strategy

**Client-Side:**

```javascript
const ws = new WebSocket('ws://localhost:8080/ws/reload');
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'reload') {
        handleReloadMessage(data);  // Routes based on change_type
    }
};
```

**Benefits:**

- Instant visual feedback (no polling)
- Low bandwidth (only sends on actual changes)
- Resilient (auto-reconnects on disconnect)
- Works through page reloads
- Targeted updates (only affected pages reload)

## Build Pipeline

The build process follows a three-phase architecture:

### Phase 1: Reading (Module Discovery)

```python
# Scan for stories.py files
catalog = make_catalog(package_location)
```

- Uses `Path.rglob("stories.py")` to find story modules
- Imports modules using `importlib.import_module()`
- Calls `this_subject()` and `this_section()` functions
- Builds tree structure with parent/child relationships

### Phase 2: Rendering (HTML Generation)

```python
# Render all views to HTML strings
rendered_catalog = CatalogView(catalog, catalog)()
rendered_sections = [SectionView(section, catalog)() for section in sections]
rendered_subjects = [SubjectView(subject, catalog)() for subject in subjects]
rendered_stories = [StoryView(story, catalog)() for story in stories]
```

- Each node has corresponding View class
- Views are callable dataclasses returning tdom Nodes
- Layout component wraps all views with consistent structure
- Themed stories generate additional `themed_story.html` files

### Phase 3: Writing (Disk Output)

```python
# Write HTML files to output directory
(output_dir / "index.html").write_text(str(rendered_catalog))
# ... write all other files
```

- Each node gets its own directory and `index.html`
- Stories get subdirectories: `story-0/`, `story-1/`, etc.
- Static assets copied from package `static/` directory
- Relative paths used for portability

**Why Three Phases?**

- Clear separation of concerns
- Easy to reason about and debug
- Testable in isolation
- Can swap implementations per phase

## Story Assertions System

Assertions provide both visual feedback and automatic test generation.

### Assertion Execution

Assertions are callables that receive rendered elements:

```python
type AssertionCallable = Callable[[Element | Fragment], None]
```

**Contract:**

- Input: Rendered component (tdom Element or Fragment)
- Output: None on success, raises AssertionError on failure
- Side effects: None (pure checking logic)

**Execution Flow:**

1. Story renders component via `story.instance`
2. Each assertion is called with rendered element
3. Results stored in `story.assertion_results`
4. Visual badges shown in browser (✓ or ✗)

### pytest Plugin Architecture

The pytest plugin automatically discovers and generates tests from assertions.

**Plugin Registration:**

```toml
[project.entry-points.pytest11]
storyville = "storyville.pytest_plugin"
```

Pytest automatically loads the plugin when storyville is installed.

**Collection Process:**

1. Plugin hooks into `pytest_collect_file`
2. Scans configured `story_paths` for `stories.py` files
3. Uses `make_catalog()` to build story tree
4. Generates one pytest Item per assertion
5. Test naming: `test_story[catalog.section.subject.story::Assertion N]`

**Fresh Rendering Per Test:**

- Each test renders the story fresh (no cached results)
- Ensures test isolation for parallel execution (pytest-xdist)
- Prevents state leakage between tests

**Failure Reporting:**

- Captures AssertionError with message
- Renders HTML of component
- Generates unified diff (expected vs actual)
- Includes story metadata (props, title)

## Themed Stories System

Themed stories allow components to be previewed within custom-themed layouts.

### Architecture

**Catalog Configuration:**

```python
@dataclass
class Catalog:
    themed_layout: Callable[[str, Node], Node] | None = None
```

The `themed_layout` is a callable that accepts:
- `story_title: str` - Title of the story
- `children: Node` - Rendered component

And returns a complete HTML document (tdom Node).

### Dual-File Generation

When themed layout is configured, each story generates two files:

1. **`story-N/index.html`**: StoryView with iframe
2. **`story-N/themed_story.html`**: Component in ThemedLayout

**Iframe Pattern:**

```html
<iframe src="./themed_story.html" style="width: 100%; min-height: 500px;"></iframe>
```

Uses relative path for portability when deploying static builds.

**Benefits:**

- Visual isolation (iframe prevents style leakage)
- Real-world context (see component in actual design system)
- Maintains standard Storyville UI (breadcrumbs, assertions, props)

## Type System

Storyville uses modern Python 3.14+ type features extensively.

### Type Aliases with `type` Statement

```python
type AssertionCallable = Callable[[Element | Fragment], None]
type AssertionResult = tuple[str, bool, str | None]
type Target = Callable[..., Node]
type Template = Callable[[Story, Catalog], Node]
```

**Benefits:**

- Clear, readable type definitions
- Better IDE support and type checking
- Follows PEP 695 generic syntax

### Union Types with `|`

```python
title: str | None = None
parent: Catalog | Section | None = None
items: dict[str, Section | Subject] = field(default_factory=dict)
```

Uses PEP 604 union syntax instead of `Union[]` or `Optional[]`.

### Generic Functions

```python
def find_path[T: TreeNode](catalog: Catalog, path: str) -> T | None:
    """Navigate tree using dotted path notation."""
```

Uses PEP 695 generic function syntax with type parameter.

## Static Site Generation

The build command generates a complete static site that can be deployed anywhere.

### Output Structure

```
output/
├── index.html                 # Catalog view
├── static/                    # Static assets
│   ├── pico.css
│   └── [user static files]
├── section-name/
│   ├── index.html            # Section view
│   └── subject-name/
│       ├── index.html        # Subject view
│       ├── story-0/
│       │   ├── index.html    # Story view
│       │   └── themed_story.html  # (if themed layout configured)
│       └── story-1/
│           ├── index.html
│           └── themed_story.html
```

### Portability

- All links use relative paths
- No hardcoded domain or protocol
- Static assets copied into output directory
- Self-contained (no external dependencies)

**Can be deployed to:**

- GitHub Pages
- Netlify
- Vercel
- Any static hosting service
- Local file system (file:// URLs work)

## Performance Considerations

### Subinterpreter Overhead

- Pool management: ~5-10ms per build
- Warm-up import time: ~100ms per interpreter
- Single-use pattern: Prevents memory accumulation

**Optimization:**

- Standby interpreter pre-warmed
- Minimal latency between file change and build start
- Tested with 300-story catalog: ~450-500ms rebuild time

### Build Optimization

- Assertions can be disabled with `--no-with-assertions`
- Skips assertion execution for faster rendering
- Useful during development when only checking visual appearance

### Tree Traversal

- O(n) traversal using generators
- Lazy evaluation where possible
- Path-based lookup uses dotted notation for efficiency

### Change Detection Overhead

- Change classification: ~1-5ms per file
- WebSocket broadcast: ~1-2ms per connection
- DOM morphing: ~10-50ms (faster than full reload)
- Debouncing prevents rapid successive operations (0.3s window)

## Testing Architecture

Storyville itself is thoroughly tested using pytest.

### Test Organization

```
tests/
├── conftest.py              # Shared fixtures
├── test_models.py           # Data model tests
├── test_story.py            # Story rendering tests
├── test_examples.py         # Integration tests with examples
├── test_websocket_connection_state.py  # WebSocket state management
├── test_change_classification.py       # Change detection logic
├── test_granular_change_detection_integration.py  # End-to-end workflows
├── test_watcher_broadcast_integration.py  # Watcher + broadcast integration
├── dom_morphing/
│   └── test_dom_morphing.py  # DOM morphing functionality
└── pytest_plugin/
    └── test_plugin.py       # Plugin tests
```

### Key Test Patterns

**Fixture-based component testing:**

```python
@pytest.fixture
def sample_story():
    def check_element_exists(el) -> None:
        assert el is not None, "Missing"

    return Story(
        props=dict(text="Test"),
        target=Button,
        assertions=[check_element_exists]
    )
```

**Integration testing with examples:**

Tests run against actual `examples/` directories to verify end-to-end functionality.

**Assertion testing:**

Uses `aria-testing` library to verify rendered HTML structure.

## Dependency Architecture

### Core Dependencies

- **tdom**: Templating and HTML generation (required)
- **Starlette**: Async web framework (required)
- **watchfiles**: File change detection (required)
- **pytest**: Testing framework (required for plugin)
- **idiomorph**: DOM morphing library (bundled locally)

### Design Philosophy

- Minimal dependencies
- Stable, well-maintained libraries
- Modern Python (3.14+) features reduce need for backport libraries
- No transpilation or build tools needed
- Local bundling for reliability (no CDN dependencies)

## Future Architecture Considerations

### Potential Enhancements

1. **Parallel Builds**: Use multiple subinterpreters simultaneously for large catalogs
2. **Incremental Builds**: Only rebuild changed components and their dependents
3. **Build Cache**: Persist rendered HTML between builds when source unchanged
4. **Visual Regression**: Integrate screenshot comparison for stories
5. **Component Search**: Index stories for fast full-text search

### Extension Points

- **Custom View Components**: Override default views (CatalogView, SectionView, etc.)
- **Build Plugins**: Hook into build pipeline phases
- **Custom Assertion Types**: Extend AssertionCallable with richer reporting
- **Theme Marketplace**: Shareable ThemedLayout components

## Summary

Storyville's architecture emphasizes:

- **Simplicity**: Tree-based hierarchy is easy to understand
- **Safety**: Strong typing and automatic HTML escaping
- **Performance**: Subinterpreters enable fast hot reload
- **Intelligence**: Granular change detection provides targeted updates
- **Flexibility**: Pluggable themes, custom templates, extensible assertions
- **Developer Experience**: Instant feedback, automatic tests, clear error messages

The use of modern Python features (3.14+) enables clean, readable code while providing excellent performance and safety guarantees. The granular change detection system ensures that developers see only relevant updates, with intelligent reload strategies that preserve state and maintain focus.
