# Spec Requirements: Site to Catalog

## Initial Description

Site to Catalog.

Rename "Site" to "Catalog" and update the docs to refer to a collection of sections/stories as a "Catalog".

## Requirements Discussion

### First Round Questions

**Q1:** For the scope of the rename, should this be comprehensive throughout the codebase (class names, module names, function names, variables, documentation), or are there specific areas where "Site" should remain (e.g., for backwards compatibility)?

**Answer:** Yes, comprehensive rename throughout codebase (class names, module names, function names, variables, documentation). Don't worry about backwards compatibility.

**Q2:** For the hierarchy terminology, I'm assuming we're updating to "Catalog → Section → Subject → Story" and keeping the other terms (Section, Subject, Story) as-is. Is that correct?

**Answer:** Yes, update to "Catalog → Section → Subject → Story", keeping other terms unchanged.

**Q3:** For the file structure, should `storyville/site` directory be renamed to `storyville/catalog`?

**Answer:** Yes, rename `storyville/site` to `storyville/catalog`

**Q4:** For user-facing API, should `this_site()` function become `this_catalog()`, and similar for any other site-related function names?

**Answer:** Yes, `this_site()` becomes `this_catalog()`

**Q5:** For CLI and user-facing messages, should commands like `storyville serve` remain the same, but internal messages update to say "Building catalog..." instead of "Building site..."?

**Answer:** Yes, CLI commands remain as `storyville serve` and `storyville build`, but internal messages update to "Building catalog..." etc.

**Q6:** Regarding backward compatibility, should we provide any deprecation warnings or aliases for the old "Site" naming, or is this acceptable as a breaking change?

**Answer:** No backward compatibility needed (breaking change acceptable)

**Q7:** For documentation updates, should all references to "site" as a concept be updated to "catalog", including phrases like "your site" becoming "your catalog" and conceptual explanations?

**Answer:** Yes, update all documentation phrases and conceptual explanations

**Q8:** Are there any specific areas that should NOT be renamed? For example, should any internal implementation details, third-party integrations, or specific technical terms remain as "site"?

**Answer:** No exclusions - rename everything

**Q9:** Do you have existing features with similar rename/refactor patterns we should reference?

**Answer:** None provided

**Q10:** Do you have any design mockups, wireframes, or screenshots?

**Answer:** None provided

### Existing Code to Reference

No similar existing features identified for reference.

### Follow-up Questions

No follow-up questions were needed. Requirements are clear and comprehensive.

## Visual Assets

### Files Provided:

No visual assets provided.

### Visual Insights:

Not applicable - this is a refactoring task.

## Requirements Summary

### Functional Requirements

**Comprehensive Renaming Across All Layers:**
- Rename all Python class names from `Site` to `Catalog`
- Rename all module/package names from `site` to `catalog`
- Rename all function names containing "site" to use "catalog"
- Rename all variable names from `site` to `catalog`
- Update all type hints and type aliases
- Update all docstrings and code comments

**Hierarchy Terminology Update:**
- Update conceptual hierarchy from "Site → Section → Subject → Story" to "Catalog → Section → Subject → Story"
- Keep "Section", "Subject", and "Story" terminology unchanged
- Update all documentation explaining the hierarchy

**File Structure Changes:**
- Rename directory `storyville/site` to `storyville/catalog`
- Update all import statements throughout the codebase
- Ensure all module paths reflect the new structure

**User-Facing API Changes:**
- Rename `this_site()` function to `this_catalog()`
- Update any other public API functions containing "site" terminology
- Maintain same function signatures and behavior

**CLI and Messages:**
- Keep CLI commands unchanged: `storyville serve`, `storyville build`
- Update all user-facing messages: "Building site..." becomes "Building catalog..."
- Update progress indicators, error messages, and logs
- Update help text and command descriptions

**Documentation Updates:**
- Update all conceptual references from "site" to "catalog"
- Change phrases like "your site" to "your catalog"
- Update README, getting started guides, tutorials
- Update API documentation and docstrings
- Update example code and comments

### Reusability Opportunities

No similar existing features identified for reuse patterns.

### Scope Boundaries

**In Scope:**
- All Python source code (classes, functions, variables, types)
- All module and package names
- All directory structure
- All documentation (README, guides, docstrings, comments)
- All user-facing messages and CLI output
- All test code and test fixtures
- All example code

**Out of Scope:**
- CLI command names (remain as `storyville serve`, `storyville build`)
- Backward compatibility or deprecation warnings
- No aliases for old "Site" naming

### Technical Considerations

**Breaking Change Acceptance:**
- This is an acceptable breaking change
- No migration path or deprecation period required
- No backward compatibility needed

**Framework Independence:**
- Changes affect core Storyville components only
- Must maintain framework-independent architecture
- Component rendering and story system unchanged functionally

**Product Alignment:**
- Aligns with Storyville's mission as a "component-driven development platform"
- "Catalog" better describes the visual browseable collection of components
- Improves clarity of the hierarchical organization system
- Consistent with roadmap item #6: "Component Organization System"

**Testing Requirements:**
- All existing tests must be updated to use new terminology
- Test suite must pass after rename (`just test`)
- Type checking must pass (`just typecheck`)
- Formatting must pass (`just fmt`)
- No change in test coverage or functionality

**Import and Module Updates:**
- Update all `from storyville.site import ...` to `from storyville.catalog import ...`
- Update any `__init__.py` files that expose site-related APIs
- Ensure all internal cross-module references are updated
