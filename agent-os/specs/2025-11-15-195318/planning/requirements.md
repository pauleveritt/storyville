# Spec Requirements: Site refactoring

## Initial Description
"Make a Site in storytime/site with models.py and views.py. Extract make_site and find_path to helpers. The Site should be a tree of nodes, similar to the existing implementation."

## Requirements Discussion

### First Round Questions

**Q1:** I assume you want Site to be a dataclass in models.py with the same structure as Section and Subject (with title, path, items, etc.). Is that correct?
**Answer:** Yes - Site dataclass in models.py with same structure as Section/Subject

**Q2:** For the view layer (views.py), I'm thinking SiteView should follow the same pattern as SectionView and SubjectView with view() method and render() method. Should we include a parent link in the Site view, or should it be omitted since Site is the root?
**Answer:** Correct - SiteView follows same pattern, omit parent link

**Q3:** For the helpers module, should both make_site() and find_path() be standalone functions in helpers.py, or should make_site() be a Site method and only find_path() be a standalone helper?
**Answer:** Both should be standalone functions - Both make_site() and find_path() as standalone functions in helpers.py

**Q4:** I assume Site should inherit from BaseNode["Site"] just like the other node types. Is that correct?
**Answer:** Yes, inherit - Site should inherit from BaseNode["Site"]

**Q5:** The existing Section and Subject have __post_init__() logic for building their item collections. Should Site follow this same pattern with its logic in __post_init__() in models.py, or should that logic be in the make_site() helper?
**Answer:** Keep in post_init - __post_init__() logic stays in models.py

**Q6:** Looking at the existing code, I notice Story has .stories, Section has .sections, but Subject uses .items. Should Site use .sites for consistency with Story/Section pattern, or .items for consistency with Subject? Or should we refactor all three to be consistent?
**Answer:** Yes, refactor all 3 to be consistent - This means Subject.stories should become Subject.items for consistency

**Q7:** Should the site/__init__.py export Site, SiteView, and the helper functions for easy imports, just like the other packages do?
**Answer:** Yes - Export Site, SiteView, and helpers from site/__init__.py

**Q8:** Since you're extracting make_site from its current location, should we maintain backward compatibility by keeping the old import path working, or is a breaking change acceptable?
**Answer:** Breaking change is ok - No backward compatibility needed for make_site exports

**Q9:** Is there anything you specifically want to exclude from this refactoring? For example, should we leave the build.py or any CLI commands untouched for now?
**Answer:** Leave build.py and everything outside untouched - Only refactor the Site package itself

### Existing Code to Reference

**Similar Features Identified:**
- Feature: Story package - Path: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/story/`
- Feature: Section package - Path: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/section/`
- Feature: Subject package - Path: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/subject/`
- Pattern to follow: All three packages have models.py, views.py, and __init__.py with consistent structure
- Note: These packages provide the exact pattern to follow for the Site implementation

### Follow-up Questions

**Follow-up Q1:** In Q6 you said "refactor all 3 to be consistent" - which naming convention should we standardize on?

Option A: Each node type uses `.items` for ALL collections (Section.items, Subject.items, Site.items) - generic naming
Option B: Each node type uses specific names (.sections, .subjects, .stories, .sites) - semantic naming

**Answer:** Option A - Each node type uses `.items` for ALL collections (Section.items, Subject.items, Site.items) - generic naming

This means:
- Site.items (dict of Sections) - already uses .items ✓
- Section.items (dict of Subjects) - already uses .items ✓
- Subject.stories → Subject.items (list of Stories) - needs refactoring
- Story has no child collections

**Follow-up Q2:** For the Subject.stories → Subject.items refactor, should we:

Option A: Update ALL references to Subject.stories throughout the entire codebase (including views.py, stories.py, site.py, tests, etc.) to use Subject.items
Option B: Just update the Subject model and leave other references as-is for now (minimal change)

**Answer:** Option A - Update ALL references to Subject.stories throughout the entire codebase (including views.py, stories.py, site.py, tests, etc.) to use Subject.items

## Visual Assets

### Files Provided:
No visual assets provided.

### Visual Insights:
Not applicable.

## Requirements Summary

### Functional Requirements
- Create new `src/storytime/site/` package with three modules: models.py, views.py, helpers.py, and __init__.py
- Site dataclass in models.py should inherit from BaseNode["Site"] with same structure as Section/Subject
- Site should have __post_init__() logic for building its item collections (following Section/Subject pattern)
- SiteView in views.py should follow SectionView/SubjectView pattern with view() and render() methods
- SiteView should NOT include parent link since Site is the root node
- Extract make_site() function to helpers.py as standalone function
- Extract find_path() function to helpers.py as standalone function
- Export Site, SiteView, make_site, and find_path from site/__init__.py
- **REFACTOR: Subject.stories → Subject.items** for consistency with `.items` convention
- **UPDATE ALL REFERENCES: Update every reference to Subject.stories throughout the entire codebase** (views.py, stories.py, site.py, tests, etc.) to use Subject.items
- **STANDARDIZE: All node types use `.items` for child collections** (Section.items, Subject.items, Site.items)

### Reusability Opportunities
- Follow exact package structure from story/, section/, subject/ packages
- Reuse BaseNode inheritance pattern
- Reuse __post_init__() pattern for collection building
- Reuse view() and render() method patterns from existing View classes
- Apply consistent export pattern from existing __init__.py files

### Scope Boundaries
**In Scope:**
- Create site/ package with models.py, views.py, helpers.py, __init__.py
- Implement Site dataclass with BaseNode inheritance
- Implement SiteView class (without parent link)
- Move make_site() to site/helpers.py
- Move find_path() to site/helpers.py
- **Refactor Subject.stories to Subject.items** for consistency
- **Update ALL codebase references to Subject.stories → Subject.items** (views.py, stories.py, site.py, all tests, etc.)
- Export all public APIs from site/__init__.py

**Out of Scope:**
- Modifying build.py
- Modifying CLI commands
- Maintaining backward compatibility for make_site imports
- Any changes to code outside the site/ package (except for the comprehensive Subject.stories → Subject.items refactor)

### Technical Considerations
- Breaking change acceptable for make_site() import path
- Must inherit from BaseNode["Site"] following existing pattern
- Must implement __post_init__() in models.py following existing pattern
- SiteView.render() should omit parent link since Site is root
- **Comprehensive consistency refactor: Subject.stories → Subject.items everywhere in codebase**
- **All node types standardized to use `.items` for their child collections**
- Follow exact module organization from story/, section/, subject/ packages
- The Subject.stories → Subject.items refactor must be thorough - update models, views, helpers, tests, and any other references
