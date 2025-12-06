# Justfile for aria-testing
# Requires: just, uv, Python 3.14
# All tasks use uv to ensure isolated, reproducible runs.

# Default recipe shows help
default:
    @just --list

# Print environment info
info:
    @echo "Python: $(python --version)"
    @uv --version

# Install project and dev dependencies
install:
    uv sync --all-groups

# Alias for install (better discoverability)
setup: install

# Run tests (sequential)
test *ARGS:
    uv run pytest {{ ARGS }}

# Run tests (parallel)
test-parallel *ARGS:
    uv run pytest -n auto {{ ARGS }}

# Run only slow tests in parallel
test-slow:
    uv run pytest -m slow -n auto -v

# Lint code (check for issues)
lint *ARGS:
    uv run ruff check {{ ARGS }} .

# Format code (auto-format)
fmt *ARGS:
    uv run ruff format {{ ARGS }} .

# Lint and auto-fix
lint-fix:
    uv run ruff check --fix .

# Type checking
typecheck *ARGS:
    uv run ty check {{ ARGS }}

# Build docs
docs:
    uv run sphinx-build -b html docs docs/_build/html

# Build sdist/wheel
build:
    uv build

# Clean build and cache artifacts
clean:
    rm -rf .pytest_cache .ruff_cache .pyright .mypy_cache build dist
    find docs/_build -mindepth 1 -maxdepth 1 -not -name ".gitkeep" -exec rm -rf {} + || true

# Run all quality checks with fail-fast behavior
ci-checks:
    just install && just lint && just typecheck && just test-parallel
