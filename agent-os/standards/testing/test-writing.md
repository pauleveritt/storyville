# Test Writing

- Minimal tests during development (complete feature first)
- Test core user flows only
- Defer edge cases unless business-critical
- Test behavior, not implementation
- Descriptive test names
- Mock external dependencies
- Fast execution (milliseconds)

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
