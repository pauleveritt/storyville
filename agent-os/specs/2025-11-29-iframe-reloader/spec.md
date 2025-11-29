# Specification: Iframe Reloader

## Goal
Enable fast, smooth hot reloading for Mode C story views by reloading only the iframe content instead of the full page, preserving scroll position and minimizing visual disruption.

## User Stories
- As a developer editing themed story content, I want the iframe to reload automatically without losing my scroll position so that I can see updates immediately without disruption
- As a developer working on Mode C stories, I want visual feedback during reloads so that I know the system is responding to my changes

## Specific Requirements

**Mode C Detection**
- Detect if the current page is a Mode C story view by checking for the presence of `iframe[src="./themed_story.html"]` in the DOM
- Detection must occur before attempting any reload operation
- If no iframe is found, fall back to full page reload behavior

**Conditional Reload Logic**
- When WebSocket receives `{"type": "reload"}` message, check if page is Mode C
- If Mode C (iframe present), reload only the iframe by updating its `src` attribute
- If not Mode C (Mode A or Mode B), perform full page reload using `window.location.reload()`
- Maintain existing 300ms debounce delay for all reload types

**Scroll Position Preservation**
- Before reloading iframe, capture the current scroll position using `iframe.contentWindow.scrollY` and `iframe.contentWindow.scrollX`
- After iframe content loads, restore the saved scroll position
- Handle cross-origin restrictions gracefully by catching errors when accessing iframe content
- Only preserve scroll position within the iframe, not the parent page

**Visual Feedback During Reload**
- Apply CSS alpha mask effect to iframe element when reload is triggered
- Use opacity transition to create smooth fade effect (e.g., opacity from 1.0 to 0.6)
- Apply effect immediately when reload starts
- Do not wait for iframe load event to remove effect - apply fixed duration transition instead
- Ensure effect is visible but does not interfere with content readability

**Error Handling and Fallback**
- Listen for iframe `onerror` event to detect failed reloads
- If iframe fails to load (404, network error, etc.), trigger full page reload as fallback
- Log errors to console for debugging purposes
- Handle cross-origin access errors when checking scroll position without crashing

**Debouncing Behavior**
- Apply same 300ms debounce to iframe reloads as full page reloads
- Use existing `reloadDebounceTimeout` mechanism to prevent rapid successive reloads
- Clear any pending reload when new reload is scheduled
- Ensure debounce works correctly for both iframe and full page reload paths

## Visual Design

No visual assets provided.

## Existing Code to Leverage

**`src/storytime/components/layout/static/ws.js`**
- WebSocket connection logic with automatic reconnection and exponential backoff
- Message parsing that extracts `{"type": "reload"}` from WebSocket events
- Existing `scheduleReload()` function that implements 300ms debounce using `reloadDebounceTimeout`
- Current full page reload implementation using `window.location.reload()`
- IIFE pattern that keeps state isolated and prevents global namespace pollution

**`src/storytime/story/views.py` (StoryView Mode C rendering)**
- Mode C creates iframe with `src="./themed_story.html"` and inline styles
- Iframe has default style: `width: 100%; min-height: 600px; border: 1px solid #ccc;`
- This iframe element is the target for conditional reload logic
- No changes needed to Python code - iframe structure remains unchanged

**`src/storytime/components/layout/static/storytime.css`**
- Existing CSS patterns for transitions (e.g., `.assertion-badge` hover effects)
- CSS custom properties available for consistent theming
- Alpha mask effect should follow similar pattern to existing transitions (0.2s ease)

**`src/storytime/websocket.py` (WebSocket backend)**
- Backend sends `{"type": "reload"}` messages via `broadcast_reload_async()`
- No changes needed to backend - message format stays the same
- Frontend must handle message differently based on page context

**`src/storytime/watchers.py` (File watching)**
- Triggers rebuild and broadcasts reload after detecting file changes
- Uses 300ms debounce (`DEBOUNCE_DELAY = 0.3`) on the backend
- No changes needed - continues broadcasting same message type

## Out of Scope
- Changes to WebSocket message format or introduction of new message types
- Different reload strategies for Mode A or Mode B story views
- Build system changes to distinguish content types that affect themed vs non-themed content
- Loading indicator timing based on iframe load event detection
- Service workers, offline support, or caching strategies
- Partial DOM updates or more granular hot module replacement
- Scroll position preservation for the parent page
- Backend changes to `websocket.py`, `watchers.py`, or `app.py`
- Changes to the HTML structure of Mode C rendering in `StoryView`
- Animation timing controls or user-configurable visual feedback options
