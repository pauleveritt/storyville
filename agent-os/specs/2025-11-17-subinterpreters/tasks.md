# Task Breakdown: Subinterpreters for Hot Reloading

## Overview

Total Tasks: 23 tasks organized into 5 major groups
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

- [x] 2.0 Complete build execution in subinterpreters
    - [x] 2.1 Write 2-8 focused tests for build execution
        - Limit to 2-8 highly focused tests maximum
        - Test build runs successfully in subinterpreter
        - Test output files are written correctly
        - Test module isolation (fresh imports on each build)
        - Skip exhaustive testing of all build scenarios
    - [x] 2.2 Create subinterpreter build wrapper function
        - Implement `build_in_subinterpreter(pool: InterpreterPoolExecutor, package_location: str, output_dir: Path)` in
          `subinterpreters.py`
        - Submit build task to pool using `pool.submit()`
        - Execute full `build_site()` pipeline in subinterpreter
        - Subinterpreter writes directly to filesystem (no result passing)
        - Add logging for build start/completion in subinterpreter
    - [x] 2.3 Implement interpreter discard and replacement
        - After each build completes, discard used interpreter
        - Pull fresh interpreter from pool
        - Immediately warm up replacement interpreter to maintain pool size of 2
        - Handle pool exhaustion gracefully
    - [x] 2.4 Add error handling for subinterpreter builds
        - Catch exceptions from subinterpreter execution
        - Log errors without crashing watcher or pool
        - Continue pool operation even if build fails
        - Don't propagate build errors to browser (log only)
    - [x] 2.5 Ensure build execution tests pass
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

- [x] 3.0 Complete dual-mode integration
    - [x] 3.1 Write 2-8 focused tests for dual-mode operation
        - Limit to 2-8 highly focused tests maximum
        - Test CLI mode (direct build without subinterpreters)
        - Test web app mode (build with subinterpreters)
        - Test callback signature compatibility
        - Skip exhaustive testing of all integration scenarios
    - [x] 3.2 Add `use_subinterpreters` parameter to `create_app()`
        - Update signature: `create_app(..., use_subinterpreters: bool = False)`
        - Default to `False` for backward compatibility
        - Pass flag to lifespan context manager
        - Located in: `src/storytime/app.py`
    - [x] 3.3 Integrate pool lifecycle with Starlette lifespan
        - In `lifespan()` context manager in `app.py`
        - Create pool on app startup (before watcher) if `use_subinterpreters=True`
        - Shutdown pool on app teardown (after watcher cancelled)
        - Store pool reference in app state for access by watcher
        - Add logging for lifecycle events
    - [x] 3.4 Update `watch_and_rebuild()` for dual callbacks
        - Modify signature to support both sync and async-compatible callbacks
        - When `use_subinterpreters=True`: use `asyncio.to_thread()` to run subinterpreter build
        - When `use_subinterpreters=False`: use direct `build_site()` call
        - Maintain existing error handling and debouncing
        - Keep existing WebSocket broadcast behavior (only after successful build)
        - Located in: `src/storytime/watchers.py`
    - [x] 3.5 Wire up subinterpreter callback in web app mode
        - In `app.py`, when `use_subinterpreters=True`
        - Create async-compatible callback that calls `build_in_subinterpreter()`
        - Pass callback to `watch_and_rebuild()`
        - Use `asyncio.to_thread()` to run synchronous subinterpreter work
    - [x] 3.6 Ensure integration tests pass
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

- [x] 4.0 Complete CLI integration
    - [x] 4.1 Write 2-8 focused tests for CLI integration
        - Limit to 2-8 highly focused tests maximum
        - Test `serve` command with and without `--use-subinterpreters`
        - Test `build` command always uses direct build
        - Skip exhaustive CLI testing
    - [x] 4.2 Add `--use-subinterpreters` flag to serve command
        - Update `serve()` in `src/storytime/__main__.py`
        - Add typer option: `typer.Option(False, '--use-subinterpreters', help=...)`
        - Pass flag value to `create_app(use_subinterpreters=...)`
        - Add help text explaining flag purpose
    - [x] 4.3 Verify build command uses direct build
        - Ensure `build()` command in `__main__.py` always calls `build_site()` directly
        - Never use subinterpreters for CLI build (no flag needed)
        - Keep build command simple and fast
    - [x] 4.4 Add CLI usage documentation
        - Document `--use-subinterpreters` flag in docstring/help
        - Explain when to use flag (development with hot reload)
        - Explain default behavior (no subinterpreters for simplicity)
    - [x] 4.5 Ensure CLI integration tests pass
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

- Use typer's standard flag patterns
- Maintain simplicity for CLI users
- Default behavior should match current behavior (no breaking changes)

---

### Testing and Quality

#### Task Group 5: Test Review & Gap Analysis

**Owner:** QA Engineer
**Dependencies:** Task Groups 1-4 (all core functionality must be implemented)

- [x] **Task 5.1:** Review all tests created in previous task groups
  - Review tests/subinterpreter/test_pool.py (4 tests)
  - Review tests/subinterpreter/test_build_execution.py (5 tests)
  - Review tests/subinterpreter/test_integration.py (6 tests)
  - Review tests/subinterpreter/test_cli.py (3 tests)
  - Total: 18 tests so far
  - Identify any gaps or missing scenarios

- [x] **Task 5.2:** Perform gap analysis on test coverage
  - Check edge cases: concurrent builds, rapid rebuilds, large projects
  - Check error scenarios: pool exhaustion, timeout handling, cleanup failures
  - Check integration: WebSocket broadcasts, watcher debouncing
  - Maximum 10 additional tests to add (keep focused)
  - Document findings

- [x] **Task 5.3:** Add strategic tests for identified gaps (max 10 tests)
  - Focus on high-value scenarios not covered
  - Test real-world usage patterns
  - Add to appropriate test files (pool, build_execution, integration, or new file)
  - Ensure all new tests pass

- [x] **Task 5.4:** Run full test suite and verify quality
  - Execute: `just test` (all tests)
  - Execute: `just typecheck` (type checking)
  - Execute: `just fmt` (formatting)
  - All checks must pass
  - Total test count should be ~18-28 subinterpreter tests + existing tests

- [x] **Task 5.5:** Document test coverage and completion
  - Create summary of test coverage
  - Document any known limitations or edge cases not tested
  - Update tasks.md with completion status
  - Prepare for final verification

**Acceptance Criteria:**
- All tests from Task Groups 1-4 reviewed and verified working
- Gap analysis completed and documented
- High-priority gaps addressed with strategic tests (max 10 additional)
- Full test suite passes (just test, just typecheck, just fmt)
- Test coverage documented
- Total of 18-28 focused subinterpreter tests

**Results:**
- **Total Tests:** 28 subinterpreter tests (18 original + 10 strategic gap-filling tests)
- **All Tests Pass:** ✓ 28 passed in 3.53s
- **Type Checking:** ✓ All checks passed
- **Code Formatting:** ✓ All checks passed
- **Test Coverage Summary:** Created at `agent-os/specs/2025-11-17-subinterpreters/verification/test-coverage-summary.md`

**Strategic Tests Added:**
1. `test_concurrent_builds_handling` - Concurrent builds with pool size 2
2. `test_rapid_rebuilds_with_debouncing` - 5 rapid sequential rebuilds
3. `test_build_timeout_handling` - Build timeout enforcement and recovery
4. `test_pool_recovery_after_multiple_failures` - Pool resilience after errors
5. `test_filesystem_error_handling` - Read-only directory handling
6. `test_module_state_isolation_between_builds` - Global state isolation
7. `test_error_recovery_full_cycle` - Full error -> recovery workflow
8. `test_async_callback_error_propagation` - Async error handling
9. `test_pool_cleanup_on_shutdown_with_pending_work` - Graceful shutdown
10. `test_end_to_end_watcher_rebuild_flow` - Complete integration test

---

## Execution Order

Recommended implementation sequence:

1. **Task Group 1: Pool Creation and Lifecycle** (Core infrastructure) ✓
2. **Task Group 2: Build Wrapping and Execution** (Build integration) ✓
3. **Task Group 3: App and Watcher Integration** (Dual-mode operation) ✓
4. **Task Group 4: CLI Commands and Flags** (User-facing interface) ✓
5. **Task Group 5: Test Review & Gap Analysis** (Quality assurance) ✓

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
