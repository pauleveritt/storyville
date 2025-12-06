# Spec Requirements: Seed CLI

## Initial Description

Seed CLI - Add a CLI argument that will make an example catalog sized small/medium/large. This might require moving `examples/minimal` into `src/storyville` so that it is shipped in the package.

**Source:** From product roadmap: agent-os/product/roadmap.md
**Complexity:** Medium (M)
**Date Initiated:** 2025-11-30

## Requirements Discussion

### First Round Questions

**Q1: Command Syntax** - I assume the command should be `storyville seed <size> <output_directory>`, similar to how `storyville build` and `storyville serve` work. For example: `storyville seed medium var/my_site`. Is that correct?

**Answer:** Correct - `storyville seed <size> <output_directory>` (e.g., `storyville seed medium var/my_site`)

**Q2: Project Structure** - Should the seed command assume it's being run in an existing Python project (with pyproject.toml), or should it create a standalone project structure with its own pyproject.toml, dependencies, etc.?

**Answer:** Presumes existing project, don't make a new python project

**Q3: Catalog Sizes** - For the three sizes, I'm thinking:
- **Small**: 1 Section, 2-3 Subjects, 2 Stories per Subject (4-6 total stories)
- **Medium**: 2-3 Sections, 4-6 Subjects, 2-3 Stories per Subject (12-18 total stories)
- **Large**: 4-5 Sections, 8-12 Subjects, 3-4 Stories per Subject (30-40 total stories)

Does this scale make sense?

**Answer:** Yes - the proposed sizes are good:
- Small: 1 Section, 2-3 Subjects, 2 Stories per Subject (4-6 total stories)
- Medium: 2-3 Sections, 4-6 Subjects, 2-3 Stories per Subject (12-18 total stories)
- Large: 4-5 Sections, 8-12 Subjects, 3-4 Stories per Subject (30-40 total stories)

**Q4: Component Variety** - Should the generated examples demonstrate a variety of component types and patterns (buttons, cards, forms, lists, etc.) and use different Storyville features (assertions, themed layouts, prop variations, tdom patterns)?

**Answer:** Yes - use diverse component types demonstrating assertions, themed layouts, prop variations, and tdom patterns

**Q5: Template Location** - I assume we'll package template files in `src/storyville/templates/seed/` that get included in the distribution. The seed command would then copy/generate from these templates into the user's output directory. Sound right?

**Answer:** Good - use templates from `src/storyville/templates/seed/` packaged with distribution

**Q6: Idempotency** - Should the seed command be idempotent (safe to run multiple times) or fail if the target directory already exists?

**Answer:** Runs once, fail if target directory exists

**Q7: Example Complexity** - Should the generated examples be kept simple and educational, or should they showcase more advanced patterns? I'm thinking we should keep them straightforward but not too minimal.

**Answer:** Not too many examples (keep it simple)

**Q8: Feature Scope** - Are there any specific Storyville features you want to explicitly exclude from the seed examples (like advanced assertion patterns, complex themed layouts, etc.)?

**Answer:** User did not provide explicit exclusions

**Q9: Documentation** - Should we add documentation about this seed command to README.md and docs/?

**Answer:** Yes - Add documentation to README.md and docs/* about this seed command

### Existing Code to Reference

**Similar Features Identified:**

User did not provide specific paths to similar features or existing examples to reference.

**Known References from Context:**
- CLI implementation: `src/storyville/__main__.py` (uses typer, has `serve` and `build` commands)
- Examples directory: `examples/` (may contain example catalogs like `examples/minimal`)
- Template packaging location: `src/storyville/` (suggested location for seed templates)

### Follow-up Questions

**Follow-up 1:** Should the seed templates be entirely new template content created in `src/storyville/templates/seed/`, or should we move/copy the existing `examples/minimal` directory content?

**Answer:** Create entirely new template content in `src/storyville/templates/seed/` (not copying from existing examples)

**Follow-up 2:** Should the generated catalog include a custom ThemedLayout example, demonstrating how users can create their own themed layouts?

**Answer:** Yes, include a custom ThemedLayout example in the generated catalogs

**Follow-up 3:** Should the seed command generate a root `stories.py` file at the output directory root that defines a Catalog and imports the sections/subjects, or should it only generate the component files?

**Answer:** Yes, generate a `stories.py` file at the root of the output directory to define a Catalog with themed_layout

**Follow-up 4:** Should the generated catalog structure be importable as a Python package (with `__init__.py` files), or just a collection of .py files?

**Answer:** Yes, make it importable as a Python package (include `__init__.py` files)

## Visual Assets

### Files Provided:

Visual assets directory check performed - No visual files found in `/Users/pauleveritt/projects/t-strings/storyville/agent-os/specs/2025-11-30-seed-cli/planning/visuals/`

### Visual Insights:

No visual assets provided.

## Requirements Summary

### Functional Requirements

**Core Functionality:**
- Add new `seed` command to Storyville CLI using typer framework
- Accept two arguments: `<size>` (small/medium/large) and `<output_directory>`
- Generate example catalog with appropriate scale based on size parameter
- Fail if output directory already exists (not idempotent)
- Create entirely new template content in `src/storyville/templates/seed/` (do not copy from existing examples)
- Package seed templates as part of distribution
- Generate from templates into user's specified output directory
- Assume operation in existing Python project (don't create new project structure)
- Generate root `stories.py` file defining a Catalog with themed_layout
- Create importable Python package structure with `__init__.py` files

**Catalog Scale by Size:**
- **Small**: 1 Section, 2-3 Subjects, 2 Stories per Subject (4-6 total stories)
- **Medium**: 2-3 Sections, 4-6 Subjects, 2-3 Stories per Subject (12-18 total stories)
- **Large**: 4-5 Sections, 8-12 Subjects, 3-4 Stories per Subject (30-40 total stories)

**Component Variety:**
- Diverse component types (buttons, cards, forms, lists, etc.)
- Demonstrate multiple Storyville features:
  - Story assertions
  - Custom ThemedLayout example
  - Prop variations
  - tdom patterns
- Keep examples simple and educational, not overly complex

**Generated Structure:**
- Root `stories.py` file with Catalog definition and themed_layout
- Sections, subjects, and stories organized in subdirectories
- `__init__.py` files throughout to make it importable as Python package
- Custom ThemedLayout component demonstrating layout customization

**Documentation:**
- Update README.md to include seed command information
- Add/update docs/* to document seed command usage
- Follow existing CLI documentation patterns from `serve` and `build` commands

### Reusability Opportunities

**CLI Patterns:**
- Reference existing CLI structure in `src/storyville/__main__.py`
- Follow typer command patterns from `serve` and `build` commands
- Use similar argument handling and output messaging

**Template Packaging:**
- Follow Python package data patterns for including templates in distribution
- Update `pyproject.toml` to include template files in package data if needed
- Use pathlib for all path operations

**Storyville Patterns:**
- Custom ThemedLayout should follow patterns from existing Storyville layouts
- Component examples should follow tdom patterns
- Catalog structure should mirror standard Storyville organization

### Scope Boundaries

**In Scope:**
- New `seed` CLI command with size and output_directory arguments
- Three predefined sizes (small, medium, large) with specific catalog scales
- Template-based generation from packaged seed templates in `src/storyville/templates/seed/`
- Diverse component examples demonstrating various Storyville features
- Custom ThemedLayout example
- Root `stories.py` with Catalog definition
- Python package structure with `__init__.py` files
- Documentation updates for README.md and docs/
- Directory existence check (fail if target exists)

**Out of Scope:**
- Copying or reusing existing `examples/minimal` content
- Creating new Python project structure with pyproject.toml
- Idempotent operation (will not overwrite existing directories)
- Interactive prompts or customization beyond size selection
- Overly complex or advanced example patterns
- Custom template creation by users

**Deferred/Unclear:**
- Specific features to exclude from examples (user did not specify)
- Exact component examples to include (to be determined during implementation)

### Technical Considerations

**Integration Points:**
- CLI implementation in `src/storyville/__main__.py` using typer
- Template packaging in `src/storyville/templates/seed/`
- Package distribution configuration (pyproject.toml may need updates for template inclusion)
- Documentation in README.md and docs/ directory

**Existing System Constraints:**
- Python 3.14+ required (consistent with Storyville requirements)
- Uses typer for CLI (consistent with existing commands)
- Uses tdom for templating (component examples must use tdom)
- Uses Starlette for web serving (examples should be servable via `storyville serve`)

**Technology Preferences:**
- Modern Python 3.14+ features (structural pattern matching, type hints, PEP 604 syntax)
- pathlib for path handling (per project standards)
- Follow existing code style and formatting (ruff, basedpyright)
- Use pytest for any testing of seed functionality

**Similar Code Patterns:**
- Follow CLI command structure from `serve` and `build` commands
- Use Path objects for file system operations
- Include logging/output messages for user feedback
- Handle errors gracefully with informative messages
- Generate valid Python package structure with proper imports
