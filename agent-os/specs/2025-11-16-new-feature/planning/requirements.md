# Spec Requirements: Hot Reload Feature

## Initial Description

Add hot reload capability to Storytime's development server. When source files change, the browser should automatically refresh to show the latest changes. This should work by watching for file changes and triggering a browser reload via WebSocket connection.

## Requirements Discussion

### First Round Questions

**Q1:** For the file watching, I assume we should use the `watchfiles` package (which is already in the tech stack). Is that correct, or would you prefer a different approach?
**Answer:** Yes, use watchfiles.

**Q2:** I'm thinking we should use Starlette's built-in WebSocket support to send reload messages to the browser. Should we use this, or would you prefer a different WebSocket implementation?
**Answer:** Yes, use Starlette's WebSocket support.

**Q3:** For the watch process, should it monitor the INPUT directory (`src/storytime`) or the OUTPUT directory (where rendered HTML is generated), or both? I'm assuming we watch the INPUT since that's where source files change, but let me know if we should also watch the OUTPUT.
**Answer:** Watch both directories independently.

**Q4:** Should we implement any debouncing to avoid rapid-fire reloads if multiple files change at once (like during a git checkout)? If yes, what delay would you prefer?
**Answer:** Debounce in the browser JavaScript.

**Q5:** Should the watch process monitor only certain file types (like `.py`, `.html`, `.css`), or all files? I'm assuming we should filter to relevant file types to avoid reloading on things like `.pyc` or cache files.
**Answer:** Watch relevant file types.

**Q6:** For the WebSocket message format, should it be a simple reload command, or should we send additional metadata (like which file changed, timestamps, etc.)?
**Answer:** Simple reload message.

**Q7:** Should this feature include any visual feedback in the browser (like a "reconnecting..." indicator if the server restarts), or keep it minimal with just the reload behavior?
**Answer:** Keep it minimal.

**Q8:** Are there any features we should explicitly exclude from this implementation (like selective module reloading, state persistence, or connection retry logic)?
**Answer:** No extra features beyond basic reload.

### Existing Code to Reference

**Similar Features Identified:**
- None identified - this is a new capability for Storytime

### Follow-up Questions

**Follow-up 1:** You mentioned watching both INPUT and OUTPUT directories. Should these be two separate watch processes running independently, or a single process watching both locations?
**Answer:** Two separate watch processes running independently - INPUT watcher triggers rebuild, OUTPUT watcher sends websocket messages (in case the output directory is manually edited).

**Follow-up 2:** For the debouncing in the browser JavaScript - should there also be server-side debouncing for the file watcher, or only client-side debouncing?
**Answer:** Debounce only in the browser JavaScript (not server-side), in case the server sends a bunch of messages.

**Follow-up 3:** For filtering file types in the INPUT directory - since this is `src/storytime`, should we watch for changes to Python files (`.py`), or also static assets like CSS/JS if they exist there?
**Answer:** Static assets live in `src/storytime` (the INPUT directory) - watch for changes to files ending in `.css`, `.js`, `.png`, etc.

**Follow-up 4:** For the WebSocket message format - what should the simple reload message look like? Just `{"type": "reload"}` or something else?
**Answer:** Simple reload message like `{"type": "reload"}` - this should cause the page to reload in the browser.

## Visual Assets

### Files Provided:
No visual assets provided.

### Visual Insights:
No visual assets to analyze.

## Requirements Summary

### Functional Requirements

**Dual Watch Architecture:**
- INPUT watcher monitors `src/storytime/` directory for file changes
- When INPUT files change, trigger a rebuild of the component catalog
- OUTPUT watcher monitors the generated/rendered HTML output directory
- When OUTPUT files change (either from rebuild or manual edits), send WebSocket reload message
- Both watchers run independently as separate processes

**File Watching Specifications:**
- Use `watchfiles` package for file system monitoring
- INPUT watcher filters for: `.py`, `.css`, `.js`, `.png`, and other static asset extensions
- OUTPUT watcher monitors all files in the output directory
- No server-side debouncing - watcher sends messages immediately

**WebSocket Implementation:**
- Use Starlette's built-in WebSocket support
- Message format: `{"type": "reload"}` (simple JSON)
- Client receives message and triggers `window.location.reload()` or equivalent
- Client-side debouncing to handle rapid message bursts
- No visual indicators, reconnection UI, or connection state management

**Browser Behavior:**
- Inject WebSocket client JavaScript into served HTML pages
- Client connects to WebSocket endpoint on page load
- Client implements debouncing logic to avoid rapid reloads
- On receiving `{"type": "reload"}` message, refresh the page
- Minimal implementation - no state persistence or selective reloading

### Reusability Opportunities

**Existing Components:**
- Starlette application server (already exists)
- Existing HTML rendering pipeline (OUTPUT directory generation)
- watchfiles package (already in dependencies)

**Patterns to Follow:**
- Use existing Starlette routing patterns for WebSocket endpoint
- Follow project's Python 3.14+ standards (type hints, pattern matching)
- Integrate with existing CLI/server startup code

### Scope Boundaries

**In Scope:**
- File watching for INPUT directory (`src/storytime/`)
- File watching for OUTPUT directory (rendered HTML)
- Rebuild triggering when INPUT files change
- WebSocket server endpoint using Starlette
- WebSocket client JavaScript injection
- Simple reload message protocol
- Client-side debouncing logic
- Basic browser refresh on message receipt

**Out of Scope:**
- Visual feedback indicators (connection status, reconnecting messages)
- Server-side debouncing
- Connection retry logic or reconnection handling
- State persistence across reloads
- Selective module reloading (hot module replacement)
- File change metadata in messages (timestamps, file paths)
- Configuration options for watch patterns or debounce timing
- Production mode (feature is development-only)
- Cross-browser compatibility testing beyond modern browsers

### Technical Considerations

**Integration Points:**
- Starlette application initialization (add WebSocket route)
- HTML rendering (inject client-side JavaScript)
- Server startup sequence (launch watcher processes)
- Build/rebuild pipeline (INPUT watcher triggers this)

**Technology Stack:**
- watchfiles (file system monitoring)
- Starlette WebSocket (server-side WebSocket)
- Native JavaScript WebSocket API (client-side)
- JSON for message serialization

**File Locations:**
- INPUT directory: `src/storytime/`
- OUTPUT directory: To be determined (wherever rendered HTML is generated)
- WebSocket endpoint: To be added to Starlette application
- Client JavaScript: Injected into HTML or served as static file

**Constraints:**
- Development mode only
- No server-side debouncing
- Two independent watch processes
- Simple message protocol only
- Minimal client implementation
