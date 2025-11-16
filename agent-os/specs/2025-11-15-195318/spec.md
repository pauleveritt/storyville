# Specification: Site Package Refactoring

## Goal
Extract Site, SiteView, and helper functions into a dedicated `storytime/site/` package following the same structure as existing story/section/subject packages, and refactor all node types to use `.items` for consistency.

## User Stories
- As a developer, I want Site organized in its own package so that the codebase follows consistent modular architecture
- As a maintainer, I want all node types to use `.items` for child collections so that the API is predictable and uniform

## Specific Requirements

**Create site package structure**
- Create new directory `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/site/`
- Create four modules: `models.py`, `views.py`, `helpers.py`, and `__init__.py`
- Follow exact file structure pattern used in story/, section/, and subject/ packages
- Package should be self-contained with clear separation of concerns

**Implement Site model in models.py**
- Move Site class from `site.py` to `site/models.py`
- Site must inherit from `BaseNode["Site"]` (not standalone dataclass)
- Keep existing fields: `name`, `parent`, `title`, `context`, `package_path`, `items`, `static_dir`
- Keep `__post_init__()` logic for static directory detection in models.py
- Keep `post_update()` method for parent/tree_node processing
- Remove `find_path()` method from Site class (will be standalone helper)

**Implement SiteView in views.py**
- Create new SiteView class following SectionView pattern
- Must have `site: Site` dataclass field
- Implement `__call__(self) -> Node` method for rendering
- Render site title in h1, list of sections as links, or empty state message
- DO NOT include parent link (Site is root, has no parent)
- Use tdom for HTML rendering with t-string interpolation

**Extract helper functions to helpers.py**
- Move `make_site()` function from `site.py` to `site/helpers.py` as standalone function
- Move `find_path()` from Site class method to `site/helpers.py` as standalone function
- `find_path(site: Site, path: str) -> Site | Section | Subject | Story | None` signature
- Both functions must preserve exact current logic and behavior
- Update imports within helpers.py to use relative imports where appropriate

**Export public API from __init__.py**
- Export Site, SiteView, make_site, and find_path from `site/__init__.py`
- Follow pattern: `from storytime.site.models import Site`
- Use `__all__` list for explicit exports: `__all__ = ["Site", "SiteView", "make_site", "find_path"]`
- Enable clean imports: `from storytime.site import Site, SiteView, make_site, find_path`

**Refactor Subject.stories to Subject.items**
- Rename `stories: list[Story]` field to `items: list[Story]` in `subject/models.py`
- Update ALL references in `subject/views.py` from `self.subject.stories` to `self.subject.items`
- Update reference in `site/helpers.py` make_site() from `subject.stories` to `subject.items`
- Update ALL test files that reference `subject.stories` to use `subject.items`
- Ensure consistency: Section.items (dict), Subject.items (list), Site.items (dict)

**Update site.py imports**
- Delete old `site.py` file completely after extracting all code
- Update any imports of `from storytime.site import Site, make_site` throughout codebase
- Change to `from storytime.site import Site, make_site` (import path stays same, but now from package)
- Verify no breaking changes for external consumers

**Update find_path() call sites**
- Find all locations calling `site.find_path(path)`
- Update to `find_path(site, path)` using new standalone function
- Update import statements to include find_path from storytime.site
- Ensure type hints remain correct at call sites

**Maintain type safety**
- All type hints must use modern Python syntax (PEP 604: `X | Y`, not `Union[X, Y]`)
- Use `TYPE_CHECKING` guard for circular import prevention
- Preserve existing generic type parameter in BaseNode["Site"]
- Update find_path return type to include all node types

**Testing coverage**
- All existing tests must continue to pass after refactoring
- Update test imports to use new package structure
- Update test assertions that reference Subject.stories to use Subject.items
- Verify make_site() and find_path() work correctly as standalone functions

## Visual Design
No visual assets provided.

## Existing Code to Leverage

**Section package structure at `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/section/`**
- Use as exact template for Site package organization
- models.py has Section dataclass inheriting from BaseNode["Section"]
- views.py has SectionView with __call__() -> Node method
- __init__.py exports Section and SectionView with __all__ list
- Follow identical import patterns and module organization

**Subject package structure at `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/subject/`**
- Reference for consistent package layout
- Shows pattern of parent: Section | None field
- views.py demonstrates rendering list of child items with empty state handling
- Use tdom html() with t-strings for template interpolation

**Story package structure at `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/story/`**
- Only has models.py and views.py (no helpers.py needed for Story)
- Shows minimal package structure when helpers not needed
- StoryView demonstrates parent link rendering: `<a href="..">Parent</a>`

**BaseNode implementation in `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/nodes.py`**
- Site must inherit from BaseNode["Site"] using PEP 695 generic syntax
- Provides post_update() method that Site currently overrides
- Handles name, parent, package_path, and title logic
- Site needs custom post_update() for static_dir handling

**Current Site implementation in `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/site.py`**
- Lines 15-73 contain Site class to move to site/models.py
- Lines 75-136 contain make_site() function to move to site/helpers.py
- find_path() method (lines 64-72) to extract as standalone function in helpers.py
- Preserve all logic, imports, and type hints exactly

## Out of Scope
- Modifying build.py or any build logic
- Modifying CLI commands or entry points
- Changes to TreeNode class or node scanning logic
- Maintaining backward compatibility for old import paths (breaking change is acceptable)
- Adding new features or capabilities to Site, SiteView, or helpers
- Refactoring Section.items or Site.items (already use .items correctly)
- Creating documentation or migration guides
- Performance optimizations or algorithmic improvements
- Changes to Story package (has no child collections)
- Type system changes beyond maintaining existing type hints
