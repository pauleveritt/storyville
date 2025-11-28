# Spec Requirements: Full Static Paths

## Initial Description
Full static paths. I would like any layout/component/view to define its own `static` folder which gets copied into the output_dir. To prevent filename collisions, and to make it clear where each asset came from, I would like to preserve the path to the static directory. Meaning, the output_dir should have `static/components/layout/static/` as a directory. The rendered paths should then point to the correct static asset.

## Requirements Discussion

### First Round Questions

**Q1: Scope - Which node types should support static folders?**
**Answer:** All node types.

**Q2: Path preservation structure - How should the path be preserved in the output directory?**
**Answer:** Keep the extra static at the end. (So `src/storytime/components/navigation_tree/static/nav.css` → `output_dir/static/components/navigation_tree/static/nav.css`)

**Q3: Path resolution in components - How should components reference their static assets in templates?**
**Answer:** I want the path in the template to point to the actual path on disk. But have a helper that runs on the result node, before returning it. It would find the `<script src>` and `<link href>` and `<img src>` etc. that started with `static` and rewrote to point to (a) the full path and (b) relativized to the depth.

**Q4: Collision handling - What happens if multiple components have the same filename in their static folders?**
**Answer:** This can't happen because the two components will have different file paths to get to `static`.

**Q5: Site-level static directory - Should there be a site-level static directory for shared assets?**
**Answer:** Remove the concept of the site-level static.

**Q6: Hot reload behavior - Should changes to static assets trigger rebuild?**
**Answer:** Yes, any changes trigger rebuild.

**Q7: Development vs. production - Should behavior differ between dev and production?**
**Answer:** Both (behavior should be identical).

**Q8: Additional requirement**
**Answer:** Make sure this works for both static assets in `src/storytime` as well as `static` in the input_dir.

### Follow-up Questions

**Follow-up 1: Path rewriting - relativized to depth**
Can you clarify what "relativized to the depth" means? For example, if a page is at `/sections/components/button.html` and references a static asset, should the path be `../../static/components/navigation_tree/static/nav.css`?

**Answer:** Yes, if a page at `/sections/components/button.html` references a static asset, the path should be `../../static/components/navigation_tree/static/nav.css`

**Follow-up 2: Two static sources - precedence and disambiguation**
You mentioned support for both `src/storytime` and `input_dir` static folders. Should these be merged into the same `static/` output directory, or should they be separated? What happens if both have the same path structure?

**Answer:** Use `storytime_static` and `static` as directory names to disambiguate. (So `src/storytime` static assets go to `storytime_static/` and `input_dir` static assets go to `static/`)

**Follow-up 3: Path rewriting helper - location and integration**
Where should the path-rewriting helper live? Should it be:
- Part of the node rendering pipeline (automatically applied)?
- A post-processing step after rendering?
- Called explicitly by the developer?

**Answer:** Make it an opt-in utility function for now. The component has to call it. This means:
- NOT automatically applied in rendering pipeline
- Components/stories must explicitly call this utility function
- It should be a utility function that processes HTML content and rewrites static paths

### Existing Code to Reference
No similar existing features identified for reference. Will need to examine:
- Current static asset handling and build process
- Node rendering pipeline and transformation hooks
- File watching and hot reload mechanisms

## Visual Assets

### Files Provided:
No visual assets provided.

### Visual Insights:
N/A - No visual files found.

## Requirements Summary

### Functional Requirements

**Static Folder Support:**
- Every node type (layout/component/view/subject/section/story) can define its own `static` folder
- Static folders are discovered during build process
- All static assets are copied to output_dir with full path preservation

**Path Structure in Output:**
- Two output directories for disambiguation:
  - `output_dir/storytime_static/[path/to/component]/static/[asset]` for `src/storytime` assets
  - `output_dir/static/[path/to/component]/static/[asset]` for `input_dir` assets
- Original path structure is preserved to prevent collisions
- Example: `src/storytime/components/navigation_tree/static/nav.css` → `output_dir/storytime_static/components/navigation_tree/static/nav.css`
- Example: `input_dir/components/button/static/icon.svg` → `output_dir/static/components/button/static/icon.svg`

**Path Resolution - Opt-In Utility Function:**
- Components reference static assets with simple prefix in templates (e.g., `static/nav.css` or `storytime_static/nav.css`)
- A utility function is provided that components/stories must explicitly call
- **NOT automatically applied** - developers must opt-in by calling the utility
- Utility function processes HTML content (as a string or node) and finds asset references: `<script src>`, `<link href>`, `<img src>`, etc.
- Only processes paths that start with `static` or `storytime_static`
- Rewrites paths to:
  1. Full path: `[storytime_static|static]/[path/to/component]/static/[asset]`
  2. Relativized to page depth: Uses `../` segments based on page location

**Example Path Rewriting:**
- Template: `<link href="storytime_static/nav.css">`
- Component location: `src/storytime/components/navigation_tree/`
- Page location: `/sections/components/button.html` (depth 2)
- After calling utility: `<link href="../../storytime_static/components/navigation_tree/static/nav.css">`

**Hot Reload:**
- Changes to any static asset trigger a rebuild
- File watching includes all `static/` folders in both `src/storytime` and `input_dir`
- Browser refreshes automatically after rebuild

**Environment Consistency:**
- Behavior is identical in development and production
- No environment-specific path handling or asset processing

### Reusability Opportunities
- Investigate current static asset handling code in build process
- Examine existing node rendering pipeline for transformation hook points
- Review file watching system for extension to static folders
- Check for existing path utility functions for relative path calculation

### Scope Boundaries

**In Scope:**
- Static folder support for all node types
- Path-preserving copy to output_dir with disambiguation between sources
- **Opt-in utility function** for path rewriting (must be explicitly called by components/stories)
- Hot reload support for static asset changes
- Support for both src/storytime and input_dir static folders
- Relative path calculation based on page depth

**Out of Scope:**
- Site-level static directory (explicitly removed)
- Automatic path rewriting in rendering pipeline (utility must be called explicitly)
- Different behavior for dev vs production
- Asset optimization, minification, or bundling
- CDN integration or external asset hosting
- Asset fingerprinting or cache busting

### Technical Considerations

**Utility Function Design:**
- Must be easy to call from components/stories
- Should accept HTML content (string or node)
- Should return processed HTML with rewritten paths
- Must be well-documented for developers to understand when/how to use
- Consider naming that makes purpose clear (e.g., `rewrite_static_paths()`)

**Path Calculation:**
- Need to determine page depth from output path
- Need to construct full asset path from component location
- Need to calculate correct number of `../` segments
- Must handle edge cases (root pages, nested sections)

**File Discovery:**
- Need to scan for `static/` folders in node directories
- Must track source location (storytime vs input_dir)
- Should be efficient for large component catalogs

**Collision Prevention:**
- Path preservation ensures no filename collisions
- Different source directories (`storytime_static` vs `static`) prevent conflicts
- Full path structure makes asset origin clear

**Hot Reload Integration:**
- File watcher must monitor all discovered static folders
- Changes should trigger rebuild of affected pages
- May need to track which pages reference which assets for selective rebuilds

**Performance:**
- HTML parsing only happens when utility is called (opt-in)
- Should be efficient enough for typical use cases
- May need to optimize for large HTML documents

**Testing:**
- Test with various page depths and asset references
- Verify correct relative path calculation
- Test collision prevention with identical filenames
- Test hot reload with static asset changes
- Test both storytime and input_dir static sources
- Test utility function can be called from different contexts
- Test when utility is NOT called, paths remain unchanged
