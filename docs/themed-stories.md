# Themed Stories

Themed Stories allow you to preview your components within custom-themed layouts, providing visual isolation and
real-world context. When configured, Storyville generates an additional HTML file for each story that renders the
component within your custom theme, displayed in an iframe for visual separation.

## Overview

By default, Storyville displays components in a standard layout with PicoCSS styling. With Themed Stories, you can:

- **Preview in Real Context**: See components rendered with your project's actual design system
- **Visual Isolation**: Stories are rendered in iframes to prevent style conflicts
- **Custom Branding**: Match your organization's look and feel
- **Full HTML Control**: Define complete HTML documents with custom CSS, meta tags, and more

## Quick Start

### 1. Create a ThemedLayout Component

Create a callable component that accepts `story_title` and `children` props and returns a complete HTML document:

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
                t.meta(name="viewport", content="width=device-width, initial-scale=1"),
                t.title(f"{self.story_title or 'Story'}"),
                t.style("""
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        min-height: 100vh;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin: 0;
                        padding: 20px;
                    }
                    .story-wrapper {
                        background: rgba(255, 255, 255, 0.95);
                        border-radius: 12px;
                        padding: 2rem;
                        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                        backdrop-filter: blur(10px);
                        max-width: 800px;
                    }
                """),
            ),
            t.body(
                t.div(self.children, class_="story-wrapper")
            ),
            lang="en",
        )
```

### 2. Configure Your Catalog

Add the themed layout to your Catalog configuration:

```python
# my_package/__init__.py
from storyville import Catalog
from my_package.themed_layout.themed_layout import ThemedLayout


def themed_layout_wrapper(story_title: str, children: Node) -> Node:
    """Wrapper function to instantiate and call ThemedLayout."""
    return ThemedLayout(story_title, children)()


def this_catalog() -> Catalog:
    return Catalog(themed_layout=themed_layout_wrapper)
```

### 3. Build and View

When you build your catalog or start the dev server, Storyville will now generate two HTML files per story:

- `story-N/index.html` - The standard Storyville view with an iframe
- `story-N/themed_story.html` - Your component rendered in the custom theme

The iframe in `index.html` points to `./themed_story.html` using a relative path.

## Technical Details

### ThemedLayout Interface

Your ThemedLayout must be a callable that accepts two parameters:

- `story_title: str` - The title of the story being rendered
- `children: Node` - The rendered component (story instance) as a tdom Node

And returns a tdom `Node` representing a complete HTML document.

### Catalog Configuration

The `Catalog.themed_layout` property accepts:

```python
themed_layout: Callable[..., Node] | None = None
```

If `None` (the default), Storyville uses the standard Layout component and no iframe is rendered.

### File Generation

During the build process:

1. **Phase 2 (Rendering)**: Storyville renders both the standard StoryView and the ThemedStory for each story
2. **Phase 3 (Writing)**: Two HTML files are written to disk:
    - `index.html` contains the StoryView with iframe
    - `themed_story.html` contains the full themed HTML document

### Directory Structure

```
output/
├── section-name/
│   └── subject-name/
│       ├── story-0/
│       │   ├── index.html           # StoryView with iframe
│       │   └── themed_story.html    # Themed rendering
│       ├── story-1/
│       │   ├── index.html
│       │   └── themed_story.html
│       └── index.html
└── index.html
```

## Example: Design System Integration

Here's a more complete example showing integration with a design system:

```python
from dataclasses import dataclass
from tdom import html as t, Node


@dataclass
class DesignSystemLayout:
    story_title: str | None
    children: Node | None

    def __call__(self) -> Node:
        return t.html(
            t.head(
                t.meta(charset="utf-8"),
                t.meta(name="viewport", content="width=device-width, initial-scale=1"),
                t.title(f"Design System - {self.story_title or 'Story'}"),
                # Link to your design system CSS
                t.link(rel="stylesheet", href="/static/design-system.css"),
                # Custom page styles
                t.style("""
                    body {
                        background: var(--ds-bg-primary);
                        padding: 2rem;
                    }
                    .preview-container {
                        background: var(--ds-bg-surface);
                        border-radius: var(--ds-radius-lg);
                        padding: 3rem;
                        box-shadow: var(--ds-shadow-lg);
                    }
                """),
            ),
            t.body(
                t.div(
                    t.header(
                        t.h1(self.story_title or "Component Preview"),
                        class_="preview-header"
                    ),
                    t.div(self.children, class_="preview-content"),
                    class_="preview-container"
                ),
                class_="design-system-preview"
            ),
            lang="en",
        )
```

## Best Practices

### 1. Complete HTML Documents

Always render complete HTML documents with proper DOCTYPE, lang attributes, and meta tags:

```python
return t.html(
    t.head(
        t.meta(charset="utf-8"),
        t.meta(name="viewport", content="width=device-width, initial-scale=1"),
        t.title("..."),
        # styles, scripts, etc.
    ),
    t.body(
        # your content
    ),
    lang="en",
)
```

### 2. External Stylesheets

Link to your actual CSS files to see components in their real styling context:

```python
t.link(rel="stylesheet", href="/static/your-styles.css")
```

### 3. Wrapper Function Pattern

Use a wrapper function to instantiate your ThemedLayout class:

```python
def themed_layout_wrapper(story_title: str, children: Node) -> Node:
    return ThemedLayout(story_title, children)()
```

This pattern ensures the callable signature matches Storyville's expectations while allowing you to use dataclasses for
your layout components.

### 4. Testing Your Theme

Write tests to verify your ThemedLayout renders correctly:

```python
def test_themed_layout_renders_full_html():
    from aria_testing import parse_html, get_by_tag_name

    layout = ThemedLayout(
        story_title="Test Story",
        children=html(t.div("Test content"))
    )
    result = layout()
    rendered = str(result)

    doc = parse_html(rendered)
    html_elem = get_by_tag_name(doc, "html")
    head = get_by_tag_name(html_elem, "head")
    body = get_by_tag_name(html_elem, "body")

    assert head is not None
    assert body is not None
```

## Backward Compatibility

Themed Stories is an opt-in feature:

- If `Catalog.themed_layout` is `None` (default), stories render with standard Layout
- No iframe is displayed when themed layout is not configured
- Existing builds remain unchanged
- No performance impact when feature is unused

## Roadmap

Future enhancements planned:

- **Multiple Themes** (Roadmap #20): Switch between themes in the UI
- **Theme Marketplace**: Share and discover community themes
- **Per-Section Themes**: Override themes at section or subject level
- **Interactive Theme Editor**: Customize themes directly in the browser

## See Also

- [Writing Stories](writing-stories.md) - How to create component stories
- [Component Architecture](architecture.md) - Understanding Storyville's structure
