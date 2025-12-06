# Tech Stack

This document defines the technical stack for Storyville. All team members should reference this to maintain consistency across the project.

## Framework & Runtime

- **Language/Runtime:** Python 3.14+ (3.14-only, no version matrix testing)
  - Modern syntax: type statement, PEP 604 unions, structural pattern matching
  - Subinterpreter support for hot reload functionality
  - Required minimum: `>=3.14` (specified in pyproject.toml)

- **Package Manager:** uv 1.x
  - Fast, reliable dependency resolution
  - Workspace-aware dependency groups
  - Integrated with build system via `uv_build`
  - Cache-enabled for faster CI/CD builds

- **Task Runner:** Just 1.x (preferred)
  - Simple, consistent command interface
  - Recipe-based task definitions in `Justfile`
  - Alternative: Direct `uv run` commands (documented for accessibility)
  - All recipes use `uv run` prefix for isolation

## Application Framework

- **Web Framework:** Starlette 0.50.0+
  - Async-first ASGI framework
  - Used for dev server and catalog browsing
  - Lightweight, modern request/response handling

- **Templating:** tdom
  - t-string based HTML generation
  - Type-safe component composition
  - Native Python syntax for templates

- **File Watching:** watchfiles 1.1.1+
  - Fast, efficient file change detection
  - Powers hot reload functionality
  - Cross-platform compatibility

- **Server:** uvicorn[standard] 0.38.0+
  - ASGI server for Starlette applications
  - Standard extras include performance optimizations

## Frontend

- **CSS Framework:** PicoCSS
  - Semantic, classless CSS framework
  - Minimal, clean UI without custom classes
  - Used for catalog browser interface

- **JavaScript:** Vanilla JavaScript
  - No framework dependencies
  - Minimal client-side scripting
  - Progressive enhancement approach

## Testing & Quality

- **Test Framework:** pytest 9.0.0+
  - Modern testing framework with plugin support
  - Story assertion integration via pytest plugin
  - Parallel execution via pytest-xdist 3.8.0+

- **Linting:** ruff 0.14.4+
  - Fast Python linter (replaces Flake8, isort, etc.)
  - Command: `uv run ruff check .`
  - Configuration in pyproject.toml

- **Formatting:** ruff 0.14.4+
  - Unified formatting (replaces Black)
  - Command: `uv run ruff format .`
  - Consistent style across codebase

- **Type Checking:** ty/basedpyright 0.0.1a25+
  - Type checker for Python (Pyright fork)
  - Command: `uv run ty check`
  - Enforces type safety and modern type hints

- **Additional Test Tools:**
  - pytest-xdist 3.8.0+ (parallel test execution)
  - pytest-benchmark 4.0.0+ (performance testing)
  - pytest-playwright 0.3.0+ (browser testing)
  - httpx 0.28.1+ (async HTTP testing)
  - coverage 7.11.2+ (code coverage analysis)

## Documentation

- **Documentation Generator:** Sphinx 7.0.0+
  - Python documentation standard
  - Builds from docs/ directory
  - Command: `uv run sphinx-build -b html docs docs/_build/html`

- **Documentation Format:** MyST-Parser 2.0.0+
  - Markdown support for Sphinx
  - Enables Markdown-based documentation

- **Theme:** sphinx-rtd-theme 2.0.0+
  - Read the Docs theme for Sphinx
  - Clean, responsive documentation interface

## Deployment & Infrastructure

- **CI/CD:** GitHub Actions
  - Automated testing on push/PR
  - Composite action pattern for reusability
  - Workflows: ci.yml, pages.yml, pypi.yml

- **Composite Action Pattern:**
  - Centralized setup in `.github/actions/setup-python-uv/`
  - Reusable across all workflows
  - Includes caching for `.venv` and uv cache
  - Maintains consistency and reduces duplication

- **Caching Strategy:**
  - `.venv` directory cached with `uv.lock` hash
  - uv package cache via `setup-uv@v7` with `enable-cache: true`
  - Significantly speeds up CI builds (30-60 second improvement)

- **Build System:** uv_build 0.8.17+
  - Modern build backend for Python packages
  - Integrated with uv for seamless builds
  - Configuration in pyproject.toml

- **Local Testing:** act
  - Local GitHub Actions workflow testing
  - Installation: `brew install act` (macOS)
  - Usage: `act -j ci_tests --rm`
  - Note: Some limitations vs. real GitHub Actions

## CLI & Tooling

- **CLI Framework:** Typer 0.20.0+
  - Type-hinted CLI framework
  - Powers `storyville` command-line tool
  - Commands: serve, build, seed

- **CLI Utilities:** Click 8.3.0+
  - Underlying framework for Typer
  - Terminal formatting and interaction

## Development Workflow

### Preferred Method: Just Recipes

Just recipes are the recommended approach for all development tasks:

```bash
just install      # Install dependencies
just lint         # Check code
just fmt          # Format code
just typecheck    # Type check
just test         # Run tests
just ci-checks    # Run all quality checks
```

### Alternative Method: Direct Commands

For contributors without Just installed:

```bash
uv sync --all-groups     # Install dependencies
uv run ruff check .      # Lint code
uv run ruff format .     # Format code
uv run ty check          # Type check
uv run pytest            # Run tests (sequential)
uv run pytest -n auto    # Run tests (parallel)
```

### Quality Check Sequence

All quality checks must pass before committing:

1. **Lint** - Check code for issues: `just lint`
2. **Format** - Auto-format code: `just fmt`
3. **Type Check** - Verify types: `just typecheck`
4. **Test** - Run test suite: `just test` or `just test-parallel`

Run all at once: `just ci-checks`

## Version Requirements Summary

| Tool            | Version Requirement | Purpose                    |
|-----------------|---------------------|----------------------------|
| Python          | >=3.14              | Runtime environment        |
| uv              | 1.x                 | Package management         |
| Just            | 1.x                 | Task runner (preferred)    |
| Starlette       | >=0.50.0            | Web framework              |
| uvicorn         | >=0.38.0            | ASGI server                |
| watchfiles      | >=1.1.1             | File watching              |
| pytest          | >=9.0.0             | Testing framework          |
| ruff            | >=0.14.4            | Linting and formatting     |
| ty/basedpyright | >=0.0.1a25          | Type checking              |
| pytest-xdist    | >=3.8.0             | Parallel testing           |
| Sphinx          | >=7.0.0             | Documentation              |
| Typer           | >=0.20.0            | CLI framework              |

## Third-Party Services

This project does not currently use external third-party services for:
- Authentication
- Email delivery
- Monitoring/observability
- Cloud hosting (static site generation only)

All functionality is self-contained within the package.
