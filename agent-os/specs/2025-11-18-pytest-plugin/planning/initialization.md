# Spec Initialization: pytest Plugin for Story Assertions

## User's Initial Description

"pytest plugin. Write a plugin that does test discovery on stories with assertions.

I also want some control in a config settings. Would be great if you didn't have to write any tests manually. Make the DX great: good names for tests, good reporting on failures. Decide if making a tree is necessary."

## Project Context

### Current State
- Just completed: Story Assertions feature on `story-assertions` branch
- Stories now support `assertions` field (list of callables)
- Assertions execute during StoryView rendering
- Results stored in `assertion_results` on Story instances
- CLI flag: `--with-assertions` (defaults enabled)

### Relevant Files
- `/src/storytime/story/models.py` - Story model with assertions field
  - `AssertionCallable = Callable[[Element | Fragment], None]`
  - `AssertionResult = tuple[str, bool, str | None]`
  - Stories have `assertions` and `assertion_results` fields
- `/tests/` - Existing test directory structure
- `pyproject.toml` - Project configuration with pytest settings

### Dependencies Available
- pytest 9.0.0+
- aria-testing (dev dependency)
- Python 3.14+
- Modern type hints and pattern matching

### Product Mission Alignment
- Supports "Stories as Tests, Tests as Stories" differentiator
- Addresses roadmap item #5: "Story-to-Test Integration"
- Enables fast component testing without framework overhead
- Improves developer experience with automated test generation

## Spec Path
`/Users/pauleveritt/projects/pauleveritt/storytime/agent-os/specs/2025-11-18-pytest-plugin`
