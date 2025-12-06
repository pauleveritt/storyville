# Claude Code Rules

## Python Standards

Use modern Python standards (Python 3.14+) including:

- **Structural pattern matching**: Use `match`/`case` statements for complex conditionals
- **Type statement**: Use `type` statement for type aliases (e.g., `type Vector = list[float]`)
- **Modern type hints**: Use PEP 604 union syntax (`X | Y` instead of `Union[X, Y]`), built-in generics (`list[str]`
  instead of `List[str]`)
- **PEP 695 syntax**: Use `def func[T](x: T) -> T:` for generic functions
- **Exception groups**: Use `except*` for handling exception groups when appropriate

## Using Context7 for Documentation

Always use context7 when generating code, providing setup/configuration steps, or needing library/API documentation. This means:

- Automatically use the Context7 MCP tools (`mcp__context7__resolve-library-id` and `mcp__context7__get-library-docs`) without waiting for explicit requests
- Use context7 when working with any third-party libraries or frameworks
- Consult up-to-date documentation before suggesting code patterns or API usage
- Verify current best practices and API signatures from official documentation

## Quality Checks

After each prompt, run these commands to ensure code quality:

- Tests: `just test`
- Type checking: `just typecheck`
- Formatting: `just fmt`

All checks must pass before considering the task complete.

## Testing Guidelines

### Test Structure

- Place tests in `tests/` directory
- Use descriptive function names: `test_<functionality>_<scenario>`
- Organize test module names to match the module being tested
- Test both the happy path and edge cases
- Use `tests/conftest.py` and fixtures as appropriate (but only when useful)

### Required Test Coverage

When adding new features, ensure tests cover:

1. **Type handling**: Test with `str`, `Node`, `Markup`, and other types
2. **Safety**: Verify escaping of dangerous content
3. **Combination**: Test safe + unsafe and safe + safe combinations
4. **Edge cases**: Empty content, None, complex structures
5. **Integration**: Test with tdom t-strings
