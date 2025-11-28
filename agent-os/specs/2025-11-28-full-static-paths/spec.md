# Specification: Full Static Paths

## Goal
Enable all node types (layouts, components, views, subjects, sections, stories) to define their own static folders with path-preserving asset management and opt-in relative path rewriting for HTML references.

## User Stories
- As a component developer, I want to place static assets next to my component code so that asset management is co-located and organized
- As a developer, I want to easily reference static assets in my templates using a utility function that automatically resolves relative paths based on page depth

## Specific Requirements

**Static Folder Discovery and Copying**
- Scan all node directories during build for `static/` folders in both `src/storytime` and input_dir paths
- Track source location (storytime vs input_dir) to determine output directory disambiguation
- Copy all discovered static assets to output_dir preserving full directory path structure
- Assets from `src/storytime` copy to `output_dir/storytime_static/[path/to/node]/static/[asset]`
- Assets from input_dir copy to `output_dir/static/[path/to/node]/static/[asset]`
- Example: `src/storytime/components/navigation_tree/static/nav.css` → `output_dir/storytime_static/components/navigation_tree/static/nav.css`
- Example: `input_dir/components/button/static/icon.svg` → `output_dir/static/components/button/static/icon.svg`

**Remove Existing Site-Level Static**
- Remove the existing `Site.static_dir` property and related `__post_init__` logic from site/models.py
- Remove the static asset copying code from build.py lines 172-174 that copies `site.static_dir`
- Update any Layout component code that references site-level static to use new path structure

**Opt-In Path Rewriting Utility Function**
- Create a utility function (e.g., `rewrite_static_paths()`) that components/stories must explicitly call
- Function accepts HTML content as input (string or tdom Node) and returns processed HTML
- Parses HTML to find asset references in `src`, `href`, and other relevant attributes
- Only processes paths that start with `static/` or `storytime_static/` prefix
- Rewrites found paths to include full component path and relativize based on page depth
- Calculates correct number of `../` segments based on page location in site hierarchy
- Depth 0 (site root or section index): `../static/...` or `../storytime_static/...`
- Depth 1 (subject index): `../../static/...` or `../../storytime_static/...`
- Depth 2 (story page): `../../../static/...` or `../../../storytime_static/...`

**HTML Asset Reference Detection**
- Scan for `<script src="...">`, `<link href="...">`, `<img src="...">`, and other asset-referencing tags
- Use HTML parsing library or regex to identify attributes that contain asset paths
- Support both single and double quoted attribute values
- Handle edge cases like self-closing tags and multiple attributes per element

**Path Construction Logic**
- Accept component location information to determine asset source path
- Construct full output path: `[storytime_static|static]/[component/path]/static/[asset_filename]`
- Accept current page depth to calculate relative path prefix
- Combine relative prefix with full asset path for final rewritten reference
- Preserve original path if it doesn't match `static/` or `storytime_static/` prefix (external URLs, absolute paths)

**Hot Reload Support for Static Assets**
- Extend file watching system to monitor all discovered `static/` folders
- Include both `src/storytime/**/static/` and `input_dir/**/static/` in watch paths
- Trigger full rebuild when any static asset changes
- Ensure browser refresh occurs after rebuild completes (existing WebSocket mechanism)

**Component Integration Points**
- Make utility function easily importable from a common location (e.g., `storytime.utils.rewrite_static_paths`)
- Provide clear function signature with type hints for input/output
- Document expected calling pattern in function docstring
- Allow function to work at different stages (during render or post-render)
- Ensure function is performant enough for typical HTML document sizes

**Build Process Integration**
- Add static folder discovery phase before rendering begins
- Collect all static folder paths and their source locations during discovery
- Add static asset copying phase after HTML writing completes
- Use `shutil.copytree` with `dirs_exist_ok=True` to handle overlapping paths
- Preserve directory modification times if possible for caching

**Error Handling and Validation**
- Handle missing static folders gracefully (no error if static/ doesn't exist)
- Log warnings if static folder exists but is empty
- Validate that copied assets actually exist at expected output locations
- Provide helpful error messages if path rewriting fails due to malformed HTML
- Handle edge case of component paths with unusual characters or deep nesting

## Visual Design
No visual mockups provided for this feature.

## Existing Code to Leverage

**build.py copytree usage (lines 172-174)**
- Already uses `shutil.copytree` for copying static directory
- Uses `dirs_exist_ok=True` pattern that should be replicated for new static copying
- Currently copies from `site.static_dir` to `output_dir / "static"` which will be removed
- Can reuse this pattern but loop through discovered static folders with new output paths

**Layout depth calculation (layout.py lines 41-50)**
- Already calculates relative paths based on depth parameter
- Uses `static_prefix = "../" * (self.depth + 1)` pattern
- Constructs paths like `f"{static_prefix}static/pico-main.css"`
- This exact logic should be replicated in the path rewriting utility function
- Depth parameter is already passed through view rendering pipeline

**Site.static_dir lookup pattern (site/models.py lines 29-35)**
- Shows how to check if directory exists with `sd.exists()`
- Uses `PACKAGE_DIR` to construct paths relative to storytime installation
- Pattern can be used for discovering static folders during build process
- Need similar logic but scanning recursively through all node directories

**TreeNode package path resolution (nodes.py lines 98-139)**
- Shows how to construct relative package paths from filesystem structure
- Uses `relative_to()` to calculate paths relative to root package
- This logic can help map static folder filesystem paths to output directory structure
- Provides pattern for handling both root and nested locations

**make_site recursive scanning (site/helpers.py lines 33-38)**
- Already uses `rglob("stories.py")` to recursively find all story modules
- Same pattern can be used with `rglob("static")` to find all static directories
- Demonstrates how to walk the tree and build data structures from filesystem
- Can extend this phase to also collect static folder information

## Out of Scope
- Site-level static directory concept (explicitly removed)
- Automatic path rewriting in rendering pipeline (must be opt-in via utility function call)
- Different behavior between development and production environments
- Asset optimization, minification, bundling, or preprocessing
- CDN integration or external asset hosting
- Asset fingerprinting or cache busting for versioning
- Selective rebuilds based on which assets changed (trigger full rebuild for any static change)
- Source maps or other build artifacts for static assets
- Validation of asset file types or contents
- Compression or optimization of static assets during copy
