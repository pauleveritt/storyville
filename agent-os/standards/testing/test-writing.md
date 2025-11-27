# Test Writing

- Minimal tests during development (complete feature first)
- Test core user flows only
- Defer edge cases unless business-critical
- Test behavior, not implementation
- Descriptive test names
- Mock external dependencies
- Fast execution (milliseconds)

## Use aria-testing Query Functions

Always use `aria-testing` library functions instead of writing custom helper functions for DOM queries and text extraction.

### Available Functions

**Query Functions:**
- `get_by_tag_name()` - Get single element by tag name (throws if not found)
- `query_by_tag_name()` - Query single element by tag name (returns None if not found)
- `query_all_by_tag_name()` - Query all elements by tag name
- `get_by_text()`, `get_by_role()`, `get_by_class()` - Semantic queries
- `get_text_content()` - Extract text content from an element

**Utility Functions:**
- `get_all_elements()` - Extract all Element nodes from a container (handles Fragment)
- `normalize_text()` - Normalize whitespace in text

### ✓ Correct Usage

```python
from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name
from aria_testing.utils import get_all_elements
from tdom import Element, Fragment, Node, html

def _get_element(result: Node) -> Element:
    """Extract first Element from result (handles Fragment wrapper)."""
    elements = get_all_elements(result)
    if not elements:
        raise ValueError("No Element found in result")
    return elements[0]

def test_layout_header_contains_links() -> None:
    layout = Layout(...)
    result = layout()
    element = _get_element(result)

    header = get_by_tag_name(element, "header")
    links = query_all_by_tag_name(header, "a")
    link_texts = [get_text_content(link) for link in links]

    assert "Home" in link_texts
```

### ✗ Incorrect Usage

```python
# DON'T write custom text extraction functions
def _extract_text(node: Node) -> str:
    """Recursively extract text from a tdom node."""
    if isinstance(node, Text):
        return node.text
    if isinstance(node, Element):
        result = ""
        for child in node.children:
            result += _extract_text(child)
        return result
    return ""

# DON'T write custom element extraction functions
def _get_element(result: Node) -> Element:
    """Extract Element from Fragment."""
    if isinstance(result, Fragment):
        for child in result.children:
            if isinstance(child, Element):
                return child
    return result

# USE aria-testing utilities instead!
```

### Benefits

1. **Consistency** - Same API across all tests
2. **Tested** - aria-testing functions are well-tested
3. **Semantic** - Query by role, text, label (accessibility-focused)
4. **Maintained** - Bug fixes and improvements in one place
5. **Less code** - No need to write and maintain custom helpers

## Component Testing Strategy

### Single Test File Per Component

Each component should have **one test file** that covers all testing concerns:
- End-to-end functionality (external API)
- Component composition (if applicable)
- Edge cases and error handling
- Backward compatibility

**✓ Correct:**
```
components/
  layout/
    layout.py
    layout_test.py          # All tests in one file
```

**✗ Incorrect:**
```
components/
  layout/
    layout.py
    layout_test.py          # Unit tests
    layout_integration_test.py  # Integration tests - REDUNDANT
    layout_e2e_test.py      # E2E tests - REDUNDANT
```

### Rationale

**Why consolidate?**
1. **Reduces redundancy** - No duplicate tests for same behavior
2. **Single source of truth** - All component tests in one place
3. **Easier maintenance** - Update tests in one file when component changes
4. **Clear test count** - Easier to see total coverage at a glance
5. **Faster CI** - Fewer test file imports and setup/teardown cycles

**When to split tests:**
Only create separate test files when:
- **Performance tests** need different fixtures or timing constraints (`layout_perf_test.py`)
- **Browser/E2E tests** require Playwright or Selenium setup (`layout_browser_test.py`)
- **Large-scale integration** tests span multiple systems (`system_integration_test.py`)

### Test Organization Within File

Organize tests within the single file using **comment sections**:

```python
"""Tests for Layout component."""

# Basic Structure Tests

def test_layout_renders_html_structure():
    ...

def test_layout_includes_meta_tags():
    ...

# Title Logic Tests

def test_layout_title_concatenates_view_and_site():
    ...

# Component Composition Tests

def test_layout_renders_all_four_components():
    ...

def test_layout_passes_correct_props_to_header():
    ...

# Edge Cases

def test_layout_handles_none_children():
    ...
```

### Testing Refactored Components

When refactoring a component (e.g., extracting sub-components):

**Before refactoring:**
- Component has `component_test.py` with existing tests

**During refactoring:**
1. Keep existing tests unchanged (backward compatibility)
2. Add new composition tests to **same file** (no new `_integration_test.py`)
3. Mark sections with comments: `# Component Composition Tests`

**After refactoring:**
- Remove redundant tests that check same behavior
- Keep all unique tests in single consolidated file

**Example:**
```python
# Original tests (backward compatibility)
def test_layout_includes_navigation_bar():
    """Test Layout includes navigation bar."""
    ...

# Component composition tests (new after refactoring)
def test_layout_renders_all_four_components():
    """Test Layout renders header, aside, main, footer."""
    ...

# Note: Both test similar things but from different angles
# After verification, consolidate by removing one
```
