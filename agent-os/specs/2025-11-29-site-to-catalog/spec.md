# Specification: Site to Catalog Rename

## Goal
Comprehensively rename "Site" to "Catalog" throughout the Storytime codebase to better reflect the visual browseable collection nature of the component hierarchy.

## User Stories
- As a developer, I want consistent terminology throughout the codebase so that the hierarchy "Catalog → Section → Subject → Story" is clear
- As a user of Storytime, I want documentation and messages to refer to "catalog" so that I understand I'm building a browseable component collection

## Specific Requirements

**Directory and Module Structure Rename**
- Rename `storytime/site` directory to `storytime/catalog`
- Update `storytime/catalog/__init__.py` to export Catalog-related symbols
- Ensure all internal imports within the catalog package are updated
- Maintain the same module structure (models.py, helpers.py, views.py)

**Core Class and Function Renames**
- Rename `Site` class to `Catalog` in models.py
- Rename `SiteView` class to `CatalogView` in views.py
- Rename `make_site()` function to `make_catalog()` in helpers.py
- Rename `find_path()` first parameter from `site` to `catalog`
- Update all type hints that reference Site to use Catalog

**Public API Updates**
- Update `storytime/__init__.py` to export `Catalog` instead of `Site`
- Rename `this_site()` function references to `this_catalog()` in documentation
- Update `__all__` lists in affected modules to use new naming
- Maintain same function signatures (only names change)

**Import Statement Updates**
- Change `from storytime.site import` to `from storytime.catalog import` throughout codebase
- Update Section model's TYPE_CHECKING import from `storytime.site` to `storytime.catalog`
- Update all cross-module references that import Site-related components
- Verify no broken imports remain in src/ and tests/ directories

**Type Hints and Type Aliases**
- Update all type hints from `Site` to `Catalog`
- Update parent type hints in Section model from `Site | None` to `Catalog | None`
- Update return types of functions that return Site to return Catalog
- Update any union types that include Site

**Variable and Parameter Naming**
- Rename local variables named `site` to `catalog` in all functions
- Update function parameters from `site` to `catalog` where applicable
- Update dataclass field names if they reference "site"
- Ensure consistency across helpers.py, models.py, views.py, and other modules

**Documentation String Updates**
- Update all docstrings from "site" to "catalog" conceptually
- Change phrases like "The site contains" to "The catalog contains"
- Update function docstrings to reference catalog terminology
- Update class docstrings to explain catalog hierarchy
- Revise README.md to use catalog terminology throughout
- Update inline code comments that mention site

**User-Facing Messages**
- Update CLI output messages from "Building site..." to "Building catalog..."
- Update progress indicators to reference catalog
- Update error messages that mention site to use catalog
- Keep CLI command names unchanged (`storytime serve`, `storytime build`)

**Test File Updates**
- Update all test files that reference Site to use Catalog
- Update test fixture names from `site` to `catalog`
- Update test function names that include "site" to use "catalog"
- Update test assertions and mock objects to use new terminology
- Ensure conftest.py examples use Catalog naming

**Hierarchy Concept Updates**
- Update all documentation explaining hierarchy from "Site → Section → Subject → Story" to "Catalog → Section → Subject → Story"
- Update README.md architecture section to show Catalog at the top
- Keep "Section", "Subject", and "Story" terminology unchanged
- Update conceptual references in docstrings and comments

## Visual Design
No visual assets provided - this is a code refactoring task.

## Existing Code to Leverage

**Site Package Structure Pattern**
- Follow the existing three-file structure (models.py, helpers.py, views.py) within the catalog package
- Maintain the same architectural pattern of separating models, helper functions, and view components
- Keep the `__init__.py` export pattern for clean public API
- Preserve the BaseNode inheritance pattern in Catalog class

**BaseNode Inheritance Pattern**
- Site class extends `BaseNode["Site"]` which should become `BaseNode["Catalog"]`
- Maintain the same fields (parent, items, themed_layout) with updated type hints
- Keep the post_update() method pattern if implemented
- Follow the same dataclass decorator pattern used throughout

**TreeNode and Package Loading Pattern**
- The `make_site()` function uses TreeNode pattern for loading stories.py files
- Keep the same package discovery logic (rglob for stories.py)
- Maintain the structural pattern matching with `case Site()` becoming `case Catalog()`
- Preserve the parent-child relationship building logic

**Type Checking Imports Pattern**
- Use `TYPE_CHECKING` block in Section model for circular import avoidance
- Follow the same pattern in catalog/models.py if needed
- Maintain the forward reference pattern used in type hints
- Keep the `from __future__ import annotations` pattern where used

**View Protocol Pattern**
- SiteView implements the View Protocol with `__call__() -> Node` method
- Maintain the same pattern for CatalogView
- Keep the Layout component integration pattern
- Preserve the tdom Node return type and html template structure

## Out of Scope
- Changing CLI command names (`storytime serve` and `storytime build` remain unchanged)
- Providing backward compatibility or deprecation warnings
- Creating aliases for old "Site" naming
- Adding migration guides or transition documentation
- Changing behavior or functionality (only naming changes)
- Modifying the component rendering logic or story system
- Updating third-party dependencies or external integrations
- Changes to other hierarchy levels (Section, Subject, Story remain unchanged)
- Performance optimizations or architectural refactoring beyond the rename
- Adding new features or capabilities during the rename
