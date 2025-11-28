# Storytime ✨

**Story-based component development for Python 3.14+**

[![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Development Status](https://img.shields.io/badge/status-alpha-orange.svg)](https://github.com/pauleveritt/storytime)

---

## 🎯 What is Storytime?

Storytime is a component-driven development (CDD) system for Python that helps you build, document, and test components in isolation. Write stories to express component variations, browse them in a live catalog, and automatically generate tests from assertions.

**Perfect for:**
- Building component libraries with tdom
- Visual component development and documentation
- Test-driven component design
- Hot-reloading Python modules during development

---

## ✨ Key Features

### 🎨 **Component Catalog**
- Browse components and their variations in a live web interface
- PicoCSS-based clean, responsive UI
- Real-time hot reload with subinterpreter isolation
- Hierarchical organization: Site → Section → Subject → Story

### 🧪 **Story Assertions**
- Define assertions directly on stories
- Visual pass/fail badges in the browser
- Automatic pytest test generation (zero boilerplate)
- Rich failure reporting with HTML diffs

### ⚡ **Hot Reload with Subinterpreters**
- Python 3.14+ subinterpreter pool for true module reloading
- Instant updates when you save `stories.py` files
- No server restarts needed
- Maintains state across rebuilds

### 🔬 **pytest Plugin**
- Automatically discovers stories with assertions
- Generates one test per assertion
- Clear test naming: `test_story[site.section.subject.story::assertion]`
- Works with pytest-xdist for parallel execution
- Fresh rendering per test for proper isolation

### 🎨 **Themed Stories**
- Preview components within custom-themed layouts
- Isolated iframe rendering for visual separation
- Site-level theme configuration with automatic fallback
- Full HTML document control for real-world context
- Perfect for matching your project's design system

---

## 📦 Installation

```bash
# Requires Python 3.14+
pip install storytime
```

> **Note:** Storytime requires Python 3.14+ for subinterpreter support and modern type syntax.

---

## 🚀 Quick Start

### 1. Create a Component

```python
# my_package/components/button/button.py
from tdom import html as h

def Button(text: str, variant: str = "primary"):
    """A simple button component."""
    return h.button(text, class_=variant)
```

### 2. Write Stories

```python
# my_package/components/button/stories.py
from my_package.components.button.button import Button
from storytime import Story, Subject

def this_subject() -> Subject:
    return Subject(
        title="Button Component",
        target=Button,
        items=[
            # Story with assertions
            Story(
                props=dict(text="Click Me", variant="primary"),
                assertions=[
                    lambda el: None if "button" in str(el).lower()
                    else (_ for _ in ()).throw(AssertionError("Should be a button")),
                ],
            ),
            # More variations...
            Story(props=dict(text="Cancel", variant="danger")),
        ],
    )
```

### 3. Start the Dev Server

```bash
storytime serve my_package
# Opens http://localhost:8080
# Hot reload enabled by default!
```

### 4. Add Custom Theming (Optional)

```python
# my_package/themed_layout/themed_layout.py
from dataclasses import dataclass
from tdom import html as t, Node

@dataclass
class ThemedLayout:
    story_title: str | None
    children: Node | None

    def __call__(self) -> Node:
        return t.html(
            t.head(
                t.meta(charset="utf-8"),
                t.title(f"{self.story_title or 'Story'}"),
                t.style("""
                    body {
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        font-family: system-ui;
                    }
                """),
            ),
            t.body(t.div(self.children, class_="story-wrapper")),
            lang="en",
        )

# my_package/__init__.py
from storytime import Site
from my_package.themed_layout.themed_layout import ThemedLayout

def themed_layout_wrapper(story_title: str, children: Node) -> Node:
    return ThemedLayout(story_title, children)()

def this_site() -> Site:
    return Site(themed_layout=themed_layout_wrapper)
```

### 5. Run Tests

```bash
# Configure pytest in pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests", "my_package"]

[tool.storytime.pytest]
enabled = true

# Run tests
pytest my_package/
# Auto-generates tests from story assertions!
```

---

## 📚 Documentation

- **[Getting Started](docs/getting-started.md)** - Installation and first steps
- **[Writing Stories](docs/writing-stories.md)** - Component stories and assertions
- **[Themed Stories](docs/themed-stories.md)** - Custom layouts and design system integration
- **[pytest Plugin](docs/pytest-plugin.md)** - Automatic test generation
- **[Hot Reload](docs/hot-reload.md)** - Subinterpreter architecture
- **[API Reference](docs/api-reference.md)** - Complete API documentation

---

## 🏗️ Architecture Highlights

### Modern Python 3.14+
- Type statement for type aliases: `type AssertionCallable = Callable[[Element | Fragment], None]`
- PEP 604 union syntax: `X | Y`
- Structural pattern matching
- Subinterpreter pool for module isolation

### Built on Solid Foundations
- **tdom**: Templating and HTML generation
- **Starlette**: Async web framework
- **pytest**: Testing infrastructure
- **PicoCSS**: Semantic CSS framework
- **watchfiles**: Fast file change detection

### Tree Structure
```
Site
  ├─ Section (optional)
  │   └─ Subject
  │       └─ Story (with assertions)
  └─ Subject
      └─ Story
```

---

## 🎯 Use Cases

### Component Libraries
Build and document reusable components with all their variations in one place.

### Design Systems
Create a browseable catalog of your design system components with live examples.

### Test-Driven Development
Write assertions alongside stories for immediate visual and automated testing feedback.

### Documentation
Stories serve as both visual documentation and executable examples.

---

## 🤝 Contributing

Contributions are welcome! This project uses:
- **uv** for dependency management
- **ruff** for linting
- **pytest** for testing
- **ty** for type checking
- **sphinx** for documentation

```bash
# Install dev dependencies (includes Sphinx)
uv sync --group dev

# Run tests
just test

# Type check
just typecheck

# Format code
just fmt

# Build documentation
cd docs && make html
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🔗 Links

- **Repository**: [github.com/pauleveritt/storytime](https://github.com/pauleveritt/storytime)
- **Issues**: [github.com/pauleveritt/storytime/issues](https://github.com/pauleveritt/storytime/issues)
- **tdom**: [github.com/pauleveritt/t-strings](https://github.com/pauleveritt/t-strings)

---

**Made with 💜 by Paul Everitt**
