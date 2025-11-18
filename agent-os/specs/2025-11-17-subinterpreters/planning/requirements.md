# Spec Requirements: Subinterpreters for Hot Reloading

## Initial Description

**Feature: Subinterpreters for Hot Reloading**

Problem: Our server process detects changes and rebuilds, but changes to stories.py don't have an effect, since the module is already imported.

Solution: Run the build process in a subinterpreter using InterpreterPoolExecutor. The subinterpreter can do the imports and then be thrown away. The next build can start with a new subinterpreter.

Key requirements:
- Use InterpreterPoolExecutor to run builds in isolated subinterpreters
- Consider having a pool so the next interpreter is ready to go
- Warm up the pending interpreter by having it do some common imports such as `import storytime`
- When it is time to build, it can import everything in the input_dir package
- Have good integration in Starlette
- Reference: https://blog.changs.co.uk/subinterpreters-and-asyncio.html

## Requirements Discussion

### First Round Questions

**Q1:** Should we use the InterpreterPoolExecutor for managing the subinterpreter pool?
**Answer:** Yes, use InterpreterPoolExecutor.

**Q2:** What should the pool size be? I'm thinking a pool of 2 interpreters (one active, one warming up) would be good.
**Answer:** Pool size of 2 is good.

**Q3:** For warm-up imports, should we import storytime and tdom? Are there other modules that should be pre-imported?
**Answer:** Warm up should import storytime and tdom. Need to find a place to easily specify these imports in a way that is callable by the InterpreterPoolExecutor.

**Q4:** Should the build_site function be wrapped to run in a subinterpreter, or should we create a new API specifically for subinterpreter-based builds?
**Answer:** Use current API, not a new API. But make sure running from the CLI (outside of Starlette) works correctly.

**Q5:** Do we need to pass results back from the subinterpreter to the main interpreter, or just let the subinterpreter write files directly?
**Answer:** Don't need to pass back results - the subinterpreter does the writing to disk.

**Q6:** Should build errors in the subinterpreter be shown in the browser (via WebSocket), or just logged?
**Answer:** Don't need to show build errors in the browser for now.

**Q7:** After each build, should we discard the active subinterpreter and pull a fresh one from the pool, then immediately warm up a replacement?
**Answer:** Yes, lifecycle is correct - discard current active subinterpreter and pull fresh from pool, then warm up replacement.

**Q8:** Should we have comprehensive tests covering: pool initialization, warm-up behavior, build execution in subinterpreter, module isolation verification, error handling?
**Answer:** Yes to all testing. Also: Can we support a no-subinterpreter mode for the CLI and a subinterpreter mode for the web app?

**Q9:** Are there any specific edge cases we should exclude from the initial implementation?
**Answer:** No specific edge cases to exclude.

### Existing Code to Reference

**Codebase Analysis:**

The following existing code provides context for the implementation:

1. **Build Pipeline**: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/build.py`
   - `build_site(package_location: str, output_dir: Path)` function handles the full build process
   - Calls `make_site(package_location)` which imports all stories.py modules via `import_module()`
   - This is the function that needs to run in a subinterpreter when in web app mode

2. **File Watching**: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/watchers.py`
   - `watch_and_rebuild()` async function detects file changes and calls rebuild_callback
   - Currently passes `build_site` as the rebuild_callback
   - Will need to be updated to call subinterpreter-wrapped version when in web app mode

3. **Starlette Integration**: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/app.py`
   - `lifespan()` context manager starts watcher on app startup
   - `create_app()` creates Starlette application with hot reload support
   - Integration point for subinterpreter pool initialization and shutdown

4. **CLI**: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/__main__.py`
   - `serve()` command runs build_site then starts Starlette server
   - `build()` command runs build_site once
   - CLI should continue using direct build_site (no subinterpreters) for simplicity

5. **Module Import Mechanism**: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/site/helpers.py` and `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/nodes.py`
   - `make_site()` finds all stories.py files and creates TreeNode instances
   - TreeNode calls `import_module(module_path)` to import each stories.py
   - This is where module caching becomes problematic - modules stay imported across rebuilds
   - Subinterpreters will solve this by providing a fresh import environment each time

**Similar Features Identified:**

User has not identified similar features to reference for this new functionality.

### Follow-up Questions

**Follow-up 1:** For the dual-mode requirement (CLI without subinterpreters vs web app with subinterpreters), how should we configure this? Options:
- A. Add a boolean flag parameter to `create_app()` like `use_subinterpreters=True`
- B. Auto-detect based on whether hot-reload parameters are provided
- C. Environment variable like `STORYTIME_USE_SUBINTERPRETERS`
- D. Different approach?

**Answer:** Use option A - Add a boolean flag parameter to `create_app()` like `use_subinterpreters=True` AND add a command-line flag.

**Follow-up 2:** For specifying warm-up imports (storytime and tdom), what's the best approach? Options:
- A. Hard-code the imports in the warm-up function
- B. Accept a list of module names as a parameter to the pool/warm-up function
- C. Read from a configuration file
- D. Use an environment variable
- E. Different approach?

**Answer:** Use option A - Hard-code the imports (storytime and tdom) in the warm-up function (simplest, works for now).

**Follow-up 3:** Where should the InterpreterPoolExecutor be created and managed?
- A. Created in `app.py`'s lifespan context manager (starts with app, stops with app)
- B. Created as a global singleton that's initialized on first use
- C. Created in a new module dedicated to subinterpreter management
- D. Different approach?

**Answer:** Use option A - Create InterpreterPoolExecutor in `app.py`'s lifespan context manager (starts with app, stops with app).

**Follow-up 4:** How should we handle the rebuild_callback signature to support both modes? The watcher currently expects `rebuild_callback(package_location: str, output_dir: Path) -> None`. For subinterpreter mode, we need this to be async-compatible. Options:
- A. Make rebuild_callback async and use `asyncio.to_thread()` for sync build_site
- B. Keep rebuild_callback sync but wrap subinterpreter execution internally
- C. Have two different callback signatures (one for CLI, one for web app)
- D. Different approach?

**Answer:** Use option C - Have two different callback signatures (one for CLI, one for web app).

## Visual Assets

### Files Provided:

No visual assets provided.

### Visual Insights:

N/A - This is a backend/infrastructure feature.

## Requirements Summary

### Functional Requirements

**Core Functionality:**
- Use Python 3.13+ subinterpreters via InterpreterPoolExecutor to run builds in isolated environments
- Maintain a pool of 2 subinterpreters (one active for building, one warming up as standby)
- Warm up interpreters by pre-importing storytime and tdom modules (hard-coded in warm-up function)
- After each build, discard the used subinterpreter and pull fresh from pool
- Immediately warm up a replacement interpreter to maintain pool size
- Subinterpreters write directly to disk (no result passing needed)
- Module imports happen fresh in each build (solving the module caching problem)

**Dual-Mode Operation:**
- **CLI Mode** (storytime build, storytime serve): Use direct build_site() without subinterpreters for simplicity
- **Web App Mode** (hot-reload server): Use subinterpreter-wrapped build_site() for proper module isolation
- Configuration via `use_subinterpreters` boolean flag parameter in `create_app()`
- Command-line flag to control subinterpreter usage
- Two different callback signatures to support both modes

**Integration Points:**
- Integrate with existing `build_site()` function without creating new API
- Work with existing file watcher (`watch_and_rebuild()`)
- InterpreterPoolExecutor created and managed in `app.py`'s lifespan context manager
- Maintain compatibility with existing WebSocket hot-reload broadcasting

**Error Handling:**
- Build errors should be logged (not shown in browser for now)
- Continue watching even if build fails in subinterpreter

**Testing Requirements:**
- Test pool initialization and shutdown
- Test warm-up behavior and module pre-loading
- Test build execution in subinterpreter
- Test module isolation (verify imports are fresh each time)
- Test error handling and recovery
- Test both CLI mode (no subinterpreters) and web app mode (with subinterpreters)

### Reusability Opportunities

**Existing Code to Leverage:**
- `build_site()` function - wrap this for subinterpreter execution rather than creating new API
- `watch_and_rebuild()` - update to use subinterpreter-wrapped build when in web app mode
- Starlette `lifespan()` context manager - use for pool lifecycle management
- Existing logging infrastructure for build phases and errors

**Patterns to Follow:**
- Async/await patterns already established in watchers.py and app.py
- Error handling and logging patterns from build.py
- Lifecycle management patterns from app.py's lifespan context manager

### Scope Boundaries

**In Scope:**
- InterpreterPoolExecutor-based subinterpreter management
- Pool of 2 interpreters with warm-up capability
- Dual-mode operation (CLI vs web app) configured via boolean flag and command-line flag
- Hard-coded warm-up imports (storytime and tdom)
- Pool creation in app.py's lifespan context manager
- Two different callback signatures for dual-mode support
- Integration with existing build and watch infrastructure
- Comprehensive testing of pool behavior and module isolation
- Error logging

**Out of Scope:**
- Showing build errors in the browser (future enhancement)
- Configurable pool size (fixed at 2 for now)
- Dynamic warm-up module configuration (hard-coded for now)
- Performance monitoring/metrics for subinterpreter overhead
- Support for parallel builds across multiple subinterpreters

### Technical Considerations

**Technology Requirements:**
- Python 3.13+ (for subinterpreters support)
- InterpreterPoolExecutor from concurrent.futures (or appropriate subinterpreter library)
- Async/await compatibility with existing Starlette infrastructure

**Key Constraints:**
- Must work with existing build_site() API
- Must maintain CLI simplicity (no subinterpreters in CLI mode)
- Must integrate cleanly with Starlette lifecycle
- Subinterpreters write directly to filesystem (no serialization of results)

**Implementation Decisions:**
- Configuration: Boolean flag parameter `use_subinterpreters` in `create_app()` + command-line flag
- Warm-up imports: Hard-coded (storytime and tdom) in warm-up function
- Pool management: Created in `app.py`'s lifespan context manager
- Callback signatures: Two different signatures (one for CLI, one for web app)

### Key Reference

External documentation: https://blog.changs.co.uk/subinterpreters-and-asyncio.html
