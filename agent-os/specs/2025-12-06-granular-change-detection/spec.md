# Specification: Granular Change Detection

## Goal

Implement intelligent change detection for the hot reload system that tracks currently-viewed pages, filters changes by
story relevance, and uses either iframe reload or DOM morphing depending on what changed.

## User Stories

- As a developer, I want changes to only reload the currently-viewed story page so that I'm not distracted by unrelated
  updates
- As a developer, I want story content changes to use DOM morphing instead of full reload so that I maintain my scroll
  position and page state

## Specific Requirements

**Page Tracking on WebSocket Connection**

- Browser sends current page URL and page type when WebSocket connects
- Server maintains mapping of WebSocket connections to their current page
- Page type distinguishes between story pages, non-story pages, and story container pages
- Extract story identifier from URL path for story pages (e.g., `/components/heading/story-0/index.html` extracts
  `components/heading/story-0`)
- No navigation tracking needed - only track on initial WebSocket connection

**Change Detection Classification**

- Classify detected file changes into categories: story-specific, global assets, or non-story content
- Global assets include `themed_story.html`, CSS bundles, and JS bundles in static directories
- Story-specific changes are individual story `index.html` files
- Non-story changes include documentation pages, section index pages, and site-wide pages

**Story-Specific Change Filtering**

- Only send reload messages to clients viewing the affected story
- Compare changed file path to currently-viewed story identifier
- If story `index.html` changes, only notify clients viewing that specific story
- If global assets change, notify all clients viewing any story page
- For non-story pages, broadcast to all clients viewing non-story content

**WebSocket Message Protocol Update**

- Redesign message format to support granular reload types
- Include fields: `type` (action type), `change_type` (iframe_reload, morph_html, full_reload), `story_id` (story
  identifier if applicable), `html` (HTML payload for morphing)
- Use `type: "reload"` with `change_type: "iframe_reload"` for global asset changes affecting stories
- Use `type: "reload"` with `change_type: "morph_html"` for story-specific HTML changes
- Use `type: "reload"` with `change_type: "full_reload"` for non-story pages or when client doesn't support morphing

**Iframe Reload Strategy**

- Triggered when `themed_story.html` or global assets (CSS/JS bundles) change
- Only reload the iframe containing story content, not the full page
- Preserve existing scroll position capture and restoration logic
- Apply visual reload effect for user feedback
- Maintain fallback to full page reload on iframe load errors

**DOM Morphing Strategy**

- Bundle idiomorph library locally in static assets (not via CDN)
- Send full HTML content of updated story in WebSocket message payload
- Client applies morphing only to story content area, not full page
- Only triggered for story-specific `index.html` changes
- Preserve scroll position and maintain interactive state where possible

**Client-Side Page Identification**

- Detect page type on load: story page with iframe, story container page, or non-story page
- Extract story identifier from URL path on story pages
- Send page metadata to server on WebSocket connection establishment
- Use existing URL parsing logic from `ws.mjs` as foundation

**Server-Side Connection State Management**

- Extend `websocket.py` to track page metadata per WebSocket connection
- Store mapping: `WebSocket -> {page_url, page_type, story_id}`
- Update broadcast functions to accept target filtering parameters
- Clean up connection state on WebSocket disconnect

**Change Detection Integration**

- Extend `watchers.py` to classify file changes by type
- Determine affected story IDs from changed file paths
- Call appropriate broadcast function with filtering parameters
- Maintain existing debounce behavior (0.3s delay)

**Backward Compatibility and Fallback**

- If client doesn't support new message format, fall back to full page reload
- If DOM morphing fails, fall back to iframe reload
- If iframe reload fails, fall back to full page reload
- Maintain existing behavior for non-story pages (full reload)

**Logging and Debugging**

- Add server-side logging for change detection decisions and broadcast targeting
- Log connection state changes (page tracking, WebSocket connect/disconnect)
- Log change classification and affected story IDs
- Add browser console.log messages for reload events and morphing operations
- Log received WebSocket messages with change type and story ID
- Log morphing success/failure and fallback decisions
- Include timestamps and story identifiers in all log messages for correlation

**Documentation**

- Update `docs/architecture.md` to document the granular change detection system
- Document WebSocket message protocol and message types
- Explain the change classification logic and broadcast targeting
- Document the page tracking mechanism and connection state management
- Include diagrams showing the flow from file change to targeted reload

## Existing Code to Leverage

**`src/storyville/websocket.py` - WebSocket connection management**

- Module-level `_active_connections` set tracks all WebSocket instances
- `websocket_endpoint()` accepts connections and maintains them
- `broadcast_reload()` sends messages to all connected clients
- Implement filtered broadcast functions that target specific connections based on page metadata

**`src/storyville/watchers.py` - File watching and change detection**

- `watch_and_rebuild()` monitors directories and triggers rebuilds
- `DEBOUNCE_DELAY` constant (0.3s) prevents rapid successive rebuilds
- File filtering logic distinguishes between content and static assets
- Extend change detection to classify changes by affected story or global scope

**`src/storyville/components/layout/static/ws.mjs` - WebSocket client**

- `isModeC()` detects story pages with iframe
- `reloadIframe()` reloads iframe with scroll preservation
- `scheduleReload()` implements client-side debouncing
- `getWebSocketUrl()` constructs WebSocket connection URL
- Extend to send page metadata on connection and handle new message types

**`src/storyville/story/models.py` - Story data model**

- `Story` class with `resource_path` property for story identification
- Story index derived from parent's items list
- Use `resource_path` format to match story identifiers in file paths

**`src/storyville/app.py` - Application lifespan and watcher setup**

- `lifespan()` context manager starts/stops unified watcher
- `create_app()` configures Starlette with WebSocket route
- Integration point for passing story metadata to watcher callbacks
- Maintain existing rebuild callback pattern with filtering parameters

## Out of Scope

- Navigation tracking after initial WebSocket connection
- Dependency tracking system for imported modules
- Story dependency graphs showing relationships between components
- Change history or rollback capability for undoing changes
- Advanced caching strategies for rendered HTML
- Configurable debounce thresholds (keep existing 0.3s)
- Backward compatibility for WebSocket protocol (new format only)
- Morphing for non-story pages (full reload only)
- Real-time collaboration features or multi-user notifications
- Partial page updates for sections other than story content
