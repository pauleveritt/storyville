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

# Run tests (sequential)
test *ARGS:
    uv run pytest {{ ARGS }}

# Run tests (sequential)
test-parallel *ARGS:
    uv run pytest -n auto {{ ARGS }}

# Run only slow tests in parallel
test-slow:
    uv run pytest -m slow -n auto -v

# Format (no changes)
fmt:
    uv run ruff check .

# Format and auto-fix
fmt-fix:
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

# Run the same checks as CI
ci:
    just install
    just fmt
    just typecheck
    just test-parallel
