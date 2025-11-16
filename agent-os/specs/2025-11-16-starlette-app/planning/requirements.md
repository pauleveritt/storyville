# Spec Requirements: Starlette App

## Initial Description

Create a Starlette-based web app to serve Storytime portfolios from a built site. The app should:

1. Serve a built site from a `var` directory
2. Comment out/remove everything related to reloading functionality (focus on static serving first)
3. Tests should use tempdir fixture instead of the project root `var` directory
4. Properly serve the layout's static directory using `StaticFiles`
5. Handle potentially unusual static directory paths like `static/components/layout/static`
6. Determine whether the entire site should be a StaticFiles path or just the static assets

Starting point: `app.py` and `test_app.py` have broken beginnings that need to be fixed.

## Requirements Discussion

### First Round Questions

**Q1:** For serving the site, I'm assuming we should use a single StaticFiles mount at the root path (Option 2: Single Mount - `Mount("/", app=StaticFiles(directory=path, html=True), name="site")`) rather than separate static asset and dynamic routes. Is that correct?

**Answer:** Use Option 2 (Single Mount) - `Mount("/", app=StaticFiles(directory=path, html=True), name="site")`

**Q2:** The `create_app(path: Path)` function should accept a Path parameter pointing to the built site root (e.g., `var/`), correct?

**Answer:** `create_app(path: Path)` should point to `var/` (built site root)

**Q3:** For the broken `app.py` starting point - should we start fresh with a clean implementation, or preserve any specific patterns from the existing broken code?

**Answer:** Start fresh (don't preserve broken app.py patterns)

**Q4:** Are there any features we should explicitly exclude from this initial implementation? For example: custom error pages, middleware, request logging, CORS configuration, etc.?

**Answer:** Skip all other features (no error pages, middleware, etc.)

### Existing Code to Reference

No similar existing features identified for reference.

### Follow-up Questions

None required - all requirements were clearly answered in the first round.

## Visual Assets

### Files Provided:

No visual assets provided.

## Requirements Summary

### Functional Requirements

- Create a Starlette application factory function `create_app(path: Path)` that accepts a Path parameter
- The Path parameter should point to the built site root directory (e.g., `var/`)
- Serve all content using a single StaticFiles mount at the root path: `Mount("/", app=StaticFiles(directory=path, html=True), name="site")`
- Use `html=True` parameter to enable automatic `index.html` serving for directory paths
- Remove all reload and file watching functionality from the implementation
- Replace any existing `/stories/{full_path:path}` dynamic routes with the StaticFiles mount
- Tests should build the site to `tmp_path` first, then create the app with that path
- Tests should verify that the directory structure of the built site mirrors the input structure
- Use per-test builds with pytest's `tmp_path` fixture for test isolation

### Reusability Opportunities

No existing similar features were identified for reuse. This is a foundational piece for the Web-Based Component Browser (item 3 on the product roadmap).

### Scope Boundaries

**In Scope:**
- Static file serving via Starlette's StaticFiles
- Single mount point at root path
- Configurable directory path via `create_app(path: Path)`
- Automatic index.html serving
- Test infrastructure using temporary directories
- Clean removal of reload/watching code

**Out of Scope:**
- Hot reload development server functionality (deferred)
- Custom error pages (404, 500, etc.)
- Middleware (logging, CORS, etc.)
- Request handling beyond static file serving
- Dynamic routes or template rendering
- Custom static asset handling beyond StaticFiles default behavior

### Technical Considerations

- Aligns with product tech stack: Starlette (web server framework), Python 3.14+
- Supports roadmap item 3: "Web-Based Component Browser"
- Lays groundwork for future roadmap item 4: "Hot Reload Development Server" (currently excluded)
- Tests must use `tmp_path` fixture for isolation, not project root `var/` directory
- The built site structure should be preserved (tests verify this)
- Implementation should be minimal and focused on static serving only
- Starting from scratch rather than fixing broken existing code
