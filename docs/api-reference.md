# API Reference

Complete API documentation for Storytime.

## Core Classes

### Story

A single variation of a component with specific props and optional assertions.

```python
@dataclass
class Story:
    target: Target | None = None
    parent: Subject | None = None
    props: dict[str, Any] = field(default_factory=dict)
    title: str | None = None
    description: str | None = None
    template: Template | None = None
    assertions: list[AssertionCallable] = field(default_factory=list)
    assertion_results: list[AssertionResult] = field(default_factory=list)
```

**Fields:**
- `target` - Component callable to render (inherits from Subject if None)
- `parent` - Parent Subject in the tree (set automatically)
- `props` - Dictionary of props to pass to target
- `title` - Display title (auto-generated if None)
- `description` - Optional longer description
- `template` - Custom rendering template (uses StoryView if None)
- `assertions` - List of assertion callables for testing
- `assertion_results` - Cached assertion results (list of tuples)

**Properties:**

```python
@property
def instance(self) -> Node | None:
    """Render the component with props."""
```

Returns the rendered component (Element or Fragment), or None if no target.

**Example:**

```python
from storytime import Story

story = Story(
    title="Primary Button",
    props=dict(text="Click Me", variant="primary"),
    assertions=[
        lambda el: None if el is not None
        else (_ for _ in ()).throw(AssertionError("Element required")),
    ],
)
```

### Subject

Groups related stories for a single component.

```python
@dataclass  
class Subject(TreeNode):
    title: str | None = None
    description: str | None = None
    target: Target | None = None
    items: list[Story] = field(default_factory=list)
```

**Fields:**
- `title` - Display title (auto-generated from package path if None)
- `description` - Optional description
- `target` - Component that stories will render (inherited by stories)
- `items` - List of Story instances

**Example:**

```python
from storytime import Subject, Story

def this_subject() -> Subject:
    return Subject(
        title="Button Component",
        description="Reusable button with variants",
        target=Button,
        items=[
            Story(props=dict(variant="primary")),
            Story(props=dict(variant="secondary")),
        ],
    )
```

### Section

Optional grouping of related subjects.

```python
@dataclass
class Section(TreeNode):
    title: str | None = None
    description: str | None = None
    items: dict[str, Subject] = field(default_factory=dict)
```

**Fields:**
- `title` - Display title
- `description` - Optional description  
- `items` - Dictionary of subject_name → Subject

**Example:**

```python
from storytime import Section

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

### Catalog

Root of the story tree, auto-discovered from package.

```python
@dataclass
class Catalog(TreeNode):
    title: str | None = None
    items: dict[str, Section | Subject] = field(default_factory=dict)
```

**Fields:**
- `title` - Catalog display title
- `items` - Dictionary of section/subject name → Section or Subject

**Created automatically by:**

```python
from storytime import make_catalog

catalog = make_catalog("my_package")
```

## Type Aliases

### AssertionCallable

Callable that checks a rendered element:

```python
type AssertionCallable = Callable[[Element | Fragment], None]
```

**Signature:**
- Takes: Element or Fragment (the rendered component)
- Returns: None on success
- Raises: AssertionError on failure

**Example:**

```python
def check_button(el: Element | Fragment) -> None:
    if "button" not in str(el).lower():
        raise AssertionError("Should be a button")
    return None

# Or as lambda
assertion = lambda el: None if "button" in str(el).lower() \
    else (_ for _ in ()).throw(AssertionError("Should be a button"))
```

### AssertionResult

Tuple representing an assertion test result:

```python
type AssertionResult = tuple[str, bool, str | None]
```

**Fields:**
1. `str` - Assertion name (e.g., "Assertion 1")
2. `bool` - Whether assertion passed
3. `str | None` - Error message if failed, None if passed

**Example:**

```python
result: AssertionResult = ("Assertion 1", True, None)  # Passed
result: AssertionResult = ("Assertion 2", False, "Should be button")  # Failed
```

### Target

Any callable that returns a Node:

```python
type Target = Callable[..., Node]
```

Usually a component function:

```python
def Button(text: str) -> Element:
    return h.button(text)

# Button is a valid Target
```

### Template

Custom rendering template for stories:

```python
type Template = Callable[[Story, Catalog], Node]
```

**Signature:**
- Takes: Story instance, Catalog instance
- Returns: Node (Element or Fragment)

**Example:**

```python
def custom_template(story: Story, catalog: Catalog) -> Node:
    return h.div(
        h.h1(story.title),
        story.instance,
        class_="custom",
    )
```

## Helper Functions

### make_catalog

Build a Catalog from a package:

```python
def make_catalog(package_location: str) -> Catalog:
    """Build story tree from package.

    Args:
        package_location: Python package path (e.g., "my_package")

    Returns:
        Catalog instance with full tree loaded
    """
```

**Example:**

```python
from storytime import make_catalog

catalog = make_catalog("my_package")
print(catalog.title)
print(len(catalog.items))
```

### find_path

Traverse tree using dotted notation:

```python
def find_path(catalog: Catalog, path: str) -> TreeNode | Story | None:
    """Find node by dotted path.

    Args:
        catalog: Catalog root
        path: Dotted path (e.g., ".section.subject.story")
        
    Returns:
        Found node, or None
    """
```

**Example:**

```python
from storytime import make_catalog, find_path

catalog = make_catalog("my_package")
subject = find_path(catalog, ".components.button")
story = find_path(catalog, ".components.button.primary")
```

## Build Functions

### build_catalog

Build static catalog from stories:

```python
def build_catalog(
    package_location: str,
    output_dir: Path,
    with_assertions: bool = True,
) -> None:
    """Build static catalog.
    
    Args:
        package_location: Package to build from
        output_dir: Where to write output
        with_assertions: Whether to execute assertions
    """
```

**Example:**

```python
from pathlib import Path
from storytime.build import build_site

build_site(
    package_location="my_package",
    output_dir=Path("./dist"),
    with_assertions=True,
)
```

## Web Application

### create_app

Create Starlette app:

```python
def create_app(
    path: Path,
    input_path: str | None = None,
    package_location: str | None = None,
    output_dir: Path | None = None,
    use_subinterpreters: bool = False,
    with_assertions: bool = True,
) -> Starlette:
    """Create web application.
    
    Args:
        path: Directory to serve
        input_path: Input package path (for watching)
        package_location: Package location (for watching)
        output_dir: Output directory (for watching)
        use_subinterpreters: Enable subinterpreter builds
        with_assertions: Execute assertions during rendering
        
    Returns:
        Starlette application
    """
```

**Example:**

```python
from pathlib import Path
from storytime.app import create_app

app = create_app(
    path=Path("./dist"),
    input_path="my_package",
    package_location="my_package",
    output_dir=Path("./dist"),
    use_subinterpreters=True,
    with_assertions=True,
)
```

## CLI Commands

### serve

Start development server:

```bash
storytime serve [PACKAGE] [OPTIONS]
```

**Options:**
- `--use-subinterpreters/--no-use-subinterpreters` - Enable subinterpreters (default: True)
- `--with-assertions/--no-with-assertions` - Enable assertions (default: True)

### build

Build static catalog:

```bash
storytime build [PACKAGE] [OUTPUT_DIR]
```

**Arguments:**
- `PACKAGE` - Package location (default: current directory)
- `OUTPUT_DIR` - Output directory (optional)

## pytest Plugin

The plugin is automatically registered and requires minimal configuration.

### Configuration

```toml
[tool.pytest.ini_options]
testpaths = ["tests", "examples/"]

[tool.storytime.pytest]
enabled = true
```

### Generated Tests

For each story with assertions, generates tests:
- Test name: `test_story[catalog.section.subject.story::assertion_name]`
- Test renders story fresh
- Test executes assertion
- Test reports failure with HTML diff

## Tree Nodes

### BaseNode

Base class for tree nodes:

```python
@dataclass
class BaseNode:
    parent: TreeNode | None = None
```

### TreeNode

Base class for nodes with children:

```python
@dataclass
class TreeNode(BaseNode):
    package_path: str = ""
```

**Inherited by:**
- Catalog
- Section
- Subject

## Exceptions

Storytime uses standard Python exceptions:

- `AssertionError` - Raised by failing assertions
- `ImportError` - Package/module import failures
- `ValueError` - Invalid configuration

## Next Steps

- [Getting Started](getting-started.md) - Begin using Storytime
- [Writing Stories](writing-stories.md) - Create your stories
- [pytest Plugin](pytest-plugin.md) - Testing integration
