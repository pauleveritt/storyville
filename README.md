# 📖 Storytime ✨

**Visual, story-based component development for Python 3.14+**

[![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Development Status](https://img.shields.io/badge/status-alpha-orange.svg)](https://github.com/pauleveritt/storytime)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: basedpyright](https://img.shields.io/badge/type%20checker-basedpyright-blue.svg)](https://github.com/DetachHead/basedpyright)
[![Built with: tdom](https://img.shields.io/badge/built%20with-tdom-purple.svg)](https://github.com/pauleveritt/t-strings)

---

## 🎯 What is Storytime?

Storytime is a **visual, component-driven development (CDD)** system for Python that helps you build, document, and test
components in isolation. Write stories to express component variations, browse them in a live catalog, and automatically
generate tests from assertions.

> 💡 **Think Storybook.js for Python** — but with native Python 3.14+ features, hot reload via subinterpreters, and
> automatic pytest integration!

### 🌟 Perfect for:

- 🎨 **Building component libraries** with tdom
- 👀 **Visual component development** and documentation
- ✅ **Test-driven component design**
- 🔥 **Hot-reloading Python modules** during development

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🎨 **Component Catalog**

- 🌐 Browse components and their variations in a live web interface
- 💅 PicoCSS-based clean, responsive UI
- ⚡ Real-time hot reload with subinterpreter isolation
- 📂 Hierarchical organization: Catalog → Section → Subject → Story

</td>
<td width="50%">

### 🧪 **Story Assertions**

- ✍️ Define assertions directly on stories
- ✅❌ Visual pass/fail badges in the browser
- 🤖 Automatic pytest test generation (zero boilerplate)
- 📊 Rich failure reporting with HTML diffs

</td>
</tr>
<tr>
<td width="50%">

### ⚡ **Hot Reload with Subinterpreters**

- 🐍 Python 3.14+ subinterpreter pool for true module reloading
- ⏱️ Instant updates when you save `stories.py` files
- 🚫 No server restarts needed
- 💾 Maintains state across rebuilds

</td>
<td width="50%">

### 🔬 **pytest Plugin**

- 🔍 Automatically discovers stories with assertions
- 📝 Generates one test per assertion
- 🏷️ Clear test naming: `test_story[catalog.section.subject.story::assertion]`
- 🔀 Works with pytest-xdist for parallel execution
- 🆕 Fresh rendering per test for proper isolation

</td>
</tr>
<tr>
<td colspan="2">

### 🎨 **Themed Stories**

- 🎭 Preview components within custom-themed layouts
- 🖼️ Isolated iframe rendering for visual separation
- 🎯 Catalog-level theme configuration with automatic fallback
- 📄 Full HTML document control for real-world context
- 🎨 Perfect for matching your project's design system

</td>
</tr>
</table>

---

## 📦 Installation

```bash
# Requires Python 3.14+
pip install storytime
```

> ⚠️ **Note:** Storytime requires Python 3.14+ for subinterpreter support and modern type syntax.

<details>
<summary>📸 <strong>See it in action!</strong></summary>

<!-- Replace with actual screenshot once available -->
![Storytime Catalog Interface](https://via.placeholder.com/800x450.png?text=Storytime+Catalog+Browser)

*Browse components, view stories, and see assertion results in real-time*

</details>

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


def check_is_button(el) -> None:
    """Assertion: element should be a button tag."""
    assert "button" in str(el).lower(), "Should be a button element"


def this_subject() -> Subject:
    return Subject(
        title="Button Component",
        target=Button,
        items=[
            # Story with assertions
            Story(
                props=dict(text="Click Me", variant="primary"),
                assertions=[check_is_button],
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
from tdom import Node, html


@dataclass
class ThemedLayout:
    story_title: str | None
    children: Node | None

    def __call__(self) -> Node:
        """Render the themed layout using tdom t-string."""
        title_text = self.story_title if self.story_title else "Story"

        return html(t'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title_text}</title>
    <style>
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: system-ui;
            margin: 0;
            padding: 20px;
        }}
        .story-wrapper {{
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 12px;
        }}
    </style>
</head>
<body>
    <div class="story-wrapper">
        {self.children}
    </div>
</body>
</html>
''')


# my_package/stories.py
from tdom import Node
from storytime import Catalog
from my_package.themed_layout.themed_layout import ThemedLayout


def themed_layout_wrapper(story_title: str | None = None, children: Node | None = None) -> Node:
    """Wrapper function to create and call ThemedLayout instances."""
    layout = ThemedLayout(story_title=story_title, children=children)
    return layout()


def this_catalog() -> Catalog:
    return Catalog(themed_layout=themed_layout_wrapper)
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

### 🐍 Modern Python 3.14+

- ✨ **Type statement** for type aliases: `type AssertionCallable = Callable[[Element | Fragment], None]`
- 🔀 **PEP 604 union syntax**: `X | Y` instead of `Union[X, Y]`
- 🔍 **Structural pattern matching** for clean conditionals
- 🔄 **Subinterpreter pool** for true module isolation

### 🛠️ Built on Solid Foundations

| Technology        | Purpose                        |
|-------------------|--------------------------------|
| 🎯 **tdom**       | Templating and HTML generation |
| 🚀 **Starlette**  | Async web framework            |
| ✅ **pytest**      | Testing infrastructure         |
| 💅 **PicoCSS**    | Semantic CSS framework         |
| 👀 **watchfiles** | Fast file change detection     |

### 🌲 Tree Structure

```
📖 Catalog
  ├─ 📁 Section (optional grouping)
  │   └─ 🎯 Subject (component)
  │       ├─ 📄 Story (variation)
  │       └─ 📄 Story (with ✅ assertions)
  └─ 🎯 Subject
      └─ 📄 Story
```

---

## 🎯 Use Cases

| Use Case                       | Description                                                                            |
|--------------------------------|----------------------------------------------------------------------------------------|
| 📚 **Component Libraries**     | Build and document reusable components with all their variations in one place          |
| 🎨 **Design Systems**          | Create a browseable catalog of your design system components with live examples        |
| 🧪 **Test-Driven Development** | Write assertions alongside stories for immediate visual and automated testing feedback |
| 📖 **Living Documentation**    | Stories serve as both visual documentation and executable examples                     |

---

## 🤝 Contributing

Contributions are welcome! 🎉 This project uses modern Python tooling:

| Tool                | Purpose                  |
|---------------------|--------------------------|
| 📦 **uv**           | Dependency management    |
| 🧹 **ruff**         | Linting and formatting   |
| ✅ **pytest**        | Testing framework        |
| 🔍 **basedpyright** | Type checking            |
| 📚 **sphinx**       | Documentation generation |

### 🛠️ Development Setup

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

### 📋 Contribution Guidelines

- ✅ All tests must pass
- 🔍 Type checking must succeed
- 🧹 Code must be formatted with ruff
- 📝 Add tests for new features
- 📚 Update documentation as needed

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🔗 Links

| Resource            | URL                                                                                                  |
|---------------------|------------------------------------------------------------------------------------------------------|
| 🏠 **Repository**   | [github.com/pauleveritt/storytime](https://github.com/pauleveritt/storytime)                         |
| 🐛 **Issues**       | [github.com/pauleveritt/storytime/issues](https://github.com/pauleveritt/storytime/issues)           |
| 📝 **Discussions**  | [github.com/pauleveritt/storytime/discussions](https://github.com/pauleveritt/storytime/discussions) |
| 🎯 **tdom Project** | [github.com/pauleveritt/t-strings](https://github.com/pauleveritt/t-strings)                         |

---

<div align="center">

**Made with 💜 by Paul Everitt**

⭐ **Star this repo if you find it useful!** ⭐

</div>
