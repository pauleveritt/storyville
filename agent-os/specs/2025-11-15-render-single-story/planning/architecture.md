# Architecture Notes: Render a Single Story

## File Structure

```
src/storyville/
├── models.py                    # NEW - Protocol definitions
└── story/
    ├── __init__.py             # NEW - Package initialization
    ├── models.py               # MODIFIED - Story class (remove vdom, update instance)
    └── views.py                # NEW - StoryView implementation

tests/
└── story/
    └── test_story_view.py      # NEW - StoryView tests
```

## Component Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                        View Protocol                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Protocol:                                           │   │
│  │    __call__(self) -> Element                        │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────┘
                             │ implements
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                         StoryView                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  @dataclass                                          │   │
│  │  story: Story                                        │   │
│  │                                                       │   │
│  │  __call__(self) -> Element:                         │   │
│  │    if story.template:                               │   │
│  │      return story.template(story)                   │   │
│  │    else:                                            │   │
│  │      return default_layout()                        │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────┘
                             │ uses
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                         Story Class                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  MODIFIED:                                           │   │
│  │    - Remove: vdom() method                          │   │
│  │    - Update: instance property                      │   │
│  │                                                       │   │
│  │  @property                                           │   │
│  │  def instance(self) -> Element:                     │   │
│  │    result = self.component(**self.props)            │   │
│  │    assert isinstance(result, Element)               │   │
│  │    return result                                    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Rendering Flow

### Scenario 1: Story with Custom Template

```
User calls StoryView()
    ↓
StoryView.__call__() checks story.template
    ↓
story.template is NOT None
    ↓
StoryView returns story.template(story)
    ↓
Returns tdom.Element
```

### Scenario 2: Story without Template (Default Layout)

```
User calls StoryView()
    ↓
StoryView.__call__() checks story.template
    ↓
story.template IS None
    ↓
StoryView builds default layout:
  - Story title
  - Props display with <code> block
  - Calls story.instance to get rendered component
  - Adds parent navigation link
    ↓
Returns tdom.Element
```

## Type Safety Flow

```
Story.component(**props) → tdom.Node
    ↓
Story.instance property applies type guard
    ↓
assert isinstance(result, Element)
    ↓
Returns tdom.Element (narrowed type)
    ↓
StoryView uses story.instance
    ↓
StoryView.__call__() returns Element
    ↓
Satisfies View Protocol contract
```

## Implementation Phases

### Phase 1: Protocol Definition
1. Create `src/storyville/models.py`
2. Define `View` Protocol with `__call__(self) -> Element`
3. Add necessary imports from tdom

### Phase 2: Story Modifications
1. Move Story class to `src/storyville/story/models.py` (if not already there)
2. Remove the `vdom` method from Story class
3. Update `instance` property:
   - Change return type to `Element`
   - Add type guard: `assert isinstance(result, Element)`

### Phase 3: StoryView Implementation
1. Create `src/storyville/story/__init__.py` (package initialization)
2. Create `src/storyville/story/views.py`
3. Import necessary types: Element, Story, View Protocol
4. Implement StoryView as dataclass with:
   - `story: Story` field
   - `__call__(self) -> Element` method
5. Implement conditional rendering logic:
   - Check if `self.story.template is not None`
   - If yes: return template result
   - If no: build and return default layout

### Phase 4: Default Layout Template
Create tdom template that renders:
```python
t"""
<article>
  <h1>{self.story.title}</h1>
  <section>
    <h2>Props</h2>
    <code>{str(self.story.props)}</code>
  </section>
  <section>
    <h2>Rendered Output</h2>
    {self.story.instance}
  </section>
  <nav>
    <a href="..">Back to Parent</a>
  </nav>
</article>
"""
```

### Phase 5: Testing
1. Create `tests/story/` directory
2. Create `tests/story/test_story_view.py`
3. Write tests for:
   - Story with template mode
   - Story without template (default layout)
   - Verification of title rendering
   - Verification of props display
   - Verification of instance rendering
   - Verification of parent link
   - Type safety checks
3. Use aria-testing for semantic HTML verification

## Key Design Decisions

### Why Protocol Instead of ABC?
- Protocols enable structural typing (duck typing with type safety)
- More flexible - any class with `__call__() -> Element` satisfies contract
- Follows modern Python typing patterns
- Easier to test and mock

### Why Dataclass for StoryView?
- Simple, immutable data structure
- Automatic `__init__` generation
- Clear, declarative syntax
- Follows Python 3.14+ best practices

### Why Type Guard in Story.instance?
- Ensures type safety at runtime
- Catches errors early in development
- Enables static type checkers to narrow type
- Provides clear contract: Story.instance ALWAYS returns Element

### Why Two Rendering Modes?
- **Custom template mode**: Provides maximum flexibility for complex stories
- **Default layout mode**: Provides sensible fallback with useful debugging info
- Clean separation allows evolution of default layout without breaking custom templates

## Testing Strategy

### Test Categories

**1. Template Mode Tests**
- Story with custom template renders template output
- Template receives correct story argument
- Result is tdom.Element type

**2. Default Layout Tests**
- Story without template renders default layout
- Title is present and correct
- Props are displayed in code block
- Instance is rendered correctly
- Parent link is present with correct href

**3. Type Safety Tests**
- StoryView.__call__() returns Element
- Story.instance returns Element
- Type guards work correctly

**4. Edge Cases**
- Empty props dictionary
- Complex nested props
- Story with no parent
- Long titles and content

### Test Tools
- **pytest**: Test framework
- **aria-testing**: Semantic HTML verification
- **ty**: Type checking during development

### Success Criteria
- All tests pass: `just test`
- Type checking passes: `just typecheck`
- Code formatting passes: `just fmt`
- 100% coverage of new StoryView code
- Clear, readable test names and assertions

## Future Considerations

**Not in this spec but worth noting:**

1. **Component Extraction**: The default layout could be refactored into reusable components (PropDisplay, StoryHeader, Navigation) in a future spec

2. **Starlette Integration**: Future spec will create Starlette route that instantiates StoryView and serves the result as HTML response

3. **Advanced Templates**: Future specs might support:
   - Template inheritance
   - Partial templates
   - Layout composition

4. **Enhanced Navigation**: Future specs might add:
   - Breadcrumb navigation
   - Sibling story links
   - Full hierarchy tree

5. **Styling**: Future specs will add:
   - CSS integration
   - Theme support
   - Responsive layouts

This spec focuses solely on the core rendering mechanism. Keep it simple and focused.
