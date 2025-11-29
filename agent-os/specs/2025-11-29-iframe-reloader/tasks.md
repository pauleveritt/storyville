# Task Breakdown: Iframe Reloader

## Overview
Total Task Groups: 4
Focus: Enable fast, smooth hot reloading for Mode C story views by reloading only the iframe content instead of the full page.

## Task List

### JavaScript Core Logic

#### Task Group 1: Mode Detection and Conditional Reload
**Dependencies:** None
**Files to modify:** `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/static/ws.js`

- [x] 1.0 Implement iframe reload logic in ws.js
  - [x] 1.1 Write 2-8 focused tests for iframe reload functionality
    - Test Mode C detection (iframe present) triggers iframe reload
    - Test Mode A/B (no iframe) triggers full page reload
    - Test debounce behavior applies to iframe reloads
    - Test error fallback to full page reload
    - Skip: Exhaustive cross-origin tests, performance tests
    - Location: Create `/Users/pauleveritt/projects/pauleveritt/storytime/tests/static/ws_test.html` (browser-based test file)
  - [x] 1.2 Add Mode C detection function
    - Create `isModeC()` function that checks for `iframe[src="./themed_story.html"]` in DOM
    - Return boolean: true if iframe exists, false otherwise
    - Use `document.querySelector()` for detection
    - Reuse pattern: Similar to existing `getWebSocketUrl()` utility function
  - [x] 1.3 Add iframe reload function
    - Create `reloadIframe()` function that:
      - Finds iframe element using same selector as detection
      - Triggers reload by appending timestamp to src: `iframe.src = iframe.src.split('?')[0] + '?t=' + Date.now()`
      - Returns boolean: true if successful, false if iframe not found
    - No scroll preservation in this task (handled in Task Group 2)
  - [x] 1.4 Update scheduleReload() for conditional behavior
    - Modify `scheduleReload()` to check `isModeC()` before reload
    - If Mode C (true), call `reloadIframe()` instead of `window.location.reload()`
    - If Mode A/B (false), keep existing `window.location.reload()` behavior
    - Update console log messages to indicate reload type
  - [x] 1.5 Update RELOAD_DEBOUNCE_DELAY constant
    - Change from 300ms to 100ms as specified in requirements
    - Update constant: `var RELOAD_DEBOUNCE_DELAY = 100; // 100ms`
  - [x] 1.6 Ensure core reload tests pass
    - Run ONLY the 2-8 tests written in 1.1
    - Verify Mode C detection works correctly
    - Verify conditional reload logic branches correctly
    - Do NOT run any other test suites at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 1.1 pass
- Mode C detection correctly identifies iframe presence
- scheduleReload() branches to iframe reload for Mode C, full reload otherwise
- Debounce delay updated to 100ms
- No changes to WebSocket connection logic

**Implementation Notes:**
- Keep IIFE pattern: All new functions inside existing `(function() { ... })()` scope
- Maintain ES5 compatibility: Use `function` keyword, not arrow functions
- Console logging: Follow existing `[Storytime]` prefix pattern
- No external dependencies: Use only browser-native APIs

---

### Scroll Position Preservation

#### Task Group 2: Capture and Restore Scroll State
**Dependencies:** Task Group 1
**Files to modify:** `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/static/ws.js`

- [x] 2.0 Implement scroll position preservation
  - [x] 2.1 Write 2-8 focused tests for scroll preservation
    - Test scroll position captured before reload
    - Test scroll position restored after reload
    - Test cross-origin errors handled gracefully
    - Skip: Edge cases for scrollX, exact timing tests
    - Location: Add to existing `/Users/pauleveritt/projects/pauleveritt/storytime/tests/static/ws_test.html`
  - [x] 2.2 Add scroll capture function
    - Create `captureIframeScroll(iframe)` function that:
      - Accepts iframe element as parameter
      - Returns object: `{scrollX: number, scrollY: number}` or `null` on error
      - Safely accesses `iframe.contentWindow.scrollX` and `scrollY`
      - Wraps in try-catch to handle cross-origin SecurityError
      - Logs errors to console without throwing
  - [x] 2.3 Add scroll restore function
    - Create `restoreIframeScroll(iframe, scrollState)` function that:
      - Accepts iframe element and scroll state object
      - Calls `iframe.contentWindow.scrollTo(scrollState.scrollX, scrollState.scrollY)`
      - Wraps in try-catch to handle cross-origin errors
      - Returns boolean: true if successful, false on error
  - [x] 2.4 Update reloadIframe() to preserve scroll
    - Capture scroll position before reload: `var scrollState = captureIframeScroll(iframe);`
    - Store scrollState in closure variable
    - After setting iframe.src, add `onload` handler: `iframe.onload = function() { restoreIframeScroll(iframe, scrollState); };`
    - Only restore if scrollState is not null
  - [x] 2.5 Ensure scroll preservation tests pass
    - Run ONLY the 2-8 tests written in 2.1
    - Verify scroll position captured correctly
    - Verify scroll position restored on reload
    - Do NOT run entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 2.1 pass
- Scroll position preserved across iframe reloads
- Cross-origin errors handled without crashing
- Scroll restoration occurs after iframe content loads

**Implementation Notes:**
- Cross-origin safety: Always wrap `iframe.contentWindow` access in try-catch
- Default scroll state: If capture fails, default to `{scrollX: 0, scrollY: 0}`
- Timing: Use `iframe.onload` event to ensure content loaded before restoring scroll
- Console messages: Log scroll capture/restore actions for debugging

---

### Visual Feedback

#### Task Group 3: Alpha Mask Effect During Reload
**Dependencies:** Task Group 1
**Files to modify:**
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/static/ws.js`
- `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/static/storytime.css`

- [x] 3.0 Implement visual feedback during reload
  - [x] 3.1 Write 2-8 focused tests for visual feedback
    - Test CSS class applied to iframe on reload
    - Test opacity transition effect triggers
    - Test class removed after fixed duration
    - Skip: Exact timing measurements, animation performance tests
    - Location: Add to existing `/Users/pauleveritt/projects/pauleveritt/storytime/tests/static/ws_test.html`
  - [x] 3.2 Add CSS for iframe reload effect
    - Location: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/static/storytime.css`
    - Add new CSS class: `.iframe-reloading { opacity: 0.6; transition: opacity 0.2s ease; }`
    - Follow existing pattern: Match transition style from `.assertion-badge:hover` (0.2s ease)
    - Place near end of file, before `@media` queries
  - [x] 3.3 Add visual effect functions
    - Create `applyReloadEffect(iframe)` function that:
      - Adds CSS class: `iframe.classList.add('iframe-reloading');`
      - Sets fixed duration removal: `setTimeout(function() { iframe.classList.remove('iframe-reloading'); }, 200);`
      - Duration: 200ms to match CSS transition duration
    - No need for load event detection (per spec requirement)
  - [x] 3.4 Update reloadIframe() to apply visual effect
    - Call `applyReloadEffect(iframe)` immediately before setting iframe.src
    - Effect should be visible during entire reload process
    - Example flow:
      1. Capture scroll
      2. Apply visual effect
      3. Update iframe.src
      4. Set onload handler for scroll restoration
  - [x] 3.5 Ensure visual feedback tests pass
    - Run ONLY the 2-8 tests written in 3.1
    - Verify CSS class applied during reload
    - Verify class removed after 200ms
    - Do NOT run entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 3.1 pass
- CSS alpha mask effect (opacity: 0.6) applied to iframe during reload
- Smooth transition effect (0.2s ease)
- Effect removed after fixed 200ms duration
- Effect does not interfere with content readability

**Implementation Notes:**
- CSS class name: Use `.iframe-reloading` for semantic clarity
- Transition timing: Match existing transitions in storytime.css (0.2s ease)
- Fixed duration: 200ms removal via setTimeout, independent of iframe load event
- Browser compatibility: CSS opacity and transitions are widely supported

---

### Error Handling & Testing

#### Task Group 4: Error Fallback and Test Coverage Review
**Dependencies:** Task Groups 1, 2, 3
**Files to modify:** `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/static/ws.js`

- [x] 4.0 Implement error handling and review test gaps
  - [x] 4.1 Review tests from Task Groups 1-3
    - Review the 2-8 tests written in Task 1.1 (core reload logic)
    - Review the 2-8 tests written in Task 2.1 (scroll preservation)
    - Review the 2-8 tests written in Task 3.1 (visual feedback)
    - Total existing tests: approximately 6-24 tests
  - [x] 4.2 Add iframe error fallback handler
    - Update `reloadIframe()` to set error handler:
      - `iframe.onerror = function() { console.error('[Storytime] Iframe failed to load, falling back to full page reload'); window.location.reload(); };`
    - Error handler triggers on 404, network errors, CORS failures
    - Provides graceful degradation to full page reload
  - [x] 4.3 Analyze test coverage gaps for iframe reload feature
    - Identify critical workflows not covered by existing 6-24 tests
    - Focus ONLY on iframe reload feature (Mode C detection, scroll, visual feedback, errors)
    - Do NOT assess entire application test coverage
    - Prioritize integration scenarios over isolated unit tests
  - [x] 4.4 Write up to 10 additional strategic tests maximum
    - Add maximum of 10 new tests to fill identified critical gaps
    - Focus on end-to-end reload workflows:
      - Full reload cycle: WebSocket message -> iframe reload -> scroll restore -> visual effect
      - Error scenarios: iframe fails to load -> fallback to full page reload
      - Edge cases: iframe removed from DOM during reload, rapid successive reloads
    - Do NOT write comprehensive coverage for all scenarios
    - Skip: Performance tests, accessibility tests, cross-browser compatibility tests
    - Location: Add to `/Users/pauleveritt/projects/pauleveritt/storytime/tests/static/ws_test.html`
  - [x] 4.5 Run feature-specific tests only
    - Run ONLY tests related to iframe reload feature
    - Expected total: approximately 16-34 tests maximum (6-24 from tasks 1-3, plus up to 10 new tests)
    - Do NOT run entire application test suite (e.g., skip Python tests, component tests)
    - Verify critical workflows pass:
      - Mode C reload preserves scroll and shows visual feedback
      - Mode A/B perform full page reload
      - Error fallback works correctly

**Acceptance Criteria:**
- All iframe reload feature tests pass (approximately 16-34 tests total)
- Iframe errors trigger fallback to full page reload
- Critical workflows covered: detection, reload, scroll, visual feedback, error handling
- No more than 10 additional tests added when filling in testing gaps
- Testing focused exclusively on iframe reload feature

**Implementation Notes:**
- Error logging: Use `console.error()` with `[Storytime]` prefix
- Fallback behavior: `window.location.reload()` is the universal fallback
- Test execution: Use browser-based testing (manual or automated with Playwright/Puppeteer)
- Test file format: HTML file with inline JavaScript tests (no pytest for browser JS)

---

## Execution Order

Recommended implementation sequence:
1. **Task Group 1: Mode Detection and Conditional Reload** - Core logic foundation
2. **Task Group 2: Scroll Position Preservation** - Enhance user experience (depends on Task 1)
3. **Task Group 3: Visual Feedback** - Polish and feedback (depends on Task 1)
4. **Task Group 4: Error Handling & Testing** - Robustness and verification (depends on Tasks 1-3)

**Rationale for order:**
- Task 1 establishes the foundation (Mode C detection and conditional reload logic)
- Tasks 2 and 3 are independent enhancements that both depend on Task 1
- Task 2 (scroll) and Task 3 (visual) can be implemented in parallel if desired
- Task 4 adds error handling and comprehensive testing after core features are complete

**Parallel execution opportunities:**
- After Task 1 completes, Tasks 2 and 3 can be worked on simultaneously
- Task 4 should wait for all others to complete

## Testing Strategy

### Browser-Based Testing
Since this feature is pure client-side JavaScript, tests should run in a browser environment:

**Test file location:** `/Users/pauleveritt/projects/pauleveritt/storytime/tests/static/ws_test.html`

**Test structure:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Iframe Reload Tests</title>
</head>
<body>
    <div id="test-results"></div>
    <iframe src="./themed_story.html" style="width: 100%; min-height: 600px;"></iframe>

    <script src="../../src/storytime/components/layout/static/ws.js"></script>
    <script>
        // Simple test runner
        function test(name, fn) {
            try {
                fn();
                console.log('[PASS]', name);
            } catch (e) {
                console.error('[FAIL]', name, e);
            }
        }

        // Example tests
        test('Mode C detection returns true when iframe exists', function() {
            // Test implementation
        });

        test('Mode A/B detection returns false when no iframe', function() {
            // Test implementation
        });

        // ... more tests
    </script>
</body>
</html>
```

**Alternative:** Use Playwright or Puppeteer for automated browser testing if preferred.

### Test Count Limits
- Each task group (1-3) writes 2-8 focused tests maximum
- Task group 4 adds up to 10 additional strategic tests maximum
- Total expected: 16-34 tests for entire feature
- Focus on critical paths, not exhaustive coverage

### Running Tests
Since this is JavaScript in the browser:
1. **Manual testing:** Open test HTML file in browser, check console for results
2. **Automated testing:** Use Playwright/Puppeteer to run tests in CI pipeline
3. **Integration with `just test`:** Consider adding browser test task to Justfile if automation is added

## Implementation Notes

### Code Quality Standards
After each task group, ensure:
- **ES5 compatibility:** Use `function` keyword, no arrow functions, no `const`/`let` in production code
- **IIFE pattern:** Keep all code inside existing `(function() { 'use strict'; ... })()` wrapper
- **Console logging:** Use `[Storytime]` prefix for all log messages
- **Error handling:** Wrap cross-origin iframe access in try-catch blocks
- **No dependencies:** Use only browser-native APIs (WebSocket, DOM, setTimeout, etc.)

### File Paths Reference
- **Primary file to modify:** `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/static/ws.js`
- **CSS file to modify:** `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/components/layout/static/storytime.css`
- **Test file to create:** `/Users/pauleveritt/projects/pauleveritt/storytime/tests/static/ws_test.html`
- **Reference files (no changes needed):**
  - `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/story/views.py` (Mode C iframe structure)
  - `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/websocket.py` (backend message format)

### Backward Compatibility
- **No breaking changes:** All existing functionality (Mode A/B full reload) must continue working
- **WebSocket message format:** Keep using `{"type": "reload"}` - no new message types
- **No Python changes:** All changes are client-side JavaScript only
- **CSS additive:** New `.iframe-reloading` class does not affect existing styles

### Out of Scope Reminders
- Do NOT change WebSocket message format or create new message types
- Do NOT add service workers, caching, or offline support
- Do NOT implement partial DOM updates or hot module replacement
- Do NOT preserve scroll position in parent page (only iframe)
- Do NOT make changes to Python backend (`websocket.py`, `watchers.py`, `views.py`)
- Do NOT add user-configurable timing or animation controls
