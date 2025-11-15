# Spec Requirements: Render a Single Story

## Initial Description

Render a single Story. A Story should have a StoryView which receives the `story: Story` and uses a tdom template and
possibly some components to return a tdom.Element. You might need to do some type guard to convert tdom.Node to
tdom.Element before returning.

## Product Context

### Product Mission Alignment

This spec contributes to Storytime's core mission of providing a "Storybook-like experience" for Python developers by
implementing the fundamental rendering mechanism for individual stories. This is a critical piece of the "Component
Isolation" and "Story-Based Development" core features, enabling developers to visualize UI components independently of
web frameworks.

### Roadmap Position

This spec directly supports multiple roadmap items:

- **Item #1 - Component Rendering System**: This spec implements the story-level rendering that produces HTML output
  from Story instances
- **Item #2 - Story Definition API**: The StoryView provides the rendering layer for Story instances
- **Item #3 - Web-Based Component Browser**: Creates the foundation for the browser to display individual stories

This is foundational work that must be completed before the web-based component browser can function.

### Technology Stack

This spec leverages:

- **tdom**: For all templating and HTML generation
- **Python 3.14+**: Using modern type hints, type guards, and protocols
- **Type safety**: Protocol-based design with strict type checking via `ty`
- **pytest + aria-testing**: For comprehensive test coverage

## Requirements Discussion

### First Round Questions

**Q1:** Should the View Protocol be defined in a new `src/storytime/models.py` file, or would you prefer a different
location (like `src/storytime/protocols.py` or directly in the story module)?
**Answer:** Create `src/storytime/models.py` with the View Protocol.

**Q2:** For the Story class changes, should we remove the `vdom` method entirely and have the `Story.instance` property
return `tdom.Element` directly (with a type guard inside the property)?
**Answer:** Yes, remove `vdom` method. Add type guard inside the `Story.instance` property to convert `tdom.Node` to
`tdom.Element`.

**Q3:** For the StoryView implementation, I'm assuming it should be a dataclass with a `__call__()` method that returns
`Element`. Should this be in a new file `src/storytime/story/views.py`?
**Answer:** Yes, create `src/storytime/story/views.py` with StoryView as a dataclass.

**Q4:** When Story.template is None, what should StoryView display as the default layout? Should it show the story
title, rendered content, props, and a link back to the parent?
**Answer:** Yes, show:

- Story title
- Props display: "Props: <code>{str(self.story.props)}</code>"
- Rendered contents via `Story.instance`
- Link to parent with `href=".."`

**Q5:** When Story.template is provided (not None), should StoryView use that template for ALL rendering (ignoring the
default layout), or should it wrap the template with additional elements?
**Answer:** Use template for ALL rendering. No wrapping.

**Q6:** For the type guard converting `tdom.Node` to `tdom.Element`, should we use `assert isinstance(result, Element)`
or a more sophisticated type narrowing approach?
**Answer:** Use `assert isinstance(result, Element)` inside the `__call__` method.

**Q7:** Should StoryView have any error handling for edge cases (empty story, missing props, etc.), or should we let
exceptions propagate naturally?
**Answer:** Let exceptions propagate naturally. No special error handling.

**Q8:** For testing, should we focus only on Story rendering, or should we also test integration with Starlette
request/response cycles?
**Answer:** Focus only on Story rendering. No Starlette integration testing for this spec.

**Q9:** Are there any reusable layout components we should extract (header, prop display, navigation), or should this be
a standalone template for now?
**Answer:** Standalone template for now. No reusable components.

**Q10:** What should be explicitly excluded from this spec? Should we avoid any hierarchy navigation beyond the parent
link?
**Answer:** Exclude:

- Full hierarchy navigation (only show parent link)
- Starlette integration details
- Advanced layout features
  Focus solely on Story rendering.

### Existing Code to Reference

**Similar Features Identified:**
No similar existing features were identified for reference. This is foundational rendering functionality.

### Follow-up Questions

No follow-up questions were required. All requirements were clarified in the first round.

## Visual Assets

### Files Provided:

No visual assets provided.

### Visual Insights:

N/A - No visual files were found in the visuals folder.

## Requirements Summary

### Functional Requirements

**1. View Protocol Definition**

- Create new file: `src/storytime/models.py`
- Define `View` Protocol with signature: `__call__(self) -> Element`
- This provides a type contract for all view classes

**2. Story Class Modifications**

- **Remove**: The `vdom` method from the Story class
- **Modify**: The `Story.instance` property to:
    - Return type: `tdom.Element` (not `tdom.Node`)
    - Add type guard inside property: `assert isinstance(result, Element)` to ensure Node → Element conversion

**3. StoryView Implementation**

- Create new package: `src/storytime/story/` with `__init__.py`
- Create new file: `src/storytime/story/views.py`
- Implement `StoryView` as a dataclass
- Constructor parameter: `story: Story`
- Implement `__call__(self) -> Element` method (satisfying View Protocol)
- Rendering logic with two modes:

  **Mode A - When Story.template is NOT None:**
    - Use `Story.template` for ALL rendering
    - No additional wrapping or layout elements
    - Template controls complete output

  **Mode B - When Story.template IS None (default layout):**
    - Display story title
    - Display props: Show "Props: <code>{str(self.story.props)}</code>"
    - Display rendered content: Call `Story.instance` to get rendered component
    - Display parent link: `<a href="..">Parent</a>` or similar navigation

- Type safety: Use `assert isinstance(result, Element)` inside `__call__` to ensure return type
- Error handling: No special error handling - let exceptions propagate naturally

**4. Testing Requirements**

- Write comprehensive tests in `tests/` using pytest
- Use aria-testing for accessibility verification
- Test coverage must include:
    - Story with template (Mode A)
    - Story without template (Mode B - default layout)
    - Rendering of story title, props, and instance
    - Parent link presence and href value
    - Type safety (ensure Element is returned)
    - Edge cases with various prop values
- Focus ONLY on Story rendering
- Do NOT test Starlette integration

### Reusability Opportunities

None identified. This is foundational code with no existing similar features to reference.

Future specs may extract reusable components from the StoryView default layout (headers, prop displays, navigation
elements), but this spec implements them as standalone template code.

### Scope Boundaries

**In Scope:**

- Creating `src/storytime/models.py` with View Protocol
- Creating `src/storytime/story/` package with `__init__.py`
- Creating `src/storytime/story/views.py` with StoryView class
- Moving/modifying Story class in `src/storytime/story/models.py` to remove `vdom` and update `instance` property
- Implementing two rendering modes (with/without template)
- Type guards for Node → Element conversion
- Comprehensive pytest tests using aria-testing
- Default layout showing title, props, content, and parent link

**Out of Scope:**

- Starlette integration and request/response handling
- Full hierarchy navigation (beyond single parent link)
- Advanced layout features or styling
- Reusable component extraction
- Error handling and validation (let exceptions propagate)
- Custom error pages or fallback rendering
- Any UI beyond the basic default layout
- Integration with the web-based component browser
- Hot reload functionality
- CLI integration

### Technical Considerations

**Type Safety:**

- Use Protocol for View to enable structural typing
- Type guard (`assert isinstance`) to narrow Node → Element
- Leverage Python 3.14+ type hints throughout
- Ensure all return types match Protocol contract

**Architecture:**

- Separation of concerns: Story (data model) vs StoryView (presentation)
- View Protocol enables future view implementations
- Template system allows complete rendering override
- Default layout provides sensible fallback

**Testing Strategy:**

- Focus on pure rendering output verification
- Use aria-testing for semantic HTML validation
- Test both template modes thoroughly
- Verify type safety and contract adherence
- No framework overhead - fast, isolated tests

**Integration Points:**

- Story class (existing) - will be modified
- tdom library - used for all templating
- Future: Starlette will call StoryView to render stories in browser

**Code Quality:**

- All changes must pass: `just test`, `just typecheck`, `just fmt`
- Follow Python 3.14+ standards (match/case, modern type hints, PEP 695)
- Use type statement for aliases if needed
- Keep implementations simple - no premature abstraction
