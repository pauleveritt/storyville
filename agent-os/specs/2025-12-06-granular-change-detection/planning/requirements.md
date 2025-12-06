# Spec Requirements: Granular Change Detection

## Initial Description

From the product roadmap (feature #17):

"Granular change detection — Make the change detection more granular. First, track the currently-viewed page. If it is not a Story, then keep as-is. If a Story, keep track of which Story and only do reloading if the change is about the currently-viewed story. If the `themed_story.html` or any of its assets are in the changeset, tell the iframe to reload. If it is the Story index.html, don't do a reload. Instead, send the HTML in the payload and use a local copy of https://github.com/bigskysoftware/idiomorph to patch the page. Explain this in the architecture documents."

**Size Estimate:** M (Medium)

**Context:** This feature builds on the existing hot reload development server (feature #4) and themed stories (feature #8) to provide more intelligent and performant reloading behavior.

## Requirements Discussion

### First Round Questions

**Q1:** For tracking the currently-viewed page, I assume we should have the browser tell the server which page it's on when the WebSocket connects, and update this tracking whenever navigation occurs. Is that correct, or should tracking happen differently?

**Answer:** Yes, when the WebSocket connects, have the browser tell the server the page it is on.

**Q2:** For Story-specific filtering, I'm thinking we'll need to track dependencies (which files affect which stories). Should we implement a dependency tracking system that monitors imports/includes, or use a simpler approach like file path pattern matching?

**Answer:** This is tracking rendered HTML so no need to track dependencies.

**Q3:** For iframe reload vs DOM morphing, I assume we should bundle idiomorph locally (rather than CDN) for reliability. Should we use npm/bundler or just vendor the minified file?

**Answer:** Bundled locally

**Q4:** For changeset determination, I assume "global assets" like `themed_story.html` affect all stories and should trigger iframe reload. Should CSS/JS bundle changes also force full reload, or can we be more granular?

**Answer:** Yes (force full reload for global asset changes)

**Q5:** For non-story pages (like documentation or index pages), I assume we keep the current full-page reload behavior since DOM morphing is only for story content. Correct?

**Answer:** No filtering for those pages, just tell them to reload

**Q6:** Performance-wise, I'm thinking we should debounce change detection (e.g., 100ms window) to batch rapid file changes. Should we add configurable thresholds, or keep it simple with a sensible default?

**Answer:** Let's keep the current debounce threshold

**Q7:** For the WebSocket message format, I assume we'll need to extend the current protocol to include: `page_type` (story/other), `story_id` (if applicable), `change_type` (iframe_reload/morph_html/full_reload), and `html_payload` (for morphing). Should we maintain backward compatibility or can we change the format?

**Answer:** You can totally change the format

**Q8:** What should we NOT include in this feature? For example: story dependency graphs, change history, rollback capability, or advanced caching strategies?

**Answer:** None

### Existing Code to Reference

**Similar Features Identified:**

No similar existing features explicitly identified by user. However, the following features provide the foundation:
- Feature #4: Hot Reload Development Server (completed) - existing WebSocket infrastructure and file watching
- Feature #8: Themed Stories (completed) - iframe architecture for story rendering

### Follow-up Questions

None needed - answers were comprehensive and clear.

## Visual Assets

### Files Provided:

No visual assets provided.

### Visual Insights:

N/A

## Requirements Summary

### Functional Requirements

**Page Tracking:**
- Browser sends current page information to server when WebSocket connects
- Server maintains mapping of connected clients to their current page/story
- No need for navigation update tracking (implied by "when WebSocket connects")

**Change Detection Logic:**
- Determine if currently-viewed page is a Story or non-story page
- For Stories: track which specific story is being viewed
- For non-story pages: trigger simple full-page reload (no filtering)
- Change detection operates on rendered HTML (no dependency tracking needed)

**Story-Specific Reloading:**
- Only reload if changes affect the currently-viewed story
- Global asset changes (themed_story.html, CSS/JS bundles) force iframe reload for all stories
- Story-specific HTML changes trigger DOM morphing (not iframe reload)

**DOM Morphing Implementation:**
- Bundle idiomorph library locally (not via CDN)
- Send HTML payload via WebSocket for story content updates
- Apply morphing to update story content without full page refresh
- Only used for story index.html changes

**Iframe Reload Behavior:**
- Triggered when themed_story.html or global assets change
- Reloads the iframe containing story content
- Full iframe refresh (not DOM morphing)

**WebSocket Protocol:**
- New message format (no backward compatibility requirement)
- Must include: page type, story identifier, change type, HTML payload (when morphing)
- Use existing debounce threshold (no new configuration needed)

### Reusability Opportunities

**Components to Investigate:**
- Existing WebSocket connection handling from hot reload server
- Current file watching and change detection infrastructure
- Iframe management for themed stories
- Message protocol from existing hot reload implementation

**Backend Patterns to Reference:**
- File change detection and notification system
- WebSocket connection management
- Story rendering logic

### Scope Boundaries

**In Scope:**
- Track currently-viewed page on WebSocket connection
- Differentiate between story pages and non-story pages
- Implement story-specific change filtering
- Bundle idiomorph locally for DOM morphing
- Trigger iframe reload for global asset changes (themed_story.html, CSS/JS)
- Trigger DOM morphing for story-specific HTML changes
- Simple full reload for non-story pages
- Update WebSocket message format
- Update architecture documentation

**Out of Scope:**
- Navigation tracking (only track on WebSocket connect)
- Dependency tracking system (not needed - track rendered HTML)
- Story dependency graphs
- Change history or rollback capability
- Advanced caching strategies
- Configurable debounce thresholds (use existing)
- Backward compatibility for WebSocket protocol

### Technical Considerations

**Integration Points:**
- Existing hot reload development server (feature #4)
- Themed story iframe architecture (feature #8)
- WebSocket connection infrastructure
- File watching system
- Architecture documentation (feature #10)

**Technology Preferences:**
- Bundle idiomorph locally (not via CDN)
- New WebSocket message format (no backward compatibility constraints)
- Use existing debounce threshold

**Implementation Approach:**
- Track rendered HTML changes (not file dependencies)
- Server-side tracking of client page state
- Client-side page identification on WebSocket connect
- Conditional reload behavior based on page type and change type
