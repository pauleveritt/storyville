# Spec Requirements: Breadcrumbs Navigation

## Initial Description

From roadmap item #11:

Put the path to the current node in a breadcrumbs-style navigation, in `<main>` above the title. Provide links for each hop. Remove the `Parent` link in the template.

### Context

The breadcrumbs component has been created at `src/storytime/components/breadcrumbs/breadcrumbs.py` and integrated into `LayoutMain`. The component shows a hierarchy like: Home → Section → Subject → Story.

However, based on the code review:

1. The Breadcrumbs component is already integrated into LayoutMain
2. Each view (SectionView, SubjectView, StoryView) still contains `<a href="..">Parent</a>` links that should be removed
3. The current_path parameter needs to be properly passed through all views to the Layout component

### Current State

- Breadcrumbs component: ✅ Implemented
- Integration in LayoutMain: ✅ Done
- Parent links in views: ❌ Still present (needs removal)
- current_path plumbing: ❓ Needs verification

## Requirements Discussion

### First Round Questions

**Q1:** Should we remove the `<a href="..">Parent</a>` links from SectionView, SubjectView, and StoryView templates?
**Answer:** YES, simply remove them.

**Q2:** Should we audit the current_path parameter plumbing to ensure it flows correctly from tree construction → views → Layout component?
**Answer:** YES, fix it.

**Q3:** Should CatalogView remain unchanged (no breadcrumbs on the home page)?
**Answer:** CORRECT (no breadcrumbs on home).

**Q4:** The breadcrumb rendering logic is already implemented in the Breadcrumbs component. Should it remain unchanged?
**Answer:** NO CHANGES needed.

**Q5:** Should we convert breadcrumb links from absolute paths (`/section`) to relative paths (`../`) based on depth?
**Answer:** YES, convert breadcrumb links to relative paths based on depth.

**Q6:** Should the breadcrumbs positioning (in `<main>` above the title) remain as-is?
**Answer:** YES, keep current position.

**Q7:** Should styling and accessibility attributes remain as-is?
**Answer:** FINE as is.

**Q8:** Should there be visual distinction between current page and parent links in breadcrumbs?
**Answer:** NO distinction needed.

### Follow-up Questions

**Follow-up 1:** Where should the path information (`current_path`) come from and how should it be structured?
**Answer:** The path should be associated with the current "resource" (Story, Section, Subject, Catalog). It should be:
- The on-disk path to the module that resource is at
- Represent the URL path in the tree
- **Better name**: Rename `current_path` to `resource_path` throughout
- Could alternatively be part of TreeNode, but since we already pass the "resource" into views, store it on the resource
- **Type hint change**: Make `resource_path` NOT optional (no `| None`)

**Follow-up 2:** Can you confirm the format for `resource_path` values?
**Answer:** Confirmed correct format:
- Section: `"section_name"`
- Subject: `"section_name/subject_name"`
- Story: `"section_name/subject_name/story_name"`

**Follow-up 3:** Where are views instantiated and called?
**Answer:** Views are called in `_render_all_views` in `build.py`.

**Follow-up 4:** Does this issue affect the development server or only built pages?
**Answer:** Issue affects built pages (static build output).

### Existing Code to Reference

**Similar Features Identified:**

No similar existing features specifically identified, but key files to reference:
- `src/storytime/components/breadcrumbs/breadcrumbs.py` - Existing breadcrumbs component
- `src/storytime/build.py` - View instantiation in `_render_all_views`
- Tree node models (BaseNode and subclasses) - Where `resource_path` will be added
- All view files (SectionView, SubjectView, StoryView) - Need updates

### Visual Assets

No visual assets provided.

## Requirements Summary

### Core Issue Identified

Breadcrumbs component exists and is integrated but isn't showing because `resource_path` is not being:
1. Stored on the resource objects (Catalog, Section, Subject, Story)
2. Passed through to the view constructors
3. Passed from views to Layout component

### Functional Requirements

**1. Data Model Changes**
- Add `resource_path: str` attribute to BaseNode (affects Catalog, Section, Subject, Story)
- Populate `resource_path` during tree construction/traversal
- Format for `resource_path`:
  - Catalog: `""` (empty string for home)
  - Section: `"section_name"`
  - Subject: `"section_name/subject_name"`
  - Story: `"section_name/subject_name/story_name"`
- Make `resource_path` non-optional (no `| None` in type hints)

**2. View Signature Updates**
- Update all view constructors (SectionView, SubjectView, StoryView) to:
  - Accept `resource_path: str` parameter
  - Store it as instance attribute
  - Pass it to Layout component when rendering

**3. Parent Link Removal**
- Remove `<a href="..">Parent</a>` links from:
  - SectionView template
  - SubjectView template
  - StoryView template

**4. Breadcrumb Link Path Conversion**
- Convert breadcrumb links from absolute paths (`/section`) to relative paths
- Calculate relative paths based on depth:
  - From Story (depth 3): `../../../`, `../../section/`, `../subject/`
  - From Subject (depth 2): `../../`, `../section/`
  - From Section (depth 1): `../`
- Home link should always navigate to root using appropriate relative path

**5. Build Process Integration**
- Update `_render_all_views` in `build.py` to pass `resource_path` when instantiating views
- Ensure `resource_path` is available during tree traversal

### Reusability Opportunities

- Existing breadcrumbs component at `src/storytime/components/breadcrumbs/breadcrumbs.py` is complete and requires no changes
- Breadcrumbs tests at `src/storytime/components/breadcrumbs/breadcrumbs_test.py` can be referenced for testing approach
- Layout component integration is already complete

### Naming Convention Changes

**Critical Rename**: Throughout the codebase, rename `current_path` → `resource_path`
- More accurately describes what it represents (path to the resource/page)
- Distinguishes it from potential "current directory" or other path concepts
- Should be applied consistently across:
  - Model attributes
  - View parameters
  - Layout component parameters
  - Test fixtures and test code

### Scope Boundaries

**In Scope:**
- Add `resource_path` attribute to BaseNode and all resource models
- Populate `resource_path` during tree construction
- Update view signatures to accept and use `resource_path`
- Pass `resource_path` from views to Layout component
- Rename all instances of `current_path` to `resource_path`
- Remove Parent links from SectionView, SubjectView, StoryView
- Convert breadcrumb links to relative paths based on depth
- Update type hints to make `resource_path` non-optional
- Update tests to reflect all changes
- Ensure breadcrumbs display correctly on built static pages

**Out of Scope:**
- Changes to breadcrumbs component rendering logic (already correct)
- Changes to breadcrumbs positioning in layout (already correct)
- Visual styling changes (current styling is acceptable)
- Adding breadcrumbs to CatalogView/home page (intentionally excluded)
- Visual distinction between current page and parent links (not needed)
- Development server changes (issue is specific to build output)

### Technical Considerations

**Architecture Decision: Store resource_path on Resource Objects**

The path information will be stored directly on the resource objects (Catalog, Section, Subject, Story) rather than on TreeNode because:
- Views already receive the resource object as a parameter
- Simpler to pass one object rather than multiple parameters
- Keeps resource metadata with the resource itself
- More intuitive for developers working with views

**Integration Points:**
- Tree construction/traversal logic (where resource_path gets populated)
- BaseNode model (where resource_path attribute is defined)
- All view constructors (SectionView, SubjectView, StoryView)
- Layout component (receives resource_path from views)
- `build.py` `_render_all_views` function (passes resource_path to views)

**Type System Considerations:**
- `resource_path` should be typed as `str` (not `str | None`)
- This ensures it's always available and eliminates need for None checks
- Catalog should have `resource_path = ""` (empty string for root)

**Path Calculation Logic:**
- Relative paths should be calculated based on depth in tree
- Depth 1 (Section): `../` to go up one level
- Depth 2 (Subject): `../../` to go up two levels
- Depth 3 (Story): `../../../` to go up three levels
- Each breadcrumb link combines upward traversal with forward path

**Testing Strategy:**
- Test resource_path population for all resource types
- Test view instantiation with resource_path
- Test breadcrumb link generation with relative paths
- Test that Parent links are removed from all view templates
- Verify breadcrumbs render correctly on built pages
- Test all depth levels (Section, Subject, Story)

**Build System Impact:**
- Changes affect static build output (not development server)
- `_render_all_views` in `build.py` is the key integration point
- Ensure resource_path is available during tree traversal for build
