# Task Breakdown: Subinterpreters for Hot Reloading

## Overview

Total Tasks: 23 tasks organized into 4 major groups
Estimated Complexity: Medium-High (infrastructure change with careful integration)

## Task List

### Core Infrastructure: Subinterpreter Pool Management

#### Task Group 1: Pool Creation and Lifecycle

**Dependencies:** None

- [x] 1.0 Complete subinterpreter pool infrastructure
    - [x] 1.1 Write 2-8 focused tests for pool lifecycle
        - Limit to 2-8 highly focused tests maximum
        - Test pool creation, warm-up execution, and shutdown
        - Test interpreter availability after warm-up
        - Skip exhaustive coverage of edge cases
    - [x] 1.2 Create warm-up function module
        - Create `src/storytime/subinterpreters.py` for subinterpreter utilities
        - Implement `warmup_interpreter()` as module-level callable
        - Hard-code imports: `import storytime` and `import tdom`
        - Must be compatible with `InterpreterPoolExecutor.submit()`
        - Add logging for warm-up completion
    - [x] 1.3 Create pool initialization function
        - Implement `create_interpreter_pool()` returning `InterpreterPoolExecutor`
        - Pool size: exactly 2 interpreters
        - Initialize pool and warm up both interpreters immediately
        - Use Python 3.14+ `concurrent.futures.InterpreterPoolExecutor`
        - Add logging for pool creation event
    - [x] 1.4 Create pool shutdown function
        - Implement `shutdown_interpreter_pool(pool: InterpreterPoolExecutor)`
        - Graceful shutdown with timeout
        - Add logging for shutdown event
        - Handle exceptions during shutdown gracefully
    - [x] 1.5 Ensure pool infrastructure tests pass
        - Run ONLY the 2-8 tests written in 1.1
        - Verify pool creates successfully with 2 interpreters
        - Verify warm-up completes without errors
        - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**

- The 2-8 tests written in 1.1 pass
- Pool creates with exactly 2 interpreters
- Warm-up function successfully imports storytime and tdom
- Pool shuts down gracefully
- All logging events captured

**Notes:**

- Reference: https://blog.changs.co.uk/subinterpreters-and-asyncio.html
- Use modern Python 3.14+ type hints (PEP 604 syntax: `X | Y`)
- Follow structural pattern matching where applicable

---

### Build Execution: Subinterpreter Integration

#### Task Group 2: Build Wrapping and Execution

**Dependencies:** Task Group 1

- [ ] 2.0 Complete build execution in subinterpreters
    - [ ] 2.1 Write 2-8 focused tests for build execution
        - Limit to 2-8 highly focused tests maximum
        - Test build runs successfully in subinterpreter
        - Test output files are written correctly
        - Test module isolation (fresh imports on each build)
        - Skip exhaustive testing of all build scenarios
    - [ ] 2.2 Create subinterpreter build wrapper function
        - Implement `build_in_subinterpreter(pool: InterpreterPoolExecutor, package_location: str, output_dir: Path)` in
          `subinterpreters.py`
        - Submit build task to pool using `pool.submit()`
        - Execute full `build_site()` pipeline in subinterpreter
        - Subinterpreter writes directly to filesystem (no result passing)
        - Add logging for build start/completion in subinterpreter
    - [ ] 2.3 Implement interpreter discard and replacement
        - After each build completes, discard used interpreter
        - Pull fresh interpreter from pool
        - Immediately warm up replacement interpreter to maintain pool size of 2
        - Handle pool exhaustion gracefully
    - [ ] 2.4 Add error handling for subinterpreter builds
        - Catch exceptions from subinterpreter execution
        - Log errors without crashing watcher or pool
        - Continue pool operation even if build fails
        - Don't propagate build errors to browser (log only)
    - [ ] 2.5 Ensure build execution tests pass
        - Run ONLY the 2-8 tests written in 2.1
        - Verify builds complete successfully in subinterpreters
        - Verify module isolation works (modules reimported fresh)
        - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**

- The 2-8 tests written in 2.1 pass
- `build_site()` executes successfully in subinterpreter
- Files written to disk by subinterpreter are correct
- Module isolation verified (changes to stories.py take effect)
- Errors logged but don't crash pool or watcher
- Pool maintains 2 interpreters after builds

**Notes:**

- Do NOT modify `build_site()` function signature or internals
- Wrap existing `build_site()` for subinterpreter execution
- Verify existing logging infrastructure works in subinterpreter

---

### Integration: Dual-Mode Operation

#### Task Group 3: App and Watcher Integration

**Dependencies:** Task Group 2

- [ ] 3.0 Complete dual-mode integration
    - [ ] 3.1 Write 2-8 focused tests for dual-mode operation
        - Limit to 2-8 highly focused tests maximum
        - Test CLI mode (direct build without subinterpreters)
        - Test web app mode (build with subinterpreters)
        - Test callback signature compatibility
        - Skip exhaustive testing of all integration scenarios
    - [ ] 3.2 Add `use_subinterpreters` parameter to `create_app()`
        - Update signature: `create_app(..., use_subinterpreters: bool = False)`
        - Default to `False` for backward compatibility
        - Pass flag to lifespan context manager
        - Located in: `src/storytime/app.py`
    - [ ] 3.3 Integrate pool lifecycle with Starlette lifespan
        - In `lifespan()` context manager in `app.py`
        - Create pool on app startup (before watcher) if `use_subinterpreters=True`
        - Shutdown pool on app teardown (after watcher cancelled)
        - Store pool reference in app state for access by watcher
        - Add logging for lifecycle events
    - [ ] 3.4 Update `watch_and_rebuild()` for dual callbacks
        - Modify signature to support both sync and async-compatible callbacks
        - When `use_subinterpreters=True`: use `asyncio.to_thread()` to run subinterpreter build
        - When `use_subinterpreters=False`: use direct `build_site()` call
        - Maintain existing error handling and debouncing
        - Keep existing WebSocket broadcast behavior (only after successful build)
        - Located in: `src/storytime/watchers.py`
    - [ ] 3.5 Wire up subinterpreter callback in web app mode
        - In `app.py`, when `use_subinterpreters=True`
        - Create async-compatible callback that calls `build_in_subinterpreter()`
        - Pass callback to `watch_and_rebuild()`
        - Use `asyncio.to_thread()` to run synchronous subinterpreter work
    - [ ] 3.6 Ensure integration tests pass
        - Run ONLY the 2-8 tests written in 3.1
        - Verify CLI mode works (no subinterpreters)
        - Verify web app mode works (with subinterpreters)
        - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**

- The 2-8 tests written in 3.1 pass
- `create_app()` accepts `use_subinterpreters` boolean parameter
- Pool lifecycle integrated with Starlette app lifecycle
- Watcher supports both direct and subinterpreter builds
- Callbacks work correctly in both modes
- WebSocket broadcasts still work after successful builds

**Notes:**

- Maintain backward compatibility (default: no subinterpreters)
- Follow existing async/await patterns in `watchers.py` and `app.py`
- Don't break existing file watching and debouncing logic

---

### CLI Integration: Command-Line Interface

#### Task Group 4: CLI Commands and Flags

**Dependencies:** Task Group 3

- [ ] 4.0 Complete CLI integration
    - [ ] 4.1 Write 2-8 focused tests for CLI integration
        - Limit to 2-8 highly focused tests maximum
        - Test `serve` command with and without `--use-subinterpreters`
        - Test `build` command always uses direct build
        - Skip exhaustive CLI testing
    - [ ] 4.2 Add `--use-subinterpreters` flag to serve command
        - Update `serve()` in `src/storytime/__main__.py`
        - Add click option: `@click.option('--use-subinterpreters', is_flag=True, default=False)`
        - Pass flag value to `create_app(use_subinterpreters=...)`
        - Add help text explaining flag purpose
    - [ ] 4.3 Verify build command uses direct build
        - Ensure `build()` command in `__main__.py` always calls `build_site()` directly
        - Never use subinterpreters for CLI build (no flag needed)
        - Keep build command simple and fast
    - [ ] 4.4 Add CLI usage documentation
        - Document `--use-subinterpreters` flag in docstring/help
        - Explain when to use flag (development with hot reload)
        - Explain default behavior (no subinterpreters for simplicity)
    - [ ] 4.5 Ensure CLI integration tests pass
        - Run ONLY the 2-8 tests written in 4.1
        - Verify serve command works with and without flag
        - Verify build command always uses direct build
        - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**

- The 2-8 tests written in 4.1 pass
- `serve` command accepts `--use-subinterpreters` flag
- Flag defaults to `False` for backward compatibility
- `build` command never uses subinterpreters
- CLI help text is clear and accurate

**Notes:**

- Use click's standard flag patterns
- Maintain simplicity for CLI users
- Default behavior should match current behavior (no breaking changes)

---

### Testing and Quality

#### Task Group 5: Test Review & Gap Analysis

**Dependencies:** Task Groups 1-4

- [ ] 5.0 Review existing tests and fill critical gaps only
    - [ ] 5.1 Review tests from Task Groups 1-4
        - Review the 2-8 tests written for pool infrastructure (Task 1.1)
        - Review the 2-8 tests written for build execution (Task 2.1)
        - Review the 2-8 tests written for dual-mode integration (Task 3.1)
        - Review the 2-8 tests written for CLI integration (Task 4.1)
        - Total existing tests: approximately 8-32 tests
    - [ ] 5.2 Analyze test coverage gaps for THIS feature only
        - Identify critical workflows lacking coverage
        - Focus ONLY on subinterpreter feature requirements
        - Prioritize integration and end-to-end scenarios
        - Key areas: module isolation verification, error recovery, pool state management
    - [ ] 5.3 Write up to 10 additional strategic tests maximum
        - Add maximum of 10 new tests to fill critical gaps
        - Focus on: module reimport verification, concurrent build handling, pool recovery after errors
        - Test edge cases: pool exhaustion, interpreter failures, file system errors
        - Test integration: full rebuild cycle with file changes
        - Skip: performance tests, stress tests, exhaustive error scenarios
    - [ ] 5.4 Run feature-specific tests only
        - Run ONLY tests related to subinterpreter feature
        - Expected total: approximately 18-42 tests maximum
        - Do NOT run the entire application test suite
        - Verify all critical workflows pass
    - [ ] 5.5 Run quality checks
        - Run `just test` (feature-specific tests only)
        - Run `just typecheck` (verify type hints)
        - Run `just fmt` (format code)
        - All checks must pass

**Acceptance Criteria:**

- All feature-specific tests pass (approximately 18-42 tests total)
- Critical workflows verified: hot reload with module changes, dual-mode operation, error recovery
- No more than 10 additional tests added when filling gaps
- Type checking passes with modern Python 3.14+ type hints
- Code formatted according to project standards
- Testing focused exclusively on subinterpreter feature

**Notes:**

- Follow test structure in `tests/` directory
- Use descriptive test names: `test_<functionality>_<scenario>`
- Test behavior, not implementation
- Mock external dependencies where appropriate
- Keep tests fast (milliseconds)

---

## Execution Order

Recommended implementation sequence:

1. **Task Group 1: Pool Creation and Lifecycle** (Core infrastructure)
2. **Task Group 2: Build Wrapping and Execution** (Build integration)
3. **Task Group 3: App and Watcher Integration** (Dual-mode operation)
4. **Task Group 4: CLI Commands and Flags** (User-facing interface)
5. **Task Group 5: Test Review & Gap Analysis** (Quality assurance)

## Key Design Decisions

- **Pool Size:** Fixed at 2 interpreters (one active, one warming up)
- **Warm-up Imports:** Hard-coded `storytime` and `tdom` modules
- **Configuration:** Boolean flag `use_subinterpreters` in `create_app()` + CLI flag
- **Lifecycle:** Pool managed in Starlette's lifespan context manager
- **Callback Signatures:** Dual signatures (sync for CLI, async-compatible for web app)
- **Error Handling:** Log errors, don't crash pool or watcher, don't show in browser

## Technical Requirements

- Python 3.14+ for `InterpreterPoolExecutor` support
- Modern type hints: PEP 604 syntax (`X | Y`), PEP 695 generics
- Async/await compatibility with Starlette
- No modifications to `build_site()` internals
- Maintain backward compatibility (default: no subinterpreters)

## Out of Scope

- Showing build errors in browser WebSocket interface
- Configurable pool size
- Dynamic warm-up module configuration
- Performance monitoring or metrics
- Parallel builds across multiple subinterpreters
- Support for Python versions below 3.14
- Persisting interpreters across builds
- Custom exception handling beyond logging
- Configuration files or environment variables
