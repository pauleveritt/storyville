# Getting Started

## Installation

Storytime requires Python 3.14+ for subinterpreter support and modern type syntax.

```bash
pip install storytime
```

Or using uv:

```bash
uv add storytime
```

## Prerequisites

- **Python 3.14+** - Required for subinterpreter pool and modern type syntax
- **tdom** - Templating library (automatically installed as dependency)
- **Starlette** - Web framework (automatically installed)

## Your First Story

### 1. Project Structure

Create a simple project structure:

```
my_project/
├── pyproject.toml
└── my_project/
    ├── __init__.py
    └── components/
        └── button/
            ├── __init__.py
            ├── button.py
            └── stories.py
```

### 2. Create a Component

```python
# my_project/components/button/button.py
from tdom import html as h

def Button(text: str, variant: str = "primary"):
    """A simple button component."""
    return h.button(text, class_=variant)
```

### 3. Write Stories

```python
# my_project/components/button/stories.py
from my_project.components.button.button import Button
from storytime import Story, Subject

def this_subject() -> Subject:
    """Define stories for the Button component."""
    return Subject(
        title="Button Component",
        description="Interactive button with variants",
        target=Button,
        items=[
            Story(
                title="Primary Button",
                props=dict(text="Click Me", variant="primary"),
            ),
            Story(
                title="Danger Button",  
                props=dict(text="Delete", variant="danger"),
            ),
        ],
    )
```

### 4. Start the Development Server

```bash
storytime serve my_project
```

This will:
1. Build the catalog from your stories
2. Start a server at http://localhost:8080
3. Enable hot reload (changes auto-update in browser)
4. Use subinterpreters for true module reloading

Visit http://localhost:8080 to browse your component catalog!

## CLI Commands

### serve

Start the development server with hot reload:

```bash
storytime serve [PACKAGE] [OPTIONS]
```

**Options:**
- `--use-subinterpreters/--no-use-subinterpreters` - Enable subinterpreter isolation (default: True)
- `--with-assertions/--no-with-assertions` - Enable assertion execution (default: True)

**Examples:**

```bash
# Serve with defaults (subinterpreters + assertions enabled)
storytime serve my_project

# Disable subinterpreters (faster but no module reload)
storytime serve my_project --no-use-subinterpreters

# Disable assertions (faster rendering)
storytime serve my_project --no-with-assertions
```

### build

Build the static catalog without starting a server:

```bash
storytime build [PACKAGE] [OUTPUT_DIR]
```

**Examples:**

```bash
# Build to default output directory
storytime build my_project

# Build to custom directory
storytime build my_project ./dist
```

## Configuration

### pytest Configuration

Add to your `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests", "my_project"]

[tool.storytime.pytest]
enabled = true
```

This enables automatic test generation from story assertions.

## Next Steps

- [Writing Stories](writing-stories.md) - Learn about Story structure and assertions
- [pytest Plugin](pytest-plugin.md) - Automatic test generation
- [Hot Reload](hot-reload.md) - Understanding subinterpreters
