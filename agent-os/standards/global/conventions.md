# Development Conventions

This document outlines the development conventions and best practices for the Storyville project.

## Project Structure Conventions

- Predictable project structure
- Up-to-date README with setup/architecture
- Clear commit messages and PR descriptions
- Environment variables for config (no secrets in repo)
- Minimal, documented dependencies
- Code review before merge
- Feature flags over long-lived branches

## Quality Check Sequence

All quality checks must pass before committing code. The checks should be run in the following order:

1. **Lint** - Check code for style and potential issues
2. **Format** - Auto-format code to maintain consistent style
3. **Type Check** - Verify type annotations and type safety
4. **Test** - Run the test suite to ensure correctness

### Running Quality Checks

**Preferred method (using Just):**
```bash
# Run all checks in sequence with fail-fast behavior
just ci-checks

# Or run individual checks
just lint
just fmt
just typecheck
just test-parallel
```

**Alternative method (without Just):**
```bash
# Manual sequence (stop if any command fails)
uv sync --all-groups && \
uv run ruff check . && \
uv run ruff format . && \
uv run ty check && \
uv run pytest -n auto
```

**Important:** All checks must pass before creating commits or pull requests. The `just ci-checks` recipe uses `&&` to chain commands, ensuring fail-fast behavior - it stops at the first failure.

## Caching Strategy

The project implements two-layer caching to speed up CI/CD builds:

### Layer 1: Virtual Environment Cache

- **What:** The `.venv` directory containing installed packages
- **Key:** Hash of `uv.lock` file (`venv-${{ runner.os }}-${{ hashFiles('uv.lock') }}`)
- **Invalidation:** Automatic when dependencies change in `uv.lock`
- **Speed improvement:** 30-60 seconds per CI run
- **Implementation:** `actions/cache@v4` in composite action

### Layer 2: uv Package Cache

- **What:** uv's internal package cache (downloaded wheels, etc.)
- **Key:** Managed automatically by `astral-sh/setup-uv@v7`
- **Configuration:** `enable-cache: true` in composite action
- **Benefit:** Faster package downloads across runs

### How It Works

1. On CI run start, restore `.venv` cache if `uv.lock` hasn't changed
2. If cache hit, skip dependency installation (already in `.venv`)
3. If cache miss, install dependencies and save `.venv` for next run
4. uv cache layer speeds up downloads when cache miss occurs

This two-layer approach provides:
- Fast builds when dependencies unchanged (cache hit on `.venv`)
- Faster installations when dependencies changed (cache hit on uv packages)
- Reliable cache invalidation tied to lockfile

## Composite Action Pattern

The project uses GitHub Actions composite actions for workflow reusability and consistency.

### Benefits

- **Centralized setup:** All workflows use the same setup steps
- **Maintainability:** Update setup logic in one place
- **Consistency:** Eliminates duplication and drift across workflows
- **Efficiency:** Shared caching logic across all workflows

### Implementation

**Location:** `.github/actions/setup-python-uv/action.yml`

**Usage in workflows:**
```yaml
- name: Set up Python and uv with caching
  uses: ./.github/actions/setup-python-uv
```

**Workflows using composite action:**
- `ci.yml` - Continuous integration testing
- `pages.yml` - Documentation deployment
- `pypi.yml` - Package publishing

### What the Composite Action Does

1. Restores `.venv` cache (keyed to `uv.lock`)
2. Sets up uv with its own caching enabled
3. Installs Python 3.14
4. Syncs dependencies using `uv sync --all-groups`
5. Saves `.venv` cache for subsequent runs

## Local CI Testing

Before pushing changes, you can test GitHub Actions workflows locally using the `act` tool.

### Installation

**macOS:**
```bash
brew install act
```

**Other platforms:** See [act documentation](https://github.com/nektos/act)

### Usage

```bash
# Run specific workflow job
act -j ci_tests --rm

# Run all workflows
act --rm

# Run with specific event
act push --rm
```

### Known Limitations

- **Caching behavior:** May differ from actual GitHub Actions
- **GitHub-specific features:** Some API calls or context may not work
- **Secrets:** Require additional configuration
- **Docker requirement:** Docker must be running on your system
- **Resource usage:** May be slower than GitHub's hosted runners

### Best Practices

1. Test workflows locally before pushing to reduce CI failures
2. Use `--rm` flag to clean up containers after run
3. Don't rely solely on local testing - GitHub Actions environment differs
4. Use local testing for quick validation, not as replacement for real CI

## Development Workflow Summary

### Daily Development

1. Make code changes
2. Run `just fmt` to format code
3. Run `just lint` to check for issues
4. Run `just typecheck` to verify types
5. Run `just test` to run tests
6. Optional: Run `just ci-checks` to run all checks at once

### Before Committing

1. Ensure all quality checks pass: `just ci-checks`
2. Review your changes: `git diff`
3. Write a clear commit message
4. Commit changes: `git commit -m "description"`

### Before Pushing

1. Optional: Test workflows locally with `act -j ci_tests --rm`
2. Push to feature branch: `git push`
3. Monitor CI workflow execution on GitHub
4. Address any CI failures promptly

### Code Review

1. Ensure CI passes before requesting review
2. Respond to review feedback promptly
3. Re-run quality checks after making changes
4. Squash commits if needed for cleaner history

## Fail-Fast Philosophy

The project follows a fail-fast approach to provide quick feedback:

- **Just recipes:** Use `&&` to chain commands (stop on first failure)
- **CI workflows:** Use `continue-on-error: false` for all quality check steps
- **Testing:** Parallel execution with pytest-xdist for speed, but stops on failures
- **Benefits:**
  - Faster feedback when something breaks
  - Clear indication of what failed first
  - Saves time by not running subsequent checks when earlier ones fail

## Version Control Conventions

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in imperative mood (Add, Fix, Update, Remove)
- Keep first line under 72 characters
- Add detailed description if needed (blank line, then details)

### Branch Naming

- Use descriptive branch names
- Prefix with type: `feature/`, `fix/`, `docs/`, `refactor/`
- Use kebab-case: `feature/add-new-component`
- Keep branch names concise but descriptive

### Pull Requests

- Reference related issues in PR description
- Provide clear description of changes and motivation
- Ensure all CI checks pass before requesting review
- Keep PRs focused and reasonably sized
- Update documentation as needed

## Python-Specific Conventions

### Modern Python 3.14+ Features

Use modern Python syntax and features:

- **Type statement:** `type Vector = list[float]`
- **PEP 604 unions:** `X | Y` instead of `Union[X, Y]`
- **Pattern matching:** Use `match`/`case` for complex conditionals
- **Generic syntax:** `def func[T](x: T) -> T:`
- **Built-in generics:** `list[str]` instead of `List[str]`

### Type Hints

- Add type hints to all function signatures
- Use modern union syntax: `str | None` not `Optional[str]`
- Use type aliases for complex types
- Run `just typecheck` before committing

### Testing

- Test both happy path and edge cases
- Use descriptive test names: `test_<functionality>_<scenario>`
- Place tests in `tests/` directory
- Run tests in parallel: `just test-parallel`
- Ensure all tests pass before committing

## Code Style

- Follow PEP 8 guidelines (enforced by ruff)
- Use 4 spaces for indentation
- Maximum line length: 88 characters (ruff default)
- Use `ruff format` for automatic formatting
- Use `ruff check` for linting

## Documentation

- Keep README.md up to date
- Document new features in appropriate docs/ files
- Update CHANGELOG when making notable changes
- Write docstrings for public APIs
- Use clear, concise language
