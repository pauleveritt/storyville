# Architecture

This document explains the key architectural decisions and design patterns in Storytime.

## Overview

Storytime is built around a tree-based component catalog system with hot reloading capabilities, powered by Python 3.14+ subinterpreters and modern async patterns.

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

Storytime uses Python 3.14+ `InterpreterPoolExecutor` for true module reloading without process restarts.

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
    import storytime
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

### WebSocket Live Reload

Browser connects to WebSocket endpoint for instant reload notifications.

**Flow:**

1. Browser opens WebSocket connection to `/ws`
2. File watcher detects changes
3. Build executes in subinterpreter
4. On success, server broadcasts `{"type": "reload"}`
5. Browser receives message and triggers page reload

**Client-Side:**

```javascript
const ws = new WebSocket('ws://localhost:8080/ws');
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'reload') {
        location.reload();
    }
};
```

**Benefits:**

- Instant visual feedback (no polling)
- Low bandwidth (only sends on actual changes)
- Resilient (auto-reconnects on disconnect)
- Works through page reloads

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
storytime = "storytime.pytest_plugin"
```

Pytest automatically loads the plugin when storytime is installed.

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
- Maintains standard Storytime UI (breadcrumbs, assertions, props)

## Type System

Storytime uses modern Python 3.14+ type features extensively.

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

## Testing Architecture

Storytime itself is thoroughly tested using pytest.

### Test Organization

```
tests/
├── conftest.py              # Shared fixtures
├── test_models.py           # Data model tests
├── test_story.py            # Story rendering tests
├── test_examples.py         # Integration tests with examples
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

### Design Philosophy

- Minimal dependencies
- Stable, well-maintained libraries
- Modern Python (3.14+) features reduce need for backport libraries
- No transpilation or build tools needed

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

Storytime's architecture emphasizes:

- **Simplicity**: Tree-based hierarchy is easy to understand
- **Safety**: Strong typing and automatic HTML escaping
- **Performance**: Subinterpreters enable fast hot reload
- **Flexibility**: Pluggable themes, custom templates, extensible assertions
- **Developer Experience**: Instant feedback, automatic tests, clear error messages

The use of modern Python features (3.14+) enables clean, readable code while providing excellent performance and safety guarantees.
