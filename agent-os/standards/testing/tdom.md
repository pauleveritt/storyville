# tdom Standards

## t-strings

- Template strings from PEP 750 (Python 3.14)
- Template function accepts `string.templatelib.Template`
- Parts are string or `string.templatelib.Interpolation`
- Use structural pattern matching
- Always type hint

## tdom

- Components in `components/` with snake_case filenames
- Function signatures start with `*` (force named args)
- Tests suffix `_test.py` in same directory
- Tests use t-string + aria-testing assertions

## Environment

- Python 3.14 only

## Documentation

- User-facing behavior in docs/ and README.md
- Examples in docs/examples
- Offline-buildable (no external fetches, use MyST)
