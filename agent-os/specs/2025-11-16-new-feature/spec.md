# Specification: Hot Reload Development Server

## Goal

Add automatic browser refresh capability to Storyville's development server by watching source files for changes and
notifying connected browsers via WebSocket to reload when files are modified.

## User Stories

- As a developer, I want my browser to automatically refresh when I modify Python or static files so that I can see
  changes immediately without manual page reload
- As a developer, I want the build process to automatically run when source files change so that my rendered HTML stays
  in sync with my components

## Specific Requirements

**Dual Watch System Architecture**

- Create two independent file watchers using the `watchfiles` package
- INPUT watcher monitors `src/storyville/` directory and triggers rebuild on changes
- OUTPUT watcher monitors the rendered HTML output directory (e.g., temp build directory) and sends WebSocket reload
  messages
- Integrate watchers into Starlette app lifecycle using Starlette's lifespan context manager
- This may require keeping the Site instance around for the duration of the server lifecycle
- Use modern Python 3.14+ async/await patterns for the watcher tasks

**INPUT Directory Watcher**

- Monitor TWO directories for changes:
    1. **Content directory**: Monitor the `input_path` argument (where user content is located) recursively for any file
       changes
    2. **Storyville static assets**: Monitor `src/storyville/` (if it exists) but ONLY for static file changes (`.css`,
       `.js`, `.png`, `.jpg`, `.svg`, `.ico`, etc.)
- If anything in either watched location changes, trigger a full rebuild
- For content directory: watch all file types
- For Storyville directory: only watch static assets (not `.py` files)
- Ignore Python cache files (`.pyc`, `__pycache__`) and other temporary/build artifacts in both locations
- When changes detected in either location, invoke the existing `build_site()` function to regenerate the output
- Implement simple server-side debouncing to avoid multiple rebuilds when many files change at once

**OUTPUT Directory Watcher**

- Monitor the output directory (where `build_site()` writes rendered HTML) for any file changes
- Watch all files in the output directory tree without filtering by extension
- When changes detected (from rebuild or manual edits), broadcast reload message to all connected WebSocket clients
- Implement simple server-side debouncing to avoid sending multiple reload messages when many files change at once

**WebSocket Server Integration**

- Add WebSocket endpoint to Starlette application at `/ws/reload` using Starlette's built-in WebSocket support
- Accept WebSocket connections from browsers and maintain list of active connections
- Broadcast simple JSON message `{"type": "reload"}` to all connected clients when OUTPUT watcher detects changes
- Handle client disconnections gracefully and clean up connection list
- Use async WebSocket handlers compatible with Starlette patterns

**WebSocket Client JavaScript**

- Inject client-side JavaScript into all generated HTML pages via the Layout component
- JavaScript establishes WebSocket connection to `/ws/reload` on page load
- Implement client-side debouncing (e.g., 300ms) to prevent rapid-fire reloads if server sends multiple messages
- On receiving `{"type": "reload"}` message, execute `window.location.reload()` after debounce delay
- Implement simple exponential backoff-reconnect logic when connection is lost (e.g., retry after 1s, 2s, 4s, max 30s)
- Handle connection errors silently - no user-visible error messages
- Keep implementation minimal with no visual indicators or connection state UI

**Serve Command Enhancement**

- Modify the `serve` command in `__main__.py` to integrate watchers into Starlette app lifecycle
- Use Starlette's lifespan context manager to start/stop watcher tasks with the application
- Pass necessary paths (input package location, output directory) to watcher functions
- Ensure graceful shutdown of all tasks on Ctrl+C or server termination
- Maintain existing uvicorn configuration (port 8080, log level info)
- May need to keep Site instance around for the duration of the server lifecycle

**JavaScript Injection into Layout**

- Update the `Layout` component in `components/layout/layout.py` to inject WebSocket client script
- Add inline `<script>` tag before closing `</body>` tag with complete WebSocket client code
- Use relative WebSocket URL (e.g., `ws://localhost:8080/ws/reload`) or construct from current window.location
- Ensure script only runs in development mode (always inject for now, future enhancement could add mode flag)

**Build System Integration**

- Leverage existing `build_site()` function from `build.py` without modification
- INPUT watcher calls `build_site()` with same parameters used by serve command
- Handle build errors gracefully - log errors but don't crash watcher process
- Continue watching for changes even if a build fails

**File Path Configuration**

- INPUT path: Use existing `input_path` argument from serve command (defaults to "storyville")
- OUTPUT path: Use existing temporary directory from serve command's `TemporaryDirectory()` context
- WebSocket endpoint: Fixed at `/ws/reload` relative to server root
- No configuration file or environment variables needed

**Error Handling and Logging**

- Log watcher start/stop events to console for debugging
- INPUT watcher must log detected changes showing which files changed for developer visibility
- OUTPUT watcher should NOT log individual file changes (too noisy during rebuilds)
- Log build success/failure when INPUT watcher triggers rebuild
- Log WebSocket broadcast events when OUTPUT watcher sends reload messages
- Handle WebSocket connection errors silently without crashing server
- Use Python's built-in logging module consistent with uvicorn's logging
- Ensure all watcher events appear in Starlette/uvicorn console output

**Testing Strategy**

- Write integration tests that simulate the rebuild watcher behavior
- Test approach: Write to a temporary directory, fire up the watching logic WITHOUT Starlette, make a change, and verify
  output directory reflects the change
- This testing requirement may prompt refactoring of builder/server logic to make watcher testable in isolation
- Add a pytest marker `slow` in `pyproject.toml` `[tool.pytest.ini_options]` section:
  `markers = ["slow: marks tests as slow (deselect with '-m \"not slow\"')"]`
- Mark these watcher integration tests with `@pytest.mark.slow` decorator
- Tests should verify:
    - File changes in content directory trigger rebuild
    - Static asset changes in `src/storyville/` trigger rebuild
    - Output directory is updated with new content
    - Watcher can be started and stopped cleanly

## Visual Design

No visual assets provided. The feature operates transparently with no UI changes beyond automatic page refresh behavior.

## Existing Code to Leverage

**Starlette Application (`app.py`)**

- Use existing `create_app()` function that returns configured Starlette instance
- Add WebSocket route to the routes list: `WebSocketRoute("/ws/reload", websocket_endpoint)`
- Keep `debug=True` for helpful error pages, but ensure uvicorn does NOT use `--reload` flag
- Do not use Starlette/uvicorn's built-in auto-reload - we have our own custom file watching
- Follow existing Mount pattern for routes
- Integrate watchfiles into Starlette lifecycle using lifespan context manager for startup/shutdown
- This ensures watchers start when the app starts and stop cleanly when the app shuts down

**Build System (`build.py`)**

- Reuse `build_site()` function exactly as-is for rebuilding on file changes
- Function signature: `build_site(package_location: str, output_dir: Path) -> None`
- No modifications needed to build.py - INPUT watcher calls this directly

**Serve Command (`__main__.py`)**

- Extend existing `serve()` command to launch watcher tasks
- Maintain `TemporaryDirectory` context manager for output directory
- Keep existing uvicorn.run() call but wrap in async context with watchers
- Ensure uvicorn does NOT use `reload=True` or `--reload` flag - we use custom file watching instead
- Preserve existing CLI arguments (input_path) and defaults

**Layout Component (`components/layout/layout.py`)**

- Inject WebSocket client script into existing HTML structure
- Add script tag before closing `</body>` tag in the `__call__()` method's template
- Use existing tdom t-string syntax for clean HTML interpolation

**Static File Handling (Site model)**

- Reference existing `static_dir` pattern from `Site.static_dir` (set to `components/layout/static`)
- Static assets already copied by `build_site()` - no changes needed
- Watcher will detect changes to files in this directory

## Out of Scope

- Visual indicators for connection status or reconnecting states in the browser UI
- State persistence across page reloads
- Hot module replacement or selective component reloading without full page refresh
- Sending file change metadata in WebSocket messages (file paths, timestamps, change types)
- Configuration files or environment variables for watch patterns or debounce timing
- Production mode or feature flags to disable hot reload in production builds
- Cross-browser compatibility testing beyond modern evergreen browsers
- Performance optimization for large file trees or high-frequency changes
- Unit tests for watcher processes (integration test only for core flow)
- Command-line flags to disable/enable hot reload
- Custom rebuild strategies or incremental builds
- Watching files outside INPUT and OUTPUT directories
- Browser notifications or console logging of reload events
