# UI Components

- Single responsibility per component
- Reusable with configurable props
- Compose complex UIs from small components
- Clear, documented interfaces with defaults
- Keep state local; lift only when needed
- Minimal props; split if too many

## tdom Component Composition

### Passing Children to Components

In tdom (like React), children are passed using nested syntax, **not** as props:

**✓ Correct:**
```python
<{MyComponent} prop1={value1}>
  <div>This is a child</div>
  {some_node}
</{MyComponent}>
```

**✗ Incorrect:**
```python
<{MyComponent} prop1={value1} children={some_node} />
```

### How It Works

When you write:
```python
<{MyComponent} prop1="hello">
  <div>Child content</div>
</{MyComponent}>
```

The component receives:
- `prop1="hello"` as a regular prop
- `children` prop automatically populated with the nested content (`<div>Child content</div>`)

### Component Implementation

Components should declare `children` in their dataclass:

```python
@dataclass
class MyComponent:
    prop1: str
    children: Element | Fragment | Node | None = None

    def __call__(self) -> Node:
        return html(t'''
<div class="wrapper">
  <h2>{self.prop1}</h2>
  {self.children}
</div>
''')
```

### Example Usage

```python
# Layout component using proper children syntax
return html(t'''
<body>
  <{Header} title="Site" />
  <{Main} current_path="/home">
    <article>
      <h1>Page Content</h1>
      <p>This gets passed as children</p>
    </article>
  </{Main}>
  <{Footer} year={2025} />
</body>
''')
```

### Self-Closing vs Nested Syntax

- **Self-closing** (`<{Component} />`) when component has no children
- **Nested** (`<{Component}>...</{Component}>`) when passing children content
