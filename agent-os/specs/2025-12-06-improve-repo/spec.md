# Specification: Repository Development Infrastructure Improvements

## Goal

Modernize and standardize the repository's development infrastructure by enhancing the GitHub Actions composite action
with better caching, reorganizing Just recipes for clarity, and documenting alternative workflows for developers without Just installed.

## User Stories

- As a developer, I want faster CI builds through improved caching so that I can iterate more quickly
- As a contributor without Just, I want clear documentation of alternative commands so that I can work on the project
  without additional tooling

## Specific Requirements

**Justfile Recipe Reorganization**

- Rename current `fmt` recipe to `lint` (keeps `uv run ruff check .` behavior)
- Create new `fmt` recipe that runs `uv run ruff format .` for code formatting
- Add `setup` recipe as an alias to the existing `install` recipe for better discoverability
- Add `ci-checks` recipe that chains: `install`, `lint`, `typecheck`, and `test-parallel` using `&&` for fail-fast
  behavior
- Update existing `ci` recipe to call `ci-checks` or consolidate the logic
- Ensure all recipes maintain the existing pattern of using `uv run` for command execution

**Composite Action Enhancement**

- Add caching for the `.venv` directory using `actions/cache@v4` to speed up dependency installation
- Generate cache key using hash of `uv.lock` file to invalidate cache when dependencies change
- Keep existing setup-uv@v7 with `enable-cache: true` for uv's own cache
- Ensure cache restore and save steps properly handle the `.venv` directory location

**Documentation of Non-Just Alternatives**

- Add a "Development" section to README.md (after the "Contributing" section) documenting direct command alternatives
- Document the mapping: `just install` -> `uv sync --all-groups`, `just test` -> `uv run pytest`, etc.
- Include a table showing Just recipes in one column and equivalent direct commands in the other
- Clearly state that Just recipes are the preferred approach but alternatives are provided for flexibility
- Document that `act` tool can be used for local workflow testing: `brew install act` and basic usage

**Tech Stack Standards Update**

- Update `agent-os/standards/global/tech-stack.md` to replace placeholder content with actual project stack
- Document: Python 3.14 runtime (no version matrix, 3.14-only), uv (1.x) package manager, Just (1.x) task runner
- Document: ruff (0.14.4+) for linting/formatting, pytest (9.0+) for testing, ty/basedpyright for type checking
- Document: GitHub Actions for CI/CD, composite action pattern for workflow reusability
- Include version requirements or ranges for each tool
- Add note that Just recipes are preferred but document `uv run` direct commands as alternatives

**Development Conventions Update**

- Update `agent-os/standards/global/conventions.md` with specific development workflow standards
- Document the quality check sequence: lint, format, type check, test (using `just ci-checks` or individual steps)
- Document caching strategy: `.venv` directory cached with dependency hash, uv cache via setup-uv
- Document composite action pattern: centralized setup steps for reusability
- Document local testing approach using `act` for workflow validation before pushing

## Visual Design

No visual assets provided for this infrastructure improvement feature.

## Existing Code to Leverage

**Composite Action Foundation**

- File: `.github/actions/setup-python-uv/action.yml` already exists and is functional
- Currently sets up uv with caching enabled and installs Python and dependencies
- Used by all three workflows (ci.yml, pages.yml, pypi.yml) consistently
- Needs enhancement with version parameter and venv caching, but core structure is solid
- Pattern of composite action for reusability should be maintained and documented as standard

**Justfile Recipe Patterns**

- File: `Justfile` has established patterns for task definitions
- All recipes use `uv run` prefix for command execution (maintain this consistency)
- Uses `*ARGS` pattern for passing through arguments (keep for new recipes)
- Has `default` recipe that lists all available tasks (maintain this discoverability)
- Recipe chaining in `ci` recipe shows precedent for the new `ci-checks` recipe

**Workflow Structure**

- Files: `.github/workflows/ci.yml`, `pages.yml`, `pypi.yml` have consistent structure
- All use the composite action via `./.github/actions/setup-python-uv` pattern
- Use `continue-on-error: false` for quality checks (maintain this fail-fast approach)
- Set `timeout-minutes: 30` for job-level timeouts (keep this safety measure)
- `ci.yml` runs comprehensive checks (lint, format check, type check, test) - use as model for matrix testing

**README Development Section**

- File: `README.md` already has a "Contributing" section with development setup instructions
- Shows pattern of documenting tools in table format (Tool | Purpose columns)
- Documents existing Just recipes: `just test`, `just typecheck`, `just fmt`
- New "Development" section should follow similar formatting and placement
- Currently only shows Just commands, needs augmentation with direct alternatives

**Standards File Templates**

- Files: `agent-os/standards/global/tech-stack.md` and `conventions.md` have established structure
- `tech-stack.md` uses categorized sections (Framework & Runtime, Testing & Quality, etc.)
- `conventions.md` uses concise bullet points for principles
- Both need population with actual project-specific content rather than placeholders

## Out of Scope

- Implementing workflow concurrency controls to cancel outdated runs
- Setting up automated dependency updates via Dependabot or Renovate
- Adding workflow artifacts to preserve test reports or build outputs
- Creating pre-commit hooks for local quality checks
- Setting up Docker-based development environment
- Supporting additional CI providers beyond GitHub Actions
- Adding code coverage reporting or coverage badges
- Adding matrix testing for multiple Python versions (project is Python 3.14-only)
- Adding Python version parameters or version management to workflows
- Changing the existing test framework or adding new testing tools
- Updating documentation beyond README and standards files (no changes to docs/ folder)
