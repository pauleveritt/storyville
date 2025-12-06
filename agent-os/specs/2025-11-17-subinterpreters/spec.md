# Specification: Subinterpreters for Hot Reloading

## Goal

Enable hot reloading of Python modules (particularly stories.py) during development by running builds in isolated
subinterpreters, allowing fresh module imports on each rebuild while maintaining compatibility with both CLI and web
server workflows.

## User Stories

- As a developer, I want changes to stories.py files to take effect immediately when I save them, so that I can see my
  updates without restarting the server
- As a CLI user, I want simple builds without subinterpreter overhead, so that one-off builds remain fast and
  straightforward

## Specific Requirements

**Subinterpreter Pool Management**

- Use Python 3.14+ InterpreterPoolExecutor to manage a pool of 2 subinterpreters
- One interpreter is active for building, one is warming up as standby
- Create and shutdown the pool in app.py's lifespan context manager
- Pool initialization happens on Starlette app startup, shutdown on app teardown
- Use asyncio.to_thread to run synchronous subinterpreter work from async context

**Interpreter Warm-Up Strategy**

- Pre-import storyville and tdom modules in warm-up phase to reduce build latency
- Hard-code these imports in a warm-up function (no dynamic configuration needed)
- Warm-up happens immediately after pool creation and after each interpreter is pulled
- Warm-up function must be a module-level callable compatible with InterpreterPoolExecutor

**Build Execution in Subinterpreters**

- Wrap build_site function to run in subinterpreter when use_subinterpreters=True
- Subinterpreter executes full build pipeline: import modules, render views, write to disk
- No result passing needed - subinterpreter writes directly to filesystem
- After each build, discard the used subinterpreter and pull fresh from pool
- Immediately warm up a replacement interpreter to maintain pool size of 2

**Dual-Mode Operation**

- Add use_subinterpreters boolean parameter to create_app function (default: False)
- Add --use-subinterpreters command-line flag to serve command
- CLI mode (build command): Always use direct build_site without subinterpreters
- Web app mode: Use subinterpreters by default
- Support different callback signatures: sync for CLI, async-compatible for web app

**Integration with File Watcher**

- Modify watch_and_rebuild to accept async-compatible rebuild callback when in subinterpreter mode
- In web app mode with subinterpreters, wrap build execution in asyncio.to_thread
- Maintain existing error handling: log errors, continue watching even on build failure
- Keep existing broadcast behavior: only broadcast reload after successful build

**Error Handling and Logging**

- Log subinterpreter pool creation and shutdown events
- Log warm-up phase completion for each interpreter
- Log build errors from subinterpreters (don't show in browser)
- Continue watching and maintain pool even if builds fail
- Handle subinterpreter exceptions gracefully without crashing the watcher

## Visual Design

No visual assets provided - this is a backend infrastructure feature.

## Existing Code to Leverage

**build.py - build_site function**

- Current signature: build_site(package_location: str, output_dir: Path) -> None
- Performs three phases: Reading (import modules), Rendering (generate HTML), Writing (save to disk)
- Uses make_site which imports all stories.py modules via import_module
- This function should be wrapped for subinterpreter execution, not modified directly
- Existing logging infrastructure for build phases should work in subinterpreter

**watchers.py - watch_and_rebuild function**

- Current signature accepts rebuild_callback: Callable[[str, Path], None]
- Runs rebuild_callback synchronously from async context
- Has error handling that continues watching even on build failure
- Needs to support async-compatible callback when in subinterpreter mode
- Existing debouncing and change detection logic should remain unchanged

**app.py - lifespan context manager**

- Creates watcher tasks on app startup, cancels on shutdown
- Pattern to follow: create InterpreterPoolExecutor on startup, shutdown on app teardown
- Uses asyncio.create_task for background tasks
- Pool should be created before watcher task, shutdown after watcher is cancelled

**app.py - create_app function**

- Current parameters: path, input_path, package_location, output_dir
- Add use_subinterpreters boolean parameter
- Pass this flag to lifespan context manager
- Conditionally create pool and use subinterpreter-wrapped build callback

**__main__.py - CLI commands**

- serve command creates app with hot reload support
- build command runs build_site once without server
- Add --use-subinterpreters flag to serve command only
- build command should never use subinterpreters (always direct build_site)

## Out of Scope

- Showing build errors in the browser WebSocket interface
- Configurable pool size (fixed at 2)
- Dynamic warm-up module configuration (hard-coded storyville and tdom)
- Performance monitoring or metrics for subinterpreter overhead
- Parallel builds across multiple subinterpreters
- Support for Python versions below 3.14
- Persisting interpreters across multiple builds (always discard after use)
- Custom exception handling beyond logging
- Configuration files for subinterpreter settings
- Environment variable-based configuration
