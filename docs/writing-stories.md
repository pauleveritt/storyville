# Writing Stories

Stories are the heart of Storytime. Each story represents one variation of a component with specific props and optional assertions for testing.

## Story Structure

### Basic Story

```python
from storytime import Story, Subject

def this_subject() -> Subject:
    return Subject(
        title="Button Component",
        target=Button,  # The component to render
        items=[
            Story(props=dict(text="Click Me", variant="primary")),
        ],
    )
```

### Story with All Fields

```python
Story(
    title="Primary Action Button",
    description="The main call-to-action button",
    props=dict(text="Get Started", variant="primary", disabled=False),
    template=custom_template,  # Optional custom rendering template
    assertions=[
        lambda el: None if "button" in str(el).lower()
        else (_ for _ in ()).throw(AssertionError("Should be a button tag")),
    ],
)
```

## Story Fields

### Required Fields

None! Stories can be as minimal as `Story(props=dict())`.

### Optional Fields

- **`props`** (dict): Component props (default: empty dict)
- **`title`** (str): Story display title (auto-generated if not provided)
- **`description`** (str): Longer description of the story  
- **`target`** (callable): Component to render (inherits from Subject if not specified)
- **`template`** (callable): Custom template for rendering (uses default StoryView if not specified)
- **`assertions`** (list): List of assertion callables for testing

## Story Assertions

Assertions let you define tests directly on stories. They execute during rendering (with badges in the browser) and generate pytest tests automatically.

### Writing Assertions

Assertions are callables that receive the rendered element and raise `AssertionError` on failure:

```python
Story(
    props=dict(text="Submit", variant="primary"),
    assertions=[
        # Check element exists
        lambda el: None if el is not None
        else (_ for _ in ()).throw(AssertionError("Element required")),
        
        # Check content
        lambda el: None if "Submit" in str(el)
        else (_ for _ in ()).throw(AssertionError("Text should appear")),
        
        # Check attributes
        lambda el: None if "primary" in str(el)
        else (_ for _ in ()).throw(AssertionError("Should have primary class")),
    ],
)
```

### Assertion Types

**Simple Assertions:**
```python
lambda el: None if el is not None
else (_ for _ in ()).throw(AssertionError("Should exist"))
```

**Using aria-testing:**
```python
from aria_testing import get_by_role, get_text_content

lambda el: None if get_text_content(get_by_role(el, "button")) == "Click"
else (_ for _ in ()).throw(AssertionError("Button text mismatch"))
```

**Complex Assertions:**
```python
def check_button_structure(el):
    """Verify button has correct structure."""
    button = get_by_tag_name(el, "button")
    if not button:
        raise AssertionError("No button found")
    if "class" not in button.attrs:
        raise AssertionError("Button missing class")
    return None

# Use in story
Story(props={...}, assertions=[check_button_structure])
```

### Assertion Benefits

1. **Visual Feedback**: Pass/fail badges appear in the browser
2. **Auto Tests**: pytest plugin generates tests automatically
3. **Documentation**: Assertions document expected behavior
4. **TDD**: Write assertions first, implement component after

## Subject Structure

Subjects group related stories for a single component:

```python
def this_subject() -> Subject:
    return Subject(
        title="Button Component",
        description="Reusable button with multiple variants",
        target=Button,  # All stories inherit this target
        items=[
            Story(props=dict(variant="primary")),
            Story(props=dict(variant="secondary")),
            Story(props=dict(variant="danger")),
        ],
    )
```

### Subject Fields

- **`title`** (str): Display title (auto-generated from package path if not provided)
- **`description`** (str): Optional description
- **`target`** (callable): Component that stories will render
- **`items`** (list[Story]): List of Story instances

## Sections (Optional)

Sections group related subjects:

```python
# my_project/components/__init__.py
from storytime import Section
from my_project.components.button.stories import this_subject as button_subject
from my_project.components.card.stories import this_subject as card_subject

def this_section() -> Section:
    return Section(
        title="UI Components",
        description="Core user interface components",
        items={
            "button": button_subject(),
            "card": card_subject(),
        },
    )
```

## Catalog Structure

The complete hierarchy:

```
Catalog (auto-discovered from package)
  └─ Section (optional, from __init__.py)
      └─ Subject (from stories.py)
          └─ Story (items in Subject)
```

**Auto-discovery:**
- Storytime scans for `stories.py` files
- Each `stories.py` must have `this_subject()` function
- Optional `__init__.py` with `this_section()` for grouping

## Story Templates

Custom templates give you full control over story rendering:

```python
from tdom import html as h

def custom_story_template(story, catalog):
    """Custom template for story rendering."""
    return h.div(
        h.h1("Custom Story View"),
        h.div(story.instance, class_="story-content"),
        class_="custom-template",
    )

Story(
    props=dict(text="Hello"),
    template=custom_story_template,
)
```

## Best Practices

### 1. One Component Per Subject

```python
# Good: One subject per component
def this_subject() -> Subject:
    return Subject(
        title="Button",
        target=Button,
        items=[...],
    )
```

### 2. Descriptive Story Titles

```python
# Good: Clear, descriptive titles
Story(
    title="Primary Action Button",
    props=dict(variant="primary", text="Submit"),
)

# Avoid: Generic titles
Story(title="Story 1", props={...})
```

### 3. Meaningful Assertions

```python
# Good: Clear error messages
lambda el: None if "button" in str(el).lower()
else (_ for _ in ()).throw(AssertionError("Should render as button element"))

# Avoid: Vague messages
lambda el: None if "button" in str(el).lower()
else (_ for _ in ()).throw(AssertionError("Failed"))
```

### 4. Group Related Stories

```python
# Good: Multiple variations of same component
Subject(
    target=Button,
    items=[
        Story(title="Primary", props=dict(variant="primary")),
        Story(title="Secondary", props=dict(variant="secondary")),
        Story(title="Disabled", props=dict(disabled=True)),
    ],
)
```

## Examples

See the complete examples in the repository:
- `examples/minimal` - Simplest possible story
- `examples/complete` - All story fields demonstrated
- `examples/huge_assertions` - Performance testing with many assertions

## Next Steps

- [pytest Plugin](pytest-plugin.md) - Automatic test generation from assertions
- [API Reference](api-reference.md) - Complete API documentation
