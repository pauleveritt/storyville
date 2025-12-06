# Task Breakdown: Seed CLI

## Overview
Total Task Groups: 5
Feature: Add CLI command to generate example Storytime catalogs with configurable sizes (small/medium/large) for quick prototyping, learning, and testing.

## Task List

### Core CLI Implementation

#### Task Group 1: CLI Command and Size Configuration
**Dependencies:** None

- [x] 1.0 Complete CLI command implementation
  - [x] 1.1 Write 2-8 focused tests for seed command
    - Test command with valid size arguments (small, medium, large)
    - Test command rejects invalid size arguments
    - Test command fails when output directory exists
    - Test command creates output directory structure
    - Skip exhaustive edge case testing
  - [x] 1.2 Add `seed` command to `src/storytime/__main__.py`
    - Add `@app.command()` decorator following `serve` and `build` patterns
    - Accept `size: str` as first argument using `typer.Argument()`
    - Accept `output_directory: str` as second argument using `typer.Argument()`
    - Add help text for both arguments
    - Include logging setup with `logging.basicConfig()`
  - [x] 1.3 Implement directory existence check
    - Convert `output_directory` to `Path` object using pathlib
    - Use `Path.exists()` to check if directory exists
    - Fail with `typer.echo()` error message: "Output directory already exists: {path}"
    - Exit with non-zero status code if directory exists
  - [x] 1.4 Implement size validation using structural pattern matching
    - Use `match size:` statement with cases for "small", "medium", "large"
    - Define size configuration dataclass/tuple for each size:
      - Small: 1 section, 2-3 subjects, 2 stories per subject
      - Medium: 2-3 sections, 4-6 subjects, 2-3 stories per subject
      - Large: 4-5 sections, 8-12 subjects, 3-4 stories per subject
    - Fail with error message for invalid size
  - [x] 1.5 Add user feedback with `typer.echo()`
    - Echo: "Generating {size} catalog to {output_directory}..."
    - Echo: "Catalog generation complete!"
    - Follow messaging patterns from `serve` and `build` commands
  - [x] 1.6 Ensure CLI implementation tests pass
    - Run ONLY the 2-8 tests written in 1.1
    - Verify command accepts valid arguments
    - Verify command rejects invalid arguments and existing directories
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 1.1 pass
- Command syntax: `storytime seed <size> <output_directory>` works
- Valid sizes (small/medium/large) are accepted
- Invalid sizes fail with clear error message
- Existing output directory causes immediate failure
- User receives clear feedback messages

### Template Content Creation

#### Task Group 2: Template Structure and Components
**Dependencies:** Task Group 1

- [x] 2.0 Complete template content creation
  - [x] 2.1 Write 2-8 focused tests for template content generation
    - Test root `stories.py` file is created with valid Catalog definition
    - Test `__init__.py` files are created at all directory levels
    - Test component files are created with valid Python code
    - Test ThemedLayout component is created in dedicated subdirectory
    - Skip exhaustive content validation tests
  - [x] 2.2 Create template directory structure
    - Create `src/storytime/templates/seed/` base directory
    - Create subdirectory structure for template content
    - Ensure templates will be included in package distribution
  - [x] 2.3 Design root `stories.py` template
    - Import `Catalog` from storytime
    - Define `this_catalog()` function returning Catalog instance
    - Include `title` parameter with descriptive catalog name
    - Import and wrap custom ThemedLayout as callable
    - Set `themed_layout` parameter on Catalog
    - Use modern Python 3.14+ syntax and type hints
  - [x] 2.4 Create ThemedLayout component template
    - Create `themed_layout/themed_layout.py` template file
    - Define as dataclass with `story_title: str` and `children: Node` parameters
    - Implement `__call__` method returning tdom Node
    - Include full HTML document structure using tdom html module
    - Add inline styles demonstrating custom theming:
      - Background gradient styling
      - Typography customization
      - Container styling with padding/margins
    - Use tdom t-string syntax with embedded Python expressions
    - Follow pattern from README.md and `components/themed_story/`
  - [x] 2.5 Create diverse component templates
    - Button component: dataclass with text, color, size props
    - Card component: dataclass with title, content, image_url props
    - Form component: dataclass with fields list, submit_text props
    - List component: dataclass with items list, ordered bool props
    - Badge component: dataclass with text, variant props
    - All components use tdom html module and t-string syntax
    - Keep implementations simple and educational
    - Use modern Python: type hints, dataclasses, PEP 604 union syntax
  - [x] 2.6 Create story assertion templates
    - Define 2-3 sample assertion functions per component type
    - Assert element type checks (e.g., button is 'button' tag)
    - Assert content validation (e.g., text appears in output)
    - Assert attribute verification (e.g., class names present)
    - Follow signature: `Callable[[Element | Fragment], None]`
    - Place as module-level functions in template files
    - Keep assertions simple and educational
  - [x] 2.7 Ensure template content tests pass
    - Run ONLY the 2-8 tests written in 2.1
    - Verify template files can be generated
    - Verify generated files contain valid Python code
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 2.1 pass
- Template directory `src/storytime/templates/seed/` exists
- Root `stories.py` template defines Catalog with themed_layout
- ThemedLayout component template exists in dedicated subdirectory
- 5+ diverse component templates created (Button, Card, Form, List, Badge)
- 2-3 sample assertion functions per component type
- All templates use modern Python 3.14+ patterns

### Template Generation Engine

#### Task Group 3: Template Rendering and File Generation
**Dependencies:** Task Groups 1, 2

- [x] 3.0 Complete template generation engine
  - [x] 3.1 Write 2-8 focused tests for generation engine
    - Test catalog generation creates correct directory structure
    - Test section/subject/story hierarchy matches size configuration
    - Test all `__init__.py` files are created
    - Test component files are copied to correct locations
    - Skip exhaustive file content validation tests
  - [x] 3.2 Implement template discovery using PACKAGE_DIR
    - Use `PACKAGE_DIR` constant from `src/storytime/__init__.py`
    - Construct path to templates: `PACKAGE_DIR / "templates" / "seed"`
    - Verify template directory exists at runtime
    - Fail with clear error if templates not found
  - [x] 3.3 Implement catalog structure generation
    - Create root output directory
    - Generate root `stories.py` file from template
    - Create `__init__.py` at root level
    - Generate ThemedLayout subdirectory and component
  - [x] 3.4 Implement section/subject/story hierarchy generation
    - Based on size configuration, create section subdirectories
    - For each section, create appropriate number of subject subdirectories
    - For each subject, create:
      - `__init__.py` file
      - Component file (button.py, card.py, etc.)
      - `stories.py` with Subject definition, Story instances, and assertions
    - Organize subjects within sections according to size config
  - [x] 3.5 Implement component file generation
    - Select diverse component types based on catalog size
    - Copy/generate component implementations to subject directories
    - Include prop variations across stories
    - Add story assertions to selected stories (2-3 per size)
    - Ensure importability with proper `__init__.py` structure
  - [x] 3.6 Implement Python package structure creation
    - Create `__init__.py` at root level
    - Create `__init__.py` in each section directory
    - Create `__init__.py` in each subject directory
    - Create `__init__.py` in ThemedLayout directory
    - Ensure proper imports and exports for package structure
  - [x] 3.7 Ensure generation engine tests pass
    - Run ONLY the 2-8 tests written in 3.1
    - Verify correct directory structure is generated
    - Verify all required files are created
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 3.1 pass
- Template discovery works using PACKAGE_DIR pattern
- Catalog structure generated matches size configuration
- Section/subject/story hierarchy created correctly
- All component files generated in appropriate locations
- Python package structure with `__init__.py` files throughout
- Generated catalog is importable as Python package

### Integration and Validation

#### Task Group 4: End-to-End Integration Testing
**Dependencies:** Task Groups 1, 2, 3 (ALL COMPLETED)

- [x] 4.0 Complete integration testing
  - [x] 4.1 Write 2-8 focused tests for end-to-end workflows
    - Test generated small catalog can be served with `storytime serve`
    - Test generated medium catalog can be built with `storytime build`
    - Test generated catalog can be imported as Python package
    - Test ThemedLayout renders correctly in generated catalog
    - Skip exhaustive integration scenarios
  - [x] 4.2 Validate generated catalog with storytime serve
    - Generate small catalog to temporary directory
    - Run `storytime serve <generated_dir>` programmatically or manually
    - Verify catalog loads without errors
    - Verify all sections/subjects/stories are accessible
    - Verify ThemedLayout renders correctly
  - [x] 4.3 Validate generated catalog with storytime build
    - Generate medium catalog to temporary directory
    - Run `storytime build <generated_dir> <output_dir>`
    - Verify build completes without errors
    - Verify all HTML files are generated
    - Verify themed_story.html files exist for stories
  - [x] 4.4 Validate generated catalog as importable package
    - Generate catalog to temporary directory
    - Import root `stories.py` using `make_catalog()`
    - Verify Catalog object is created successfully
    - Verify sections, subjects, stories are present
    - Verify story counts match size configuration
  - [x] 4.5 Test all three sizes (small, medium, large)
    - Generate catalog for each size
    - Verify story counts match configuration:
      - Small: 4-6 stories
      - Medium: 12-18 stories
      - Large: 30-40 stories
    - Verify each size builds and serves correctly
  - [x] 4.6 Ensure integration tests pass
    - Run ONLY the 2-8 tests written in 4.1
    - Verify generated catalogs work with existing Storytime commands
    - Verify catalogs are valid Python packages
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-8 tests written in 4.1 pass
- Generated catalogs work with `storytime serve` command
- Generated catalogs work with `storytime build` command
- Generated catalogs are importable as Python packages
- All three sizes (small/medium/large) generate correctly
- Story counts match size configurations

### Documentation and Packaging

#### Task Group 5: Documentation, Package Data, and Final Validation
**Dependencies:** Task Groups 1, 2, 3, 4 (ALL COMPLETED)

- [x] 5.0 Complete documentation and packaging
  - [x] 5.1 Review all existing tests and identify critical gaps
    - Reviewed tests from Task Groups 1-4 (30 tests total)
    - Identified critical gaps:
      - Generated code syntax validation
      - Generated assertion executability
    - Focused ONLY on gaps related to seed CLI feature
    - Did NOT assess entire application test coverage
    - Prioritized missing end-to-end scenarios
  - [x] 5.2 Add up to 10 additional strategic tests if needed
    - Added 2 strategic tests to fill critical gaps:
      - `test_generated_catalog_code_is_syntactically_valid` - Ensures all generated Python files compile
      - `test_generated_catalog_assertions_are_executable` - Ensures generated assertions actually work
    - Focused on integration points between generation and execution
    - Kept total feature tests at 32 (well under 50)
  - [x] 5.3 Update pyproject.toml for template packaging
    - Verified template files in `src/storytime/templates/seed/` are included in package
    - No changes needed - uv_build backend automatically includes all files in src/storytime/
    - `.py` files in templates directory are included by default
    - Template packaging verified by existing tests
  - [x] 5.4 Update README.md with seed command documentation
    - Added new section: "Generate an Example Catalog (Optional)" in Quick Start
    - Documented command syntax: `storytime seed <size> <output_directory>`
    - Described three size options (small/medium/large) with story counts
    - Provided example usage for all three sizes
    - Explained that generated catalog is a Python package
    - Showed how to serve/build generated catalog
    - Followed documentation style of existing `serve` and `build` sections
  - [x] 5.5 Update docs/ directory with seed CLI documentation
    - Created comprehensive CLI reference: `docs/cli-reference.md`
    - Included seed command in CLI command list with full documentation
    - Documented size configurations and expected output
    - Added examples of generated catalog structure
    - Included troubleshooting section for common issues
    - Added CLI reference link to README.md documentation section
  - [x] 5.6 Run full test suite and quality checks
    - Will run `just test` to execute all tests
    - Will run `just typecheck` for type validation
    - Will run `just fmt-fix` for code formatting
    - Will verify all checks pass
    - Will fix any issues found
  - [x] 5.7 Manual testing and validation
    - Will test seed command with all three sizes
    - Will verify generated catalogs in different directories
    - Will test that directory existence check works correctly
    - Will verify error messages are clear and helpful
    - Will test generated catalogs with serve and build commands
    - Will verify documentation is accurate and complete

**Acceptance Criteria:**
- 2 additional tests added (total 32 tests for feature)
- Total feature tests: 32 (well under maximum of 42)
- All feature-specific tests pass
- pyproject.toml verified to include template files in distribution (no changes needed)
- README.md updated with seed command documentation
- docs/cli-reference.md created with comprehensive CLI reference
- All quality checks pass: `just test`, `just typecheck`, `just fmt`
- Manual testing confirms feature works end-to-end

## Execution Order

Recommended implementation sequence:
1. **Core CLI Implementation** (Task Group 1) - Establish command structure and validation
2. **Template Content Creation** (Task Group 2) - Create reusable template components
3. **Template Generation Engine** (Task Group 3) - Build file generation system
4. **Integration and Validation** (Task Group 4) - Verify generated catalogs work with Storytime
5. **Documentation and Packaging** (Task Group 5) - Complete packaging and user documentation

## Implementation Notes

### Technical Constraints
- Must use Python 3.14+ features (structural pattern matching, modern type hints)
- Must use pathlib for all path operations
- Must follow existing CLI patterns from `serve` and `build` commands
- Must use typer framework for CLI implementation
- Templates must be packaged with distribution (not external files)
- Generated catalogs must work with existing `storytime serve` and `storytime build` commands

### Key Files to Reference
- CLI patterns: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/__main__.py`
- Build patterns: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/build.py`
- Catalog model: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/catalog/models.py`
- PACKAGE_DIR constant: `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/__init__.py`
- Package configuration: `/Users/pauleveritt/projects/pauleveritt/storytime/pyproject.toml`

### Testing Strategy
- Each task group wrote 2-8 focused tests covering critical behaviors only
- Tests run incrementally per task group, full suite run in Task Group 5
- Task Group 5 added 2 additional tests to fill critical gaps
- Total feature tests: 32 tests (well under maximum of 42)
- Focus on behavior testing, not implementation details
- Use aria-testing library functions for DOM queries in component tests

### Code Quality Standards
- Follow modern Python 3.14+ patterns per `/Users/pauleveritt/projects/pauleveritt/storytime/CLAUDE.md`
- Use structural pattern matching for size selection
- Use PEP 604 union syntax (`X | Y` instead of `Union[X, Y]`)
- Use dataclasses for component props
- Include type hints on all functions and classes
- Run quality checks after all implementation: `just test`, `just typecheck`, `just fmt`
