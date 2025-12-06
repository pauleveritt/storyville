# Specification: Starlette App for Static Site Serving

## Goal
Create a minimal Starlette application factory that serves pre-built Storyville portfolio sites from a configurable directory using StaticFiles with automatic index.html resolution.

## User Stories
- As a developer, I want to serve a built Storyville site so that I can view portfolios in a web browser
- As a developer, I want to optionally specify an output directory for the serve command so that I can persist builds across sessions
- As a developer, I want to see the output directory in logging so that I know where the site is being served from
- As a test writer, I want tests to use isolated temporary directories so that test builds don't pollute the project workspace

## Specific Requirements

**Application Factory Function**
- Create `create_app(path: Path) -> Starlette` function accepting a Path to the built site root
- The Path parameter should point to directories containing built site structure (index.html, section/*, static/*)
- Return a configured Starlette application instance ready to serve
- Use modern Python 3.14+ type hints with Path from pathlib

**Single StaticFiles Mount**
- Mount StaticFiles at root path: `Mount("/", app=StaticFiles(directory=path, html=True), name="site")`
- The `html=True` parameter enables automatic index.html serving for directory requests
- Remove any existing dynamic routes like `/stories/{full_path:path}`
- No separate static asset route needed - StaticFiles handles everything at root

**Remove Reload Infrastructure**
- Delete the RebuildServer class entirely (lines 28-90 in current app.py)
- Remove all watchfiles imports and usage
- Remove WebSocketRoute for reload functionality
- Remove lifespan context manager for file watching
- Remove ProcessPoolExecutor and async reload logic
- Keep the app simple and focused on static serving only

**Simplified Application Structure**
- No lifespan parameter in Starlette constructor
- No WebSocket routes
- Set `debug=True` for development convenience
- Single route: the root StaticFiles mount
- Remove `render_node` endpoint function

**Test Infrastructure with tmp_path**
- Tests must use pytest's `tmp_path` fixture for isolated builds
- Each test should call `build_site(package_location="storyville", output_dir=tmp_path)` first
- Then create app with the tmp_path: `app = create_app(tmp_path)`
- Use Starlette's TestClient for synchronous HTTP testing
- Tests should verify serving of index.html, section pages, and static assets

**Built Site Structure Verification**
- Confirm that `var/index.html` serves at root path `/`
- Confirm that `var/section/components/index.html` serves at `/section/components/`
- Confirm that `var/static/bulma.css` serves at `/static/bulma.css`
- Directory requests (e.g., `/section/components/`) should resolve to index.html automatically via html=True

**Function Signature Clarity**
- Accept Path parameter pointing to built site root (e.g., var/ directory)
- Do not accept Site model object - this is post-build serving only
- Return type should be explicitly annotated as `-> Starlette`
- Function should be synchronous (no async def)

**Serve Command Arguments**
- Accept required first argument: `input_path` (package location to build/serve)
- Accept optional second argument: `output_dir` (directory to build to and serve from)
- If `output_dir` is omitted, use a temporary directory (current behavior with TemporaryDirectory)
- If `output_dir` is provided, use that directory for building and serving
- Log the output directory being used for transparency
- Include the output directory in server startup messages

**Error Handling Scope**
- Let StaticFiles handle 404 errors with default behavior
- No custom error pages in this implementation
- No middleware for error handling
- Rely on Starlette's built-in error responses

## Visual Design
No visual assets provided.

## Existing Code to Leverage

**build_site function from src/storyville/build.py**
- Use in tests to create realistic built site structures in tmp_path
- The function signature: `build_site(package_location: str, output_dir: Path) -> None`
- It clears output_dir, renders HTML files, and copies static assets
- Tests should follow the pattern from test_build.py: build first, then test
- Ensures test sites have proper structure: index.html, section/*/index.html, static/*

**TestClient pattern from tests/test_app.py**
- Import from `starlette.testclient import TestClient`
- Instantiate with app: `client = TestClient(app)`
- Make requests: `response = client.get("/path/")`
- Assert on status_code and content
- Synchronous testing approach (no async required)

**tmp_path fixture usage from test_build.py**
- Use pytest's built-in `tmp_path` fixture for per-test isolation
- Example: `def test_serve_index(tmp_path): ...`
- Build site to tmp_path before creating app
- For session-scoped builds, consider tmpdir_factory pattern from test_build.py

**StaticFiles import from current app.py**
- Already imported: `from starlette.staticfiles import StaticFiles`
- Already using Mount: `from starlette.routing import Mount`
- Current pattern can be simplified by removing other Route types
- Keep the StaticFiles(directory=...) pattern but change to use path instead of site.static_dir

**Starlette application instantiation pattern**
- Current app.py already shows basic Starlette() constructor usage
- Keep debug=True for development
- Simplify routes list to single Mount item
- Remove lifespan, WebSocketRoute, and Route entries

## Out of Scope
- Hot reload development server functionality (file watching and WebSocket-based reloading)
- Custom 404 or 500 error pages
- Request logging middleware
- CORS configuration or headers
- Authentication or authorization
- Dynamic route handling or template rendering
- Building the site (only serving pre-built sites)
- Configuration of static directory path beyond the build_site defaults
- Multiple mount points for different asset types
- Custom StaticFiles subclassing or behavior modification
