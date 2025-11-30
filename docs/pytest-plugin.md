# pytest Plugin

Storytime includes a built-in pytest plugin that automatically generates tests from story assertions. Zero manual test writing required!

## Features

- **Automatic test discovery** - Finds all stories with assertions
- **Zero boilerplate** - One test per assertion, automatically generated
- **Clear naming** - `test_story[catalog.section.subject.story::assertion]`
- **Rich failure reporting** - Story metadata, rendered HTML, and diffs
- **Parallel execution** - Works with `pytest -n auto` (pytest-xdist)
- **Fresh rendering** - Each test gets a fresh component instance

## Configuration

### Enable the Plugin

Add to `pyproject.toml`:

```toml
[project.entry-points.pytest11]
storytime = "storytime.pytest_plugin"

[tool.pytest.ini_options]
testpaths = ["tests", "examples/"]

[tool.storytime.pytest]
enabled = true  # Optional: enable/disable plugin (default: true)
```

**Key points:**
- Add paths containing `stories.py` files to pytest's `testpaths`
- Plugin automatically discovers stories in those paths
- Set `enabled = false` to disable if needed

### Disable the Plugin

```toml
[tool.storytime.pytest]
enabled = false
```

Or use pytest's `-p` flag:

```bash
pytest -p no:storytime
```

## Writing Story Assertions

### Basic Assertions

```python
from storytime import Story, Subject

def this_subject() -> Subject:
    return Subject(
        target=Button,
        items=[
            Story(
                props=dict(text="Click Me", variant="primary"),
                assertions=[
                    # Element exists
                    lambda el: None if el is not None
                    else (_ for _ in ()).throw(AssertionError("Element required")),
                    
                    # Check for button tag
                    lambda el: None if "button" in str(el).lower()
                    else (_ for _ in ()).throw(AssertionError("Should be button")),
                    
                    # Verify variant class
                    lambda el: None if "primary" in str(el)
                    else (_ for _ in ()).throw(AssertionError("Should have primary class")),
                ],
            ),
        ],
    )
```

This story generates **3 tests automatically**:
- `test_story[catalog.section.subject.story::Assertion 1]`
- `test_story[catalog.section.subject.story::Assertion 2]`
- `test_story[catalog.section.subject.story::Assertion 3]`

### Using aria-testing

```python
from aria_testing import get_by_role, get_text_content

Story(
    props=dict(text="Submit"),
    assertions=[
        lambda el: None if get_text_content(get_by_role(el, "button")) == "Submit"
        else (_ for _ in ()).throw(AssertionError("Button text mismatch")),
    ],
)
```

### Named Functions

```python
def check_button_accessible(el):
    """Verify button is accessible."""
    button = get_by_role(el, "button")
    if not button:
        raise AssertionError("Button not accessible")
    return None

Story(
    props=dict(text="Click"),
    assertions=[check_button_accessible],
)
```

## Running Tests

### Basic Usage

```bash
# Run all tests (including auto-generated story tests)
pytest

# Run only story tests
pytest examples/

# Run specific example
pytest examples/complete/ -v

# See what tests will run
pytest --collect-only examples/
```

### Parallel Execution

```bash
# Use all CPU cores
pytest examples/ -n auto

# Use specific number of workers
pytest examples/ -n 4
```

### Filtering Tests

```bash
# Run tests matching pattern
pytest -k "button" -v

# Run specific story test
pytest -k "primary_action_button" -v

# Run tests from specific section
pytest examples/ -k "components.button"
```

## Test Output

### Passing Tests

```
examples/complete/stories.py::test_story[complete.button.primary::Assertion 1] PASSED
examples/complete/stories.py::test_story[complete.button.primary::Assertion 2] PASSED
examples/complete/stories.py::test_story[complete.button.primary::Assertion 3] PASSED
```

### Failing Tests

```
FAILED examples/complete/stories.py::test_story[complete.button.primary::Assertion 2]

Story: complete.button.primary
Props: {'text': 'Click Me', 'variant': 'primary'}
Assertion: Assertion 2

AssertionError: Should contain button tag

Rendered HTML:
<button class="primary">Click Me</button>
```

## Test Isolation

Each test:
1. **Renders fresh** - New component instance every time
2. **Isolated state** - No shared state between tests
3. **Parallel safe** - Can run concurrently without conflicts

This ensures tests are:
- **Reliable** - Same results every run
- **Fast** - Can run in parallel
- **Independent** - Tests don't affect each other

## Performance

### Benchmarks

From `examples.huge_assertions` (300 stories, 205 with assertions):
- **328 auto-generated tests** from story assertions
- **6-20% overhead** compared to build without assertions
- **Parallel execution** scales linearly with cores

### Optimization Tips

1. **Use parallel execution**: `pytest -n auto`
2. **Filter by path**: Only run tests you need
3. **Disable when not needed**: `--no-with-assertions` for faster builds

## Integration with pytest

### Works with Standard pytest Features

```bash
# Coverage
pytest --cov=my_project examples/

# Verbose output
pytest examples/ -vv

# Stop on first failure
pytest examples/ -x

# Show local variables on failure
pytest examples/ -l
```

### pytest Markers

```python
# Mark slow tests
@pytest.mark.slow
def test_story[...]:
    ...

# Run with: pytest -m "not slow"
```

### pytest Fixtures

The plugin integrates seamlessly with pytest fixtures, hooks, and plugins.

## Troubleshooting

### Tests Not Discovered

**Check:**
1. Is `stories.py` in a path listed in `testpaths`?
2. Is the plugin enabled in `[tool.storytime.pytest]`?
3. Do stories have non-empty `assertions` list?

```bash
# Debug: See what pytest is collecting
pytest --collect-only -v
```

### Import Errors

**Ensure:**
- Package is importable (`pip install -e .` for development)
- `stories.py` has `this_subject()` function
- Component imports are correct

### Assertion Errors Not Clear

**Improve error messages:**

```python
# Bad: Generic message
def check(el) -> None:
    assert condition, "Failed"

# Good: Specific message with context
def check_is_button_tag(el) -> None:
    """Verify element is a button tag."""
    tag_name = el.tag if hasattr(el, 'tag') else type(el).__name__
    assert "button" in str(el).lower(), f"Expected button tag, got: {tag_name}"
```

## Examples

### Complete Example

```python
from aria_testing import get_by_role, get_text_content
from storytime import Story, Subject

def this_subject() -> Subject:
    return Subject(
        title="Button Component",
        target=Button,
        items=[
            Story(
                title="Primary Action Button",
                props=dict(text="Submit", variant="primary"),
                assertions=[
                    # Accessibility
                    lambda el: None if get_by_role(el, "button")
                    else (_ for _ in ()).throw(AssertionError("Not accessible as button")),
                    
                    # Text content
                    lambda el: None if "Submit" in get_text_content(el)
                    else (_ for _ in ()).throw(AssertionError("Missing button text")),
                    
                    # Variant class
                    lambda el: None if "primary" in str(el)
                    else (_ for _ in ()).throw(AssertionError("Missing primary variant")),
                ],
            ),
        ],
    )
```

### Statistics

From real examples:
- `examples/complete`: 3 stories → 6 tests
- `examples/huge_assertions`: 205 stories → 328 tests

## Best Practices

1. **One assertion per concern**: Separate checks for clarity
2. **Clear error messages**: Make failures easy to diagnose
3. **Test behavior, not implementation**: Focus on user-visible output
4. **Use aria-testing**: Better accessibility and reliability
5. **Keep assertions simple**: Complex logic should be helper functions

## Next Steps

- [Writing Stories](writing-stories.md) - Learn about story structure
- [Hot Reload](hot-reload.md) - Development workflow
- [API Reference](api-reference.md) - Complete API docs
