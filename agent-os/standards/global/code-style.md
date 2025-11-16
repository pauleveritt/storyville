# Code Style

## Python idioms

- Prefer structural pattern matching `match`/`case` statements for complex conditionals
- Use `except*` for handling exception groups when appropriate
- Don't use `from __future__ import annotations` unless you have a string with a generic such as `BaseNode["Subject"]`

## Type hints

- Aggressively use modern Python features for type hinting
- Use `type` statement for type aliases (e.g., `type Vector = list[float]`)
- Use PEP 604 union syntax (`X | Y` instead of `Union[X, Y]`), built-in generics (`list[str]` instead of `List[str]`)
- Use PEP 695 syntax `def func[T](x: T) -> T:` for generic functions
