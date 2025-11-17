# Task Breakdown: Hot Reload Development Server

## Overview

Total Tasks: 5 Task Groups with approximately 30-40 sub-tasks

This feature adds automatic browser refresh capability using WebSocket-based file watching. The implementation uses a
dual-watcher architecture: INPUT watcher monitors source files and triggers rebuilds, OUTPUT watcher monitors build
output and triggers browser reloads.

## Task List

### Task Group 1: WebSocket Client JavaScript

**Dependencies:** None

- [x] 1.0 Complete WebSocket client JavaScript
    - [x] 1.1 Write 2-8 focused tests for client behavior
        - Test WebSocket connection establishment
        - Test reload message handling
        - Test client-side debouncing (300ms)
        - Test reconnection with exponential backoff
        - Use JavaScript testing framework or manual browser testing
        - Limit to critical client behaviors only
    - [x] 1.2 Create inline JavaScript for WebSocket client
        - Implement connection to `/ws/reload` endpoint
        - Use `window.location` to construct WebSocket URL (ws:// or wss:// based on protocol)
        - Handle `{"type": "reload"}` message format
        - Implement client-side debouncing (300ms delay before reload)
        - Execute `window.location.reload()` on message
    - [x] 1.3 Implement reconnection logic
        - Add exponential backoff: retry after 1s, 2s, 4s, up to max 30s
        - Handle connection close and error events
        - Automatically reconnect on connection loss
        - No user-visible error messages or connection state UI
    - [x] 1.4 Keep implementation minimal
        - No visual indicators or connection status UI
        - Silent error handling
        - Minimal console logging (optional for debugging)
    - [x] 1.5 Ensure client tests pass
        - Run ONLY the 2-8 tests written in 1.1
        - Verify critical client behaviors work
        - Do NOT run full integration tests at this stage

**Acceptance Criteria:**

- The 2-8 client tests pass
- WebSocket connects to `/ws/reload`
- Reload messages trigger page refresh with debouncing
- Reconnection works with exponential backoff
- Implementation is minimal with no UI

### Task Group 2: Layout Component Script Injection

**Dependencies:** Task Group 1 (needs client JavaScript code)

- [x] 2.0 Complete layout modification
    - [x] 2.1 Write 2-8 focused tests for script injection
        - Test that `<script>` tag is present in rendered HTML
        - Test script appears before closing `</body>` tag
        - Test script references WebSocket client JavaScript file
        - Test script works at different depths (depth=0, 1, 2)
        - Use existing test patterns from `layout_test.py`
        - Limit to critical injection behaviors only
    - [x] 2.2 Modify Layout component in `src/storytime/components/layout/layout.py`
        - Inject `<script src="{ws_script_path}"></script>` tag before closing `</body>`
        - Reference WebSocket client JavaScript from static/ws.js
        - Use tdom t-string syntax for clean HTML interpolation
        - Follow existing Layout structure and patterns
    - [x] 2.3 Test script injection with different depths
        - Verify script works at depth=0 (site root) with path ../static/ws.js
        - Verify script works at depth=1 (section pages) with path ../../static/ws.js
        - Verify script works at depth=2 (subject pages) with path ../../../static/ws.js
        - Ensure WebSocket URL construction is relative and works at all depths
    - [x] 2.4 Ensure layout tests pass
        - Run ONLY the 6 tests written in 2.1
        - Verify script injection works correctly
        - All quality checks pass (test, typecheck, fmt)

**Acceptance Criteria:**

- The 6 layout tests pass
- Script tag is injected before `</body>`
- Script references /static/ws.js with correct relative path based on depth
- Script works at all page depths (0, 1, 2)
- Follows existing Layout patterns
- All quality checks pass (test, typecheck, fmt)

### Task Group 3: WebSocket Server Endpoint

**Dependencies:** None (can be developed in parallel with Task Groups 1-2)

- [ ] 3.0 Complete WebSocket server endpoint
    - [ ] 3.1 Write 2-8 focused tests for WebSocket endpoint
        - Test WebSocket connection acceptance at `/ws/reload`
        - Test broadcasting reload message to connected clients
        - Test handling multiple simultaneous connections
        - Test graceful disconnection and cleanup
        - Use Starlette's TestClient or WebSocket testing utilities
        - Limit to critical server behaviors only
    - [ ] 3.2 Create WebSocket endpoint handler
        - Add WebSocket endpoint function for `/ws/reload`
        - Accept WebSocket connections using Starlette's WebSocket class
        - Maintain list/set of active WebSocket connections
        - Implement async WebSocket handler compatible with Starlette
        - Follow Starlette WebSocket patterns
    - [ ] 3.3 Implement broadcast functionality
        - Create function to broadcast messages to all connected clients
        - Send JSON message `{"type": "reload"}` format
        - Handle client disconnections during broadcast
        - Clean up disconnected clients from connection list
        - Use async iteration and error handling
    - [ ] 3.4 Integrate WebSocket route into app
        - Modify `src/storytime/app.py` to add WebSocketRoute
        - Add route: `WebSocketRoute("/ws/reload", websocket_endpoint)`
        - Maintain existing StaticFiles mount and debug=True
        - Follow existing routing patterns
    - [ ] 3.5 Ensure WebSocket tests pass
        - Run ONLY the 2-8 tests written in 3.1
        - Verify WebSocket connections and broadcasting work
        - Do NOT run entire test suite at this stage

**Acceptance Criteria:**

- The 2-8 WebSocket tests pass
- WebSocket endpoint accepts connections at `/ws/reload`
- Broadcast sends reload message to all connected clients
- Disconnections are handled gracefully
- Route is integrated into Starlette app

### Task Group 4: File Watchers and Rebuild Logic

**Dependencies:** Task Group 3 (needs WebSocket broadcast functionality)

- [ ] 4.0 Complete file watcher implementation
    - [ ] 4.1 Write 2-8 focused integration tests for watchers
        - Mark tests with `@pytest.mark.slow` decorator
        - Add pytest marker to `pyproject.toml`:
          `markers = ["slow: marks tests as slow (deselect with '-m \"not slow\"')"]`
        - Test INPUT watcher detects content directory changes
        - Test INPUT watcher detects static asset changes in `src/storytime/`
        - Test OUTPUT watcher detects build output changes
        - Test watchers can be started and stopped cleanly
        - Use temporary directories and simulate file changes
        - Tests should run WITHOUT Starlette (isolated watcher logic)
        - Limit to critical watcher workflows only
    - [ ] 4.2 Create INPUT directory watcher
        - Use `watchfiles` package for async file watching
        - Monitor TWO directories:
            1. Content directory (input_path argument) - watch all file types
            2. `src/storytime/` - watch ONLY static files (`.css`, `.js`, `.png`, `.jpg`, `.svg`, `.ico`)
        - Ignore Python cache files (`.pyc`, `__pycache__`)
        - Implement server-side debouncing to avoid multiple rebuilds
        - When changes detected, call `build_site()` function
        - Use modern Python 3.14+ async/await patterns
    - [ ] 4.3 Implement rebuild trigger
        - Call existing `build_site(package_location, output_dir)` on file changes
        - Handle build errors gracefully (log but don't crash)
        - Continue watching after build failures
        - Log file change events and build success/failure
        - Use Python's logging module consistent with uvicorn
    - [ ] 4.4 Create OUTPUT directory watcher
        - Use `watchfiles` package for async file watching
        - Monitor output directory (where `build_site()` writes HTML)
        - Watch all files without filtering by extension
        - Implement server-side debouncing to avoid multiple reload messages
        - When changes detected, broadcast reload to WebSocket clients
        - Use modern Python 3.14+ async/await patterns
    - [ ] 4.5 Implement broadcast integration
        - Call WebSocket broadcast function from Task Group 3
        - Send `{"type": "reload"}` message to all connected clients
        - Handle broadcast errors gracefully
        - Log reload events for developer visibility
    - [ ] 4.6 May require refactoring for testability
        - Extract watcher logic into testable functions
        - Allow watchers to run independently of Starlette
        - Enable dependency injection for build and broadcast functions
        - Maintain clean separation of concerns
    - [ ] 4.7 Ensure watcher tests pass
        - Run ONLY the 2-8 slow tests written in 4.1
        - Use `pytest -m slow` to run marked tests
        - Verify watchers detect changes and trigger actions
        - Do NOT run entire test suite at this stage

**Acceptance Criteria:**

- The 2-8 slow integration tests pass
- INPUT watcher monitors both content and static directories
- File changes trigger rebuild via `build_site()`
- OUTPUT watcher monitors build output directory
- Output changes trigger WebSocket broadcast
- Debouncing prevents rapid-fire actions
- Watchers can be tested in isolation

### Task Group 5: Starlette Lifespan Integration and Serve Command

**Dependencies:** Task Groups 3-4 (needs WebSocket endpoint and watchers)

- [ ] 5.0 Complete lifespan integration and serve command
    - [ ] 5.1 Write 2-8 focused tests for lifespan and serve integration
        - Test Starlette app starts with lifespan
        - Test watchers start during app startup
        - Test watchers stop during app shutdown
        - Test Site instance persists for server lifecycle
        - Test graceful shutdown on SIGTERM/SIGINT
        - Use Starlette TestClient with lifespan context
        - Limit to critical integration behaviors only
    - [ ] 5.2 Create Starlette lifespan context manager
        - Implement async lifespan function for Starlette app
        - Use `@asynccontextmanager` decorator
        - Start INPUT and OUTPUT watcher tasks on startup
        - Stop watcher tasks on shutdown
        - Follow Starlette lifespan patterns
        - Integrate into `create_app()` in `src/storytime/app.py`
    - [ ] 5.3 Manage Site instance lifecycle
        - Keep Site instance around for server duration
        - Pass Site or necessary paths to watcher functions
        - Ensure Site is available for rebuilds
        - May require refactoring `create_app()` signature
    - [ ] 5.4 Start watcher tasks in lifespan
        - Create asyncio tasks for INPUT and OUTPUT watchers
        - Pass input_path and output_dir to INPUT watcher
        - Pass output_dir to OUTPUT watcher
        - Store task references for cleanup on shutdown
        - Use `asyncio.create_task()` for background execution
    - [ ] 5.5 Implement graceful shutdown
        - Cancel watcher tasks on app shutdown
        - Wait for tasks to complete with timeout
        - Clean up resources (file handles, WebSocket connections)
        - Log shutdown events
        - Handle Ctrl+C (SIGINT) gracefully
    - [ ] 5.6 Modify serve command in `src/storytime/__main__.py`
        - Integrate watchers via Starlette lifespan (not direct uvicorn changes)
        - Maintain TemporaryDirectory context manager
        - Keep existing uvicorn.run() call
        - Ensure uvicorn does NOT use `reload=True` flag
        - Maintain existing CLI arguments and defaults
        - Pass paths to create_app() for lifespan use
    - [ ] 5.7 Update create_app() signature if needed
        - May need to accept input_path parameter
        - May need to accept package_location for rebuilds
        - Maintain backward compatibility with existing tests
        - Update test fixtures accordingly
    - [ ] 5.8 Ensure serve integration tests pass
        - Run ONLY the 2-8 tests written in 5.1
        - Verify app starts and stops cleanly with watchers
        - Do NOT run entire test suite at this stage

**Acceptance Criteria:**

- The 2-8 serve integration tests pass
- Lifespan context manager starts/stops watchers
- Site instance persists for server duration
- Watcher tasks run in background during server operation
- Graceful shutdown cancels tasks and cleans up
- Serve command integrates watchers without modifying uvicorn reload
- uvicorn does NOT use built-in `--reload` flag

### Task Group 6: Final Integration Testing and Quality Checks

**Dependencies:** All previous task groups (1-5)

- [ ] 6.0 Review existing tests and fill critical gaps
    - [ ] 6.1 Review tests from Task Groups 1-5
        - Review client JavaScript tests (Task 1.1)
        - Review layout injection tests (Task 2.1)
        - Review WebSocket server tests (Task 3.1)
        - Review watcher integration tests (Task 4.1)
        - Review lifespan/serve tests (Task 5.1)
        - Total existing tests: approximately 10-40 tests
    - [ ] 6.2 Analyze test coverage gaps for hot reload feature
        - Identify critical end-to-end workflows lacking coverage
        - Focus ONLY on gaps related to hot reload functionality
        - Prioritize integration scenarios over unit test gaps
        - Do NOT assess entire application coverage
    - [ ] 6.3 Write up to 10 additional strategic tests maximum
        - Add maximum of 10 new tests to fill critical gaps
        - Focus on end-to-end hot reload workflow:
            - File change -> rebuild -> output change -> WebSocket message -> browser reload
            - Multiple simultaneous file changes with debouncing
            - Static asset changes vs content changes
            - Error handling during rebuild
            - WebSocket reconnection after server restart
        - Do NOT write comprehensive coverage for all scenarios
        - Skip edge cases unless business-critical
    - [ ] 6.4 Run feature-specific tests
        - Run all tests related to hot reload feature only
        - Use `pytest -m slow` to include slow watcher tests
        - Expected total: approximately 20-50 tests maximum
        - Do NOT run entire application test suite
        - Verify all critical workflows pass
    - [ ] 6.5 Run quality checks
        - Execute `just test` (feature-specific tests)
        - Execute `just typecheck` (ensure type hints are correct)
        - Execute `just fmt` (format code)
        - All checks must pass
    - [ ] 6.6 Manual end-to-end testing
        - Start server with `storytime serve`
        - Verify browser connects via WebSocket
        - Modify a Python content file, verify rebuild and reload
        - Modify a static CSS file, verify rebuild and reload
        - Modify a build output file directly, verify reload only
        - Test reconnection by restarting server
        - Verify no errors in browser console or server logs

**Acceptance Criteria:**

- All feature-specific tests pass (approximately 20-50 tests)
- No more than 10 additional tests added for gap filling
- Type checking passes with no errors
- Code is properly formatted
- Manual end-to-end workflow verified
- Hot reload works for content, static, and output changes
- Browser reconnects gracefully on server restart

## Execution Order

Recommended implementation sequence:

1. **Task Group 1: WebSocket Client JavaScript** (parallel with Group 3)
    - Can be developed independently
    - Provides client-side foundation

2. **Task Group 2: Layout Component Script Injection** (depends on Group 1)
    - Requires client JavaScript from Group 1
    - Enables browser-side reload capability

3. **Task Group 3: WebSocket Server Endpoint** (parallel with Group 1)
    - Can be developed independently
    - Provides server-side communication foundation

4. **Task Group 4: File Watchers and Rebuild Logic** (depends on Group 3)
    - Requires WebSocket broadcast from Group 3
    - Implements core file watching and rebuild logic
    - May require refactoring for testability

5. **Task Group 5: Starlette Lifespan Integration and Serve Command** (depends on Groups 3-4)
    - Requires WebSocket endpoint and watchers
    - Integrates all components into server lifecycle
    - Modifies serve command for watcher integration

6. **Task Group 6: Final Integration Testing and Quality Checks** (depends on Groups 1-5)
    - Validates complete feature
    - Fills critical test gaps
    - Runs quality checks and manual testing

## Important Notes

### Testing Philosophy

- **Focused tests during development**: Each task group writes 2-8 tests maximum covering only critical behaviors
- **Slow test marker**: Watcher integration tests use `@pytest.mark.slow` and can be run separately
- **Isolated watcher tests**: Watcher tests run WITHOUT Starlette to enable faster iteration
- **Final integration**: Task Group 6 adds up to 10 strategic tests for end-to-end workflows
- **Total test count**: Approximately 20-50 tests for entire hot reload feature

### Technical Constraints

- **Python 3.14+ standards**: Use modern async/await, type hints (PEP 604, 695), pattern matching
- **No uvicorn reload flag**: Custom file watching instead of uvicorn's built-in reload
- **Starlette lifespan**: Watchers integrated via lifespan context manager, not standalone processes
- **Dual-directory monitoring**: INPUT watcher monitors both content and Storytime static directories
- **Debouncing**: Both server-side (watcher) and client-side (JavaScript) debouncing
- **Graceful error handling**: Build failures and WebSocket errors don't crash server

### Dependencies

- `watchfiles>=1.1.1`: Already in pyproject.toml
- `starlette>=0.50.0`: Already in pyproject.toml
- `uvicorn>=0.38.0`: Already in pyproject.toml

### Refactoring Considerations

- Task Group 4 may prompt refactoring of builder/server logic for testability
- `create_app()` may need signature changes to support lifespan parameters
- Site instance lifecycle management may require architectural changes
- Watcher logic should be extractable for isolated testing
