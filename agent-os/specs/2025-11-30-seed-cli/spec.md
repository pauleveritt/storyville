# Specification: Seed CLI

## Goal
Add a CLI command to generate example Storyville catalogs with configurable sizes (small/medium/large) for quick prototyping, learning, and testing.

## User Stories
- As a new Storyville user, I want to generate a working example catalog so that I can quickly learn Storyville patterns and structure
- As a developer, I want to create test catalogs of different sizes so that I can validate performance and behavior at scale

## Specific Requirements

**CLI Command Structure**
- Add new `seed` subcommand to existing typer CLI in `src/storyville/__main__.py`
- Command syntax: `storyville seed <size> <output_directory>`
- Size must be one of: `small`, `medium`, or `large`
- Output directory is required and must not already exist (fail with clear error if it does)
- Follow existing CLI patterns from `serve` and `build` commands (logging, messaging, error handling)
- Use pathlib for all path operations consistent with project standards

**Catalog Size Configuration**
- Small: 1 Section with 2-3 Subjects, each Subject has 2 Stories (4-6 total stories)
- Medium: 2-3 Sections with 4-6 Subjects total, each Subject has 2-3 Stories (12-18 total stories)
- Large: 4-5 Sections with 8-12 Subjects total, each Subject has 3-4 Stories (30-40 total stories)
- Use structural pattern matching (`match size:`) to handle size selection

**Template Location and Packaging**
- Create new template content in `src/storyville/templates/seed/` directory structure
- Templates must be packaged as part of distribution using Python package data inclusion
- Update `pyproject.toml` if needed to ensure template files are included in package distribution
- Use `PACKAGE_DIR` constant or similar pattern from existing codebase for locating templates at runtime

**Generated Catalog Structure**
- Root `stories.py` file defining a Catalog with title and themed_layout callable
- Python package structure with `__init__.py` files at each level for importability
- Directory organization: sections as subdirectories, subjects as nested subdirectories within sections
- Each subject directory contains a `stories.py` file defining a Subject with target component and Story instances
- Components defined in separate files (e.g., `button.py`, `card.py`) alongside their `stories.py`
- Custom ThemedLayout component in dedicated subdirectory demonstrating layout customization patterns

**Component Variety and Patterns**
- Generate diverse component types: Button, Card, Form, List, Badge variations
- Each component should demonstrate tdom patterns using `html` module and t-string syntax
- Include story assertions on selected stories (at least 2-3 per size) to demonstrate assertion patterns
- Show prop variations across stories (different text, colors, states, sizes)
- Keep component implementations simple and educational (avoid over-engineering)
- Follow modern Python 3.14+ patterns: type hints, dataclasses where appropriate, PEP 604 union syntax

**ThemedLayout Implementation**
- Create a custom ThemedLayout component following the pattern shown in README.md
- Layout should be a dataclass with `story_title` and `children` parameters
- Implement `__call__` method returning tdom Node with full HTML document structure
- Include inline styles demonstrating custom theming (background gradient, typography, container styling)
- Store in dedicated subdirectory (e.g., `themed_layout/themed_layout.py`) within generated catalog
- Root `stories.py` should import and wrap ThemedLayout as a callable for Catalog configuration

**Story Assertions**
- Include sample assertion callables demonstrating common patterns (element type checks, content validation, attribute verification)
- Assertions should be simple, educational functions that test rendered output
- Follow type signature: `Callable[[Element | Fragment], None]`
- Place assertions as module-level functions before Subject definition in `stories.py` files

**Directory Existence Check**
- Check if output_directory exists before any generation
- If exists, fail immediately with clear error message: "Output directory already exists: {path}"
- Do not prompt for overwrite confirmation (not idempotent by design)
- Use `Path.exists()` for check

## Visual Design
No visual assets provided for this specification.

## Existing Code to Leverage

**CLI Patterns from `__main__.py`**
- Use typer.Typer() app instance for command registration
- Follow `@app.command()` decorator pattern for seed command
- Use `typer.Argument()` with help text for positional arguments
- Use `typer.echo()` for user feedback messages during execution
- Include logging setup with `logging.basicConfig()` for build phase information

**Catalog/Section/Subject/Story Models**
- Follow dataclass patterns from `catalog/models.py`, `section/models.py`, `subject/models.py`, `story/models.py`
- Use proper parent/items relationships in generated hierarchies
- Catalog has `themed_layout` parameter accepting `Callable[..., Node] | None`
- Subject has `target`, `description`, and `items` list of Story instances
- Story has `props`, `title`, `description`, `assertions` list, and `template`

**Storyville Package Structure**
- Follow existing package organization with `__init__.py` exports
- Use `make_catalog()` helper pattern for catalog discovery
- Generated catalogs should work with `storyville serve <output_dir>` and `storyville build <output_dir> <build_output>`

**ThemedLayout Pattern**
- Reference ThemedStory component from `components/themed_story/` for integration understanding
- Follow dataclass callable pattern with `story_title` and `children` parameters
- Return tdom Node with complete HTML document structure
- Use tdom t-string syntax for HTML generation with embedded Python expressions

**Build System and Packaging**
- Project uses uv_build backend and requires-python >= 3.14
- CLI entry point defined in `[project.scripts]` as `storyville = "storyville.__main__:main"`
- Template packaging should follow Python package data best practices for file inclusion

## Out of Scope
- Copying or moving existing `examples/minimal` content (create entirely new templates)
- Creating new Python project structure with pyproject.toml, requirements.txt, or virtual environment
- Interactive prompts or customization wizard beyond size parameter
- Idempotent operation allowing overwrites (explicitly fail if directory exists)
- Custom template creation or modification by users
- Advanced component patterns beyond simple educational examples
- Integration with external component libraries
- Configuration file for seed command customization
- Deletion or cleanup of previously generated catalogs
- Version control initialization (git init) in generated directory
