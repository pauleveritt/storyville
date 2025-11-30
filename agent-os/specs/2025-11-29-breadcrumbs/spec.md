# Specification: Breadcrumbs Navigation Fix

## Goal

Enable breadcrumbs navigation to display correctly on built static pages by adding resource_path tracking to all
resource objects and plumbing it through the view rendering pipeline.

## User Stories

- As a site visitor, I want to see breadcrumb navigation showing my location in the hierarchy so that I can understand
  where I am and navigate back to parent pages
- As a developer, I want breadcrumbs to automatically appear on all rendered pages without manual intervention so that
  navigation is consistent across the entire catalog

## Specific Requirements

**Add resource_path attribute to BaseNode**

- Add `resource_path: str` field to BaseNode dataclass (non-optional)
- Initialize as empty string by default to support Catalog at root level
- Update BaseNode.post_update() to populate resource_path during tree construction
- Calculate path format: Section="section", Subject="section/subject", Story="section/subject/story"
- Ensure resource_path represents the URL path structure in the tree
- Make resource_path available on all resource types (Catalog, Section, Subject, Story)

**Populate resource_path during tree traversal**

- Calculate resource_path during catalog construction in make_catalog or similar tree-building logic
- Populate resource_path when calling post_update() on each node
- Use TreeNode information to derive the correct path segments
- Ensure Catalog has resource_path="" (empty string for root)
- Build paths incrementally as tree is traversed (parent path + current name)

**Update view signatures to accept resource_path**

- Add `resource_path: str` parameter to SectionView.__init__
- Add `resource_path: str` parameter to SubjectView.__init__
- Add `resource_path: str` parameter to StoryView.__init__
- Store resource_path as instance attribute in each view
- Pass resource_path to Layout component when rendering
- Type hint as `str` (not optional) throughout

**Update build.py to pass resource_path to views**

- Modify _render_all_views function to extract resource_path from each resource object
- Pass resource_path when instantiating SectionView, SubjectView, StoryView
- Calculate resource_path format for each node: section key for Section, "section/subject" for Subject, etc.
- Ensure resource_path flows from resource object through view instantiation to Layout
- CatalogView remains unchanged (no breadcrumbs on home page)

**Remove Parent links from view templates**

- Delete `<a href="..">Parent</a>` from SectionView template (line 68 in section/views.py)
- Delete `<a href="..">Parent</a>` from SubjectView template (lines 64 and 85 in subject/views.py)
- Delete `<a href="..">Parent</a>` from StoryView template (lines 158, 170, 194, 208 in story/views.py)
- Parent navigation now handled by breadcrumbs component instead of explicit links

**Rename current_path to resource_path throughout codebase**

- Rename in Layout component (layout.py line 32)
- Rename in LayoutMain component
- Rename in LayoutAside component
- Rename in Breadcrumbs component (breadcrumbs.py line 18)
- Rename in all test files that reference current_path
- Update parameter names consistently across all integration points

**Convert breadcrumb links to relative paths**

- Modify Breadcrumbs component to calculate relative paths based on depth
- Replace absolute paths like "/section" with relative paths like "../"
- Calculate upward traversal: depth 1 uses "../", depth 2 uses "../../", depth 3 uses "../../../"
- Home link should navigate relatively based on current depth
- Combine upward traversal with forward path segments for intermediate links
- Use depth parameter already available in views to determine relative path calculation

**Update type hints for resource_path**

- Change Breadcrumbs.current_path from `str | None` to `resource_path: str`
- Change Layout.current_path from `str | None` to `resource_path: str`
- Make resource_path non-optional throughout to eliminate None checks
- Update all view type signatures to require resource_path: str parameter
- Ensure BaseNode.resource_path is typed as str with proper initialization

## Visual Design

No visual assets provided for this specification.

## Existing Code to Leverage

**Breadcrumbs component (src/storytime/components/breadcrumbs/breadcrumbs.py)**

- Already implements parse_current_path to extract section/subject/story from path
- Already renders breadcrumb trail with separators and proper HTML structure
- Has aria-label for accessibility compliance
- Logic for determining which items are links vs current page is complete
- Needs only: rename current_path to resource_path and convert to relative paths

**Layout component (src/storytime/components/layout/layout.py)**

- Already accepts current_path parameter and passes to LayoutMain and LayoutAside
- Already integrated with Breadcrumbs via LayoutMain
- Needs only: rename current_path to resource_path throughout

**BaseNode class (src/storytime/nodes.py)**

- Already has post_update() method that receives parent and tree_node
- Already calculates package_path and name from tree_node
- Pattern established for adding resource_path calculation in same method
- Already used by Catalog, Section, Subject via inheritance

**View rendering in build.py (_render_all_views function)**

- Already iterates through all sections, subjects, stories in correct order
- Already has section_key, subject_key, story_idx variables available
- Already instantiates all view classes and passes necessary parameters
- Pattern for constructing resource_path: concatenate keys with "/" separator

**Tree traversal structure in build.py**

- Nested loops already establish hierarchy: catalog -> sections -> subjects -> stories
- Path segments already available: section_key, subject_key, story_idx
- Can calculate resource_path at each level by combining parent path with current key

## Out of Scope

- Changes to breadcrumbs component rendering HTML structure (already correct)
- Changes to breadcrumbs positioning in layout (already in correct location above title)
- Visual styling or CSS changes to breadcrumbs appearance
- Adding breadcrumbs to CatalogView or home page (intentionally excluded)
- Visual distinction between current page breadcrumb and parent links (not needed)
- Development server changes (issue specific to static build output)
- Changes to navigation tree component or sidebar navigation
- Modifications to Story model (does not inherit from BaseNode)
- Alternative storage locations for resource_path (decision made to use resource objects)
- Backwards compatibility for old current_path parameter name
