# Tech Stack

## Framework & Runtime

- **Language/Runtime:** Python 3.14+
- **Application Framework:** Starlette (web server for component browser)
- **Templating Engine:** tdom (t-strings based templating)
- **Package Manager:** uv (modern Python package management)
- **Task Runner:** just (command runner for development tasks)

## Core Dependencies

- **Web Server:** Uvicorn (ASGI server for Starlette)
- **File Watching:** watchfiles (hot reload during development)
- **HTTP Client:** httpx (testing web endpoints)

## Testing & Quality

- **Test Framework:** pytest (unit and integration testing)
- **Accessibility Testing:** aria-testing (ARIA validation for components)
- **Coverage:** coverage (test coverage reporting)
- **Type Checking:** ty (static type analysis)
- **Linting/Formatting:** ruff (fast Python linter and formatter)
- **Browser Testing** Playwright with Python bindings for pytest

## Python Standards

- **Type Hints:** PEP 604 union syntax (`X | Y`), built-in generics (`list[str]`)
- **Type Aliases:** Type statement (`type Vector = list[float]`)
- **Generic Functions:** PEP 695 syntax (`def func[T](x: T) -> T`)
- **Pattern Matching:** `match`/`case` statements for complex conditionals
- **Exception Handling:** `except*` for exception groups when appropriate

## Development Tools

- **Version Control:** Git
- **Build System:** uv_build

## Project Structure

- **Source:** `src/storytime/` (main package)
- **Tests:** `tests/` (test suite mirroring source structure)
- **Examples:** `examples/` (demonstration components and stories)
- **Documentation:** `docs/` (project documentation)
- **Config:** `pyproject.toml` (centralized project configuration)

## Key Architecture Decisions

- **Framework Independence:** Core components use tdom, not framework-specific templates
- **Type Safety:** Extensive use of modern Python type hints for better IDE support and refactoring
- **Story-Driven:** Stories are first-class citizens, used for both development and testing
- **Modern Python:** Leverages Python 3.14+ features for cleaner, more expressive code
