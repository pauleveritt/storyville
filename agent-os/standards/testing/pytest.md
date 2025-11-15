# Testing Standards

## Test Structure

- Place tests in `tests/` directory
- Use descriptive function names: `test_<functionality>_<scenario>`
- Organize test module names to match the module being tested
- Test both the happy path and edge cases
- Use `tests/conftest.py` and fixtures as appropriate (but only when useful)

## Coverage

When adding new features, ensure tests cover:

1. **Type handling**: Test with `str`, `Node`, `Markup`, and other types
2. **Safety**: Verify escaping of dangerous content
3. **Combination**: Test safe + unsafe and safe + safe combinations
4. **Edge cases**: Empty content, None, complex structures
5. **Integration**: Test with tdom t-strings
