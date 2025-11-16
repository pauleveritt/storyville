# tdom Standards

## t-strings

- t-string means template string which refers to a PEP 750 feature added in
  Python 3.14.
- A "template function" is a Python function that is passed a template object of type `string.templatelib.Template` and
  returns a string that combines the results
- A template is an iterable of "parts" which are either string or `string.templatelib.Interpolation`
- `string.templatelib.Interpolation` represents the dynamic parts in a template instance
- Use structural pattern matching, as shown in the PEP examples, when analyzing
  the parts.
- Always use type hints on the function arguments and return values.

## tdom

- Look in `/Users/pauleveritt/projects/t-strings/tdom/examples/components` for examples of `tdom` component style
- Components go in the `components` directory with the snake case component name as the filename.
- Component function signatures always start with `*` to force named arguments
- Component tests go in the same directory, with a filename for the component name suffixed with `_test.py`
- Component tests should use a t-string to generate a result. Then create a `soup` variable that calls `str()` on the
  result and uses BeautifulSoup with the `html.parser` option.
- Make a `pytest` assertion on the `soup` value

## Supported environments

- Python: 3.14 only (see requires-python in pyproject.toml).

## Documentation

- User-facing behavior must be reflected in docs/ and README.md.
- Short how-to examples go in docs/examples and are linked from docs/index.md
  toctree.
- Keep docs buildable offline: avoid external fetches during sphinx-build. Use
  myst markdown.
