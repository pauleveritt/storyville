# Task Breakdown: Granular Change Detection

## Overview

Implement intelligent change detection for hot reload that tracks currently-viewed pages, filters changes by story relevance, and uses either iframe reload or DOM morphing based on what changed.

**Total Task Groups:** 6
**Estimated Size:** Medium (M)

## Task List

### Server Infrastructure Layer

#### Task Group 1: WebSocket Connection State Management
**Dependencies:** None

- [x] 1.0 Complete WebSocket connection state tracking
  - [x] 1.1 Write 2-8 focused tests for connection state management
    - Test connection state storage and cleanup on disconnect
    - Test page metadata extraction from URLs
    - Test story identifier parsing from paths
    - Skip exhaustive edge case testing
  - [x] 1.2 Extend `websocket.py` to store page metadata per connection
    - Add connection state data structure: `{websocket: {page_url, page_type, story_id}}`
    - Create `_connection_metadata: dict[WebSocket, dict[str, str]]` module-level storage
    - Store metadata on connection establishment
  - [x] 1.3 Handle initial page metadata message from client
    - Update `websocket_endpoint()` to receive page metadata on connection
    - Parse incoming JSON message: `{type: "page_info", page_url, page_type, story_id}`
    - Store metadata in `_connection_metadata` dict
  - [x] 1.4 Implement page type classification
    - Detect story pages with iframe (Mode C)
    - Detect story container pages (themed_story.html)
    - Detect non-story pages (documentation, indexes)
  - [x] 1.5 Implement story identifier extraction
    - Extract story path from URL: `/components/heading/story-0/index.html` → `components/heading/story-0`
    - Parse section, subject, and story index from path
    - Handle both standard and themed story URLs
  - [x] 1.6 Clean up connection state on disconnect
    - Remove metadata entry in `websocket_endpoint()` finally block
    - Ensure no memory leaks from orphaned connection state
  - [x] 1.7 Ensure connection state tests pass
    - Run ONLY the 2-8 tests written in 1.1
    - Verify metadata storage and cleanup work correctly
    - Do NOT run entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 1.1 pass
- Connection metadata is stored and cleaned up correctly
- Story identifiers are correctly extracted from URLs
- Page types are accurately classified

#### Task Group 2: Change Detection and Classification
**Dependencies:** Task Group 1

- [ ] 2.0 Complete change detection classification system
  - [ ] 2.1 Write 2-8 focused tests for change classification
    - Test global asset detection (themed_story.html, CSS, JS)
    - Test story-specific change detection (story index.html)
    - Test non-story change detection (docs, indexes)
    - Skip exhaustive path pattern testing
  - [ ] 2.2 Extend `watchers.py` to classify file changes
    - Add `classify_change()` function to categorize changes
    - Return classification: `{change_type: "global" | "story" | "non_story", story_id: str | None}`
  - [ ] 2.3 Implement global asset detection
    - Detect `themed_story.html` changes in any story directory
    - Detect CSS bundle changes in `static/` directories
    - Detect JS bundle changes in `static/` directories
    - These affect all story pages
  - [ ] 2.4 Implement story-specific change detection
    - Detect individual story `index.html` changes
    - Extract story identifier from file path
    - Match story path format from `Story.resource_path`
  - [ ] 2.5 Implement non-story change detection
    - Detect documentation page changes
    - Detect section index page changes
    - Detect catalog index changes
    - These affect non-story viewers
  - [ ] 2.6 Integrate classification with watcher
    - Call `classify_change()` for each detected file change
    - Pass classification result to broadcast function
    - Maintain existing debounce behavior (0.3s)
  - [ ] 2.7 Ensure change classification tests pass
    - Run ONLY the 2-8 tests written in 2.1
    - Verify changes are correctly classified
    - Do NOT run entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 2.1 pass
- File changes are correctly classified by type
- Story identifiers are correctly extracted from file paths
- Classification integrates with existing watcher logic

#### Task Group 3: Targeted Broadcast System
**Dependencies:** Task Groups 1, 2

- [ ] 3.0 Complete targeted broadcast implementation
  - [ ] 3.1 Write 2-8 focused tests for targeted broadcasting
    - Test story-specific broadcast filtering
    - Test global broadcast to all story viewers
    - Test non-story broadcast filtering
    - Skip exhaustive connection filtering scenarios
  - [ ] 3.2 Create new message format for broadcasts
    - Define message structure: `{type: "reload", change_type: "iframe_reload" | "morph_html" | "full_reload", story_id: str | None, html: str | None}`
    - Replace old `{type: "reload"}` format with new granular format
  - [ ] 3.3 Implement `broadcast_targeted_reload()` function
    - Accept parameters: `change_type`, `affected_story_id`, `html_content`
    - Filter connections based on page type and story ID
    - Send appropriate message format to each connection
  - [ ] 3.4 Implement story-specific filtering
    - For story HTML changes: only notify connections viewing that specific story
    - Compare `affected_story_id` with stored `story_id` in connection metadata
    - Send `change_type: "morph_html"` with HTML payload
  - [ ] 3.5 Implement global story broadcast
    - For global asset changes: notify all connections viewing any story
    - Filter for `page_type: "story"` in connection metadata
    - Send `change_type: "iframe_reload"` (no HTML payload)
  - [ ] 3.6 Implement non-story broadcast
    - For non-story changes: notify all non-story viewers
    - Filter for `page_type: "non_story"` in connection metadata
    - Send `change_type: "full_reload"` (no filtering by page)
  - [ ] 3.7 Add logging for broadcast targeting
    - Log broadcast decision: which connections receive messages
    - Log change type and affected story ID
    - Include timestamps for correlation with watcher logs
  - [ ] 3.8 Ensure targeted broadcast tests pass
    - Run ONLY the 2-8 tests written in 3.1
    - Verify correct connections receive correct messages
    - Do NOT run entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 3.1 pass
- Broadcasts are correctly filtered by page type and story ID
- Message format includes all required fields
- Logging provides clear visibility into broadcast decisions

### Client Infrastructure Layer

#### Task Group 4: Client-Side Page Tracking and Message Handling
**Dependencies:** None (can be developed in parallel with server tasks)

- [ ] 4.0 Complete client-side page tracking and message handling
  - [ ] 4.1 Write 2-8 focused tests for client-side functionality
    - Test page type detection (story vs non-story)
    - Test story identifier extraction from URL
    - Test message parsing and routing
    - Use browser testing with Playwright if needed
    - Skip exhaustive URL parsing scenarios
  - [ ] 4.2 Implement page identification on load in `ws.mjs`
    - Detect page type: story page (has iframe), non-story page
    - Extract story identifier from `window.location.pathname`
    - Reuse `isModeC()` logic for story page detection
  - [ ] 4.3 Send page metadata on WebSocket connection
    - Send message on `ws.onopen`: `{type: "page_info", page_url, page_type, story_id}`
    - Include full URL path, page type classification, and extracted story ID
    - Update `connect()` function to send metadata after connection opens
  - [ ] 4.4 Implement new message handler for reload types
    - Parse incoming messages with `change_type` field
    - Route to appropriate reload handler based on `change_type`
    - Handle three types: `iframe_reload`, `morph_html`, `full_reload`
  - [ ] 4.5 Update iframe reload handler
    - Trigger iframe reload for `change_type: "iframe_reload"`
    - Preserve existing scroll position capture/restore logic
    - Keep visual reload effect (`.iframe-reloading` class)
    - Maintain fallback to full page reload on error
  - [ ] 4.6 Add logging for received messages
    - Log all received WebSocket messages with parsed data
    - Log reload type and story ID
    - Log which reload handler is invoked
    - Include timestamps for correlation with server logs
  - [ ] 4.7 Ensure client-side tests pass
    - Run ONLY the 2-8 tests written in 4.1
    - Verify page tracking and message handling work
    - Do NOT run entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 4.1 pass
- Page metadata is correctly identified and sent to server
- Messages are correctly parsed and routed to handlers
- Iframe reload works with scroll preservation
- Comprehensive logging provides visibility into client behavior

#### Task Group 5: DOM Morphing Implementation
**Dependencies:** Task Group 4

- [ ] 5.0 Complete DOM morphing with idiomorph
  - [ ] 5.1 Write 2-8 focused tests for DOM morphing
    - Test morphing story content without full reload
    - Test fallback to iframe reload on morphing failure
    - Test scroll position preservation during morph
    - Use browser testing with Playwright if needed
    - Skip exhaustive morphing scenarios
  - [ ] 5.2 Bundle idiomorph library locally
    - Download idiomorph from https://github.com/bigskysoftware/idiomorph
    - Place in `src/storyville/components/layout/static/idiomorph.min.js`
    - Do NOT use CDN - bundle locally for reliability
  - [ ] 5.3 Load idiomorph in story pages
    - Add script tag to load idiomorph in story page templates
    - Ensure idiomorph is available as global `Idiomorph` object
    - Only load on story pages (not needed for non-story pages)
  - [ ] 5.4 Implement `morphStoryContent()` function in `ws.mjs`
    - Accept HTML payload from WebSocket message
    - Target story content area for morphing (iframe content document)
    - Use idiomorph to morph only the changed content
    - Preserve scroll position during morph
  - [ ] 5.5 Handle morph messages in WebSocket handler
    - For `change_type: "morph_html"`: call `morphStoryContent(message.html)`
    - Extract HTML from message payload
    - Apply morphing to story content only
  - [ ] 5.6 Implement fallback chain
    - If morphing fails: fall back to `reloadIframe()`
    - If iframe reload fails: fall back to `window.location.reload()`
    - Log each fallback decision
  - [ ] 5.7 Add logging for morphing operations
    - Log morph attempts with story ID
    - Log morph success/failure
    - Log fallback decisions
    - Include timestamps for correlation
  - [ ] 5.8 Ensure DOM morphing tests pass
    - Run ONLY the 2-8 tests written in 5.1
    - Verify morphing works without full reload
    - Verify fallback chain works correctly
    - Do NOT run entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 5.1 pass
- idiomorph is bundled locally and loads correctly
- Story content morphs without full page reload
- Scroll position is preserved during morph
- Fallback chain works correctly
- Logging provides visibility into morph operations

### Testing & Documentation

#### Task Group 6: Test Review, Gap Analysis, and Documentation
**Dependencies:** Task Groups 1-5

- [ ] 6.0 Review tests, fill critical gaps, and update documentation
  - [ ] 6.1 Review existing tests from Task Groups 1-5
    - Review the 2-8 tests written in 1.1 (connection state)
    - Review the 2-8 tests written in 2.1 (change classification)
    - Review the 2-8 tests written in 3.1 (targeted broadcast)
    - Review the 2-8 tests written in 4.1 (client-side tracking)
    - Review the 2-8 tests written in 5.1 (DOM morphing)
    - Total existing tests: approximately 10-40 tests
  - [ ] 6.2 Analyze test coverage gaps for THIS feature only
    - Identify critical end-to-end workflows lacking coverage
    - Focus on integration between server and client
    - Prioritize story-specific reload → morph workflow
    - Prioritize global asset → iframe reload workflow
    - Do NOT assess entire application test coverage
  - [ ] 6.3 Write up to 10 additional strategic tests maximum
    - End-to-end test: story HTML change → morph
    - End-to-end test: global asset change → iframe reload
    - End-to-end test: non-story page change → full reload
    - Integration test: connection state → broadcast filtering
    - Integration test: change classification → targeted broadcast
    - Do NOT write comprehensive coverage for all scenarios
    - Skip edge cases unless business-critical
  - [ ] 6.4 Update architecture documentation
    - Document granular change detection system in `docs/architecture.md`
    - Add section: "Granular Change Detection"
    - Explain page tracking mechanism
    - Document WebSocket message protocol with all message types
    - Explain change classification logic (global, story, non-story)
    - Document broadcast targeting and filtering
    - Add flow diagram: file change → classification → targeted broadcast → client reload
    - Document DOM morphing vs iframe reload decision logic
    - Document fallback chain: morph → iframe reload → full reload
  - [ ] 6.5 Add logging documentation
    - Document server-side logging for change detection
    - Document client-side logging for reload events
    - Provide examples of log messages for debugging
    - Explain how to correlate server and client logs using timestamps
  - [ ] 6.6 Run feature-specific tests only
    - Run ONLY tests related to this spec's feature (tests from 1.1, 2.1, 3.1, 4.1, 5.1, and 6.3)
    - Expected total: approximately 20-50 tests maximum
    - Do NOT run the entire application test suite
    - Verify critical workflows pass

**Acceptance Criteria:**
- All feature-specific tests pass (approximately 20-50 tests total)
- Critical end-to-end workflows are covered
- No more than 10 additional tests added when filling in gaps
- `docs/architecture.md` includes complete granular change detection documentation
- Documentation includes flow diagrams and message protocol details
- Logging is fully documented with examples

## Execution Order

Recommended implementation sequence:

1. **Server Infrastructure (Groups 1-3)**: Build server-side change detection and broadcast targeting
   - Group 1: Connection state management (foundation)
   - Group 2: Change classification (decision logic)
   - Group 3: Targeted broadcast (delivery mechanism)

2. **Client Infrastructure (Groups 4-5)**: Build client-side tracking and reload strategies
   - Group 4: Page tracking and message handling (foundation)
   - Group 5: DOM morphing with idiomorph (advanced reload)

3. **Testing & Documentation (Group 6)**: Verify end-to-end workflows and document system

**Rationale for ordering:**
- Server groups can be implemented sequentially (each builds on previous)
- Client groups can be developed in parallel with server groups
- DOM morphing (Group 5) depends on message handling (Group 4) being complete
- Testing and documentation comes last to verify integrated system

## Important Notes

### Testing Philosophy
- Each task group writes 2-8 highly focused tests covering ONLY critical behaviors
- Test verification runs ONLY the newly written tests, not the entire suite
- Task Group 6 adds maximum 10 additional tests to fill critical end-to-end gaps
- Total expected tests for this feature: approximately 20-50 tests

### Backward Compatibility
- WebSocket message format can be completely changed (no backward compatibility required)
- Remove old `{type: "reload"}` format entirely
- Implement only new granular message format

### Logging Strategy
- Add comprehensive logging on both server and client
- Use timestamps for correlation between server and client logs
- Log all key decision points: classification, targeting, reload type
- Include story IDs and change types in all log messages

### Existing Code Patterns to Follow
- Follow existing `websocket.py` patterns for connection management
- Follow existing `watchers.py` patterns for file change detection
- Follow existing `ws.mjs` patterns for WebSocket client
- Use modern Python 3.14+ features: `type` statement, PEP 604 unions, match/case
- Use `aria-testing` library functions for DOM queries in tests
- Maintain single test file per component (no separate integration test files)

### External Dependencies
- idiomorph: Bundle locally from https://github.com/bigskysoftware/idiomorph
- No CDN dependencies - all assets must be local for reliability
