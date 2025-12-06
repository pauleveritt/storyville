# Development Best Practices

## Python version

- Use Python 3.14 or higher
- Prefer features available in the latest Python 

## Packaging

- Source code in `src/` for proper packaging
- Use `uv` and `pyproject.toml` for managing dependencies
- Use `uv add <package>` to add dependencies
- Use `uv remove <package>` to remove dependencies
- UV manages `pyproject.toml` automatically
- **Never** mix with pip/poetry unless explicitly needed


## Quality Checks

Run quality checks frequently during development:

- Individual checks: `just lint`, `just fmt`, `just typecheck`, `just test`
- Full CI suite: `just ci-checks` (runs all checks with fail-fast)
- Parallel tests: `just test-parallel` (faster feedback)

**Before marking any task complete, run `just ci-checks` and ensure it passes.**

## Import Best Practices

- Use absolute imports from package root
- Avoid circular dependencies
- Group imports: stdlib → third-party → local

## Documentation

Maintain these key files:

- `README.md`: Project overview, setup instructions
- `pyproject.toml`: Dependencies, metadata, tool configs
- Inline docstrings: Use modern format with type hints


## Anti-Patterns to Avoid

❌ Mixing package managers (stick to uv)
❌ Relative imports beyond local modules
❌ Missing `__init__.py` in packages
❌ Ignoring type hints
❌ Skipping quality checks
❌ Using deprecated Python features (Union, List, etc.)
