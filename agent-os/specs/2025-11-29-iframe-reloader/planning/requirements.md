# Spec Requirements: iframe-reloader

## Initial Description

When viewing a Story, I want the updated page to load faster, without disruption of scroll position, and little repaint. I don't want the main HTML in the document to reload. Only the HTML for the iframe.

Instead of triggering a full page reload, the JS event handler should only reload the <iframe> content.

## Requirements Discussion

### First Round Questions

**Q1: Reload scope - Should iframe-only reload apply to all story views (Mode A, B, C) or just Mode C (themed iframe views)?**
**Answer:** Only Mode C. In other contexts, full page reload.

**Q2: Scroll preservation - Should we preserve scroll position in the iframe, in the parent page, or both?**
**Answer:** Only scroll position in the iframe.

**Q3: WebSocket message types - Should we introduce a new WebSocket message type (e.g., {"type": "iframe-reload"}) or enhance the existing "reload" message?**
**Answer:** Keep current message type.

**Q4: Error handling - If the iframe fails to reload (404, network error, etc.), should we fall back to a full page reload?**
**Answer:** Full reload.

**Q5: Visual feedback - Should we provide visual feedback during iframe reload (e.g., a loading indicator or fade effect)?**
**Answer:** Yes, visual indicator using CSS on the iframe. Perhaps an alpha mask.

**Q6: Iframe load timing - Should we detect when the iframe has finished loading before removing any loading indicator?**
**Answer:** No

**Q7: Build detection - Should the watcher/WebSocket system distinguish between builds that affect themed content vs navigation/layout?**
**Answer:** Keep current.

**Q8: Out of scope - Are there any related features we should explicitly exclude from this spec (e.g., service workers, offline support, partial DOM updates)?**
**Answer:** None.

### Existing Code to Reference

**Similar Features Identified:**
- Feature: Current full-page reload system - Path: `src/storytime/components/layout/static/ws.js`
- WebSocket infrastructure: `src/storytime/websocket.py`
- File watching and rebuild: `src/storytime/watchers.py`
- Story view rendering: `src/storytime/story/views.py`
- Layout component with script injection: `src/storytime/components/layout/layout.py`

**Backend logic to reference:**
- WebSocket endpoint at `/ws/reload` (in `app.py`)
- Broadcast mechanism: `broadcast_reload_async()` in `websocket.py`
- Current message format: `{"type": "reload"}`

**Frontend logic to reference:**
- Current reload script: `ws.js` with WebSocket connection, message parsing, and `window.location.reload()`
- Script injection in Layout component at line 55: `<script src="static/ws.js"></script>`

### Follow-up Questions

No follow-up questions were needed. All requirements were clarified in the first round.

## Visual Assets

### Files Provided:
No visual assets provided.

### Visual Insights:
Not applicable - no visual files to analyze.

## Requirements Summary

### Functional Requirements

**Core Functionality:**
- Detect when a Story page is in Mode C (themed iframe rendering)
- When a WebSocket reload message is received on a Mode C page, reload only the iframe instead of the full page
- Preserve the iframe's scroll position during reload
- Apply a visual CSS effect (alpha mask) during iframe reload
- Fall back to full page reload if iframe reload fails
- Continue to perform full page reload for Mode A and Mode B stories

**User Actions Enabled:**
- Developers editing themed story content see updates in the iframe without losing navigation context
- Scroll position within the themed content is maintained across hot reloads
- Visual feedback indicates that a reload is in progress

**Data Management:**
- No new data structures required
- Reuse existing WebSocket message type: `{"type": "reload"}`
- Store iframe scroll position before reload and restore after

### Reusability Opportunities

**Components that exist:**
- `ws.js`: WebSocket client script that connects to `/ws/reload` and handles reload messages
- `Layout` component: Injects the `ws.js` script into all pages
- `StoryView`: Renders Mode C pages with `<iframe src="./themed_story.html">`

**Backend patterns to follow:**
- WebSocket infrastructure in `websocket.py` and `app.py` remains unchanged
- File watcher in `watchers.py` continues to broadcast `{"type": "reload"}` messages
- No backend changes required

**Similar code patterns:**
- Current `ws.js` implements: WebSocket connection, message parsing, debouncing, reconnection logic
- New iframe reload logic should extend this pattern with conditional behavior based on page context

### Scope Boundaries

**In Scope:**
- Modify `ws.js` to detect Mode C (iframe presence) and conditionally reload iframe vs full page
- Implement iframe scroll position preservation
- Add CSS-based visual indicator (alpha mask) during iframe reload
- Implement error handling that falls back to full page reload on iframe errors
- Ensure debouncing works correctly for iframe reloads

**Out of Scope:**
- Changes to WebSocket message format (keep `{"type": "reload"}`)
- Different reload strategies for Mode A or Mode B (always full page reload for these)
- Build detection to distinguish content types (keep current unified approach)
- Advanced features like service workers, offline support, or partial DOM updates
- Loading indicator timing based on iframe load events (user explicitly said "No")

### Technical Considerations

**Integration Points:**
- Modify `ws.js` to add iframe detection and conditional reload logic
- No changes to Python backend (`websocket.py`, `watchers.py`, `app.py`, `build.py`)
- No changes to HTML generation in `StoryView` or `Layout`
- CSS for alpha mask effect should be inline or in existing `storytime.css`

**Existing System Constraints:**
- Must maintain compatibility with existing WebSocket infrastructure
- Must work with current file watching and rebuild system
- Must not break Mode A or Mode B story views
- Must respect existing debouncing behavior (300ms delay)

**Technology Stack:**
- JavaScript (ES5 compatible, wrapped in IIFE like current `ws.js`)
- WebSocket API (browser native)
- CSS for visual effects
- No additional dependencies or frameworks

**Implementation Notes:**
- Detection of Mode C: Check for presence of `iframe[src="./themed_story.html"]` in the DOM
- Scroll preservation: Capture `iframe.contentWindow.scrollY` before reload, restore after
- Alpha mask: Apply CSS opacity/overlay effect to iframe during reload
- Error handling: Listen for iframe `onerror` event and trigger `window.location.reload()` as fallback
- Debouncing: Apply same 300ms debounce to iframe reloads as full page reloads
