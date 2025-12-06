# Specification: Render a Single Story

## Goal

Implement a rendering system for individual Story instances using tdom templates, with support for custom templates and
a default layout that displays story metadata and component output.

## User Stories

- As a component developer, I want to render a Story with a custom template so that I have full control over the
  presentation
- As a component developer, I want to render a Story with a default layout so that I can quickly view component output,
  props, and navigation without writing templates

## Specific Requirements

**View Protocol Definition**

- Create new file `src/storyville/models.py` with a `View` Protocol
- Protocol defines single method signature: `__call__(self) -> Element`
- Enables type-safe structural typing for all view implementations
- Protocol allows future view classes to satisfy the contract without inheritance

**Story Class Instance Property Update**

- Modify `Story.instance` property in `src/storyville/story/models.py` to return `Element` instead of `object | None`
- Add type guard inside property: `assert isinstance(result, Element)` to ensure Node to Element conversion
- Keep component instantiation logic: `self.component(**self.props)`
- This property provides the rendered component instance for StoryView to embed

**Story Class VDOM Method Removal**

- Remove the `vdom` method entirely from `src/storyville/story/models.py` (if it exists)
- All rendering should flow through StoryView's `__call__` method instead
- Ensures separation of concerns between data model (Story) and presentation (StoryView)

**StoryView Dataclass Structure**

- Create new file `src/storyville/story/views.py`
- Implement StoryView as a `@dataclass` with field `story: Story`
- Implement `__call__(self) -> Element` method satisfying View Protocol
- Use tdom t-string templates for all HTML generation
- Import required types: `from tdom import html, Element, Node`

**Custom Template Rendering Mode**

- When `story.template` is not None, use it for ALL rendering
- Call the template directly without any wrapping elements
- Template receives full control over HTML structure
- No additional layout, headers, or navigation should be added

**Default Layout Rendering Mode**

- When `story.template` is None, render a complete default layout containing:
- Story title as heading element (h1 or h2)
- Props display showing "Props: " followed by `<code>{str(self.story.props)}</code>`
- Rendered component content by calling `self.story.instance`
- Parent navigation link with `href=".."` and text "Parent" or similar

**Type Safety Implementation**

- Inside `__call__` method, use `assert isinstance(result, Element)` before returning
- Ensures tdom.Node is properly narrowed to tdom.Element
- Satisfies Protocol contract's Element return type
- Enables type checker to verify correctness

**Error Handling Strategy**

- No special error handling or try/except blocks
- Let exceptions propagate naturally to caller
- Missing components, invalid props, or template errors should raise immediately
- Follows fail-fast principle for easier debugging

**Test Coverage for StoryView**

- Create `tests/story/test_story_view.py` with comprehensive tests
- Test custom template mode: Story with template renders using that template
- Test default layout mode: Story without template shows title, props, instance, parent link
- Use aria-testing functions (get_by_tag_name, get_text_content) to verify HTML structure
- Test type safety: verify `__call__` returns Element instance
- Test edge cases: various prop values (empty dict, complex objects, nested structures)

**Test Infrastructure**

- Create `tests/story/` directory if it doesn't exist
- Use pytest fixtures for common test data (sample stories, components)
- Import `from aria_testing import get_by_tag_name, get_text_content` for HTML verification
- StoryView returns `tdom.Element` directly - use it directly with aria-testing functions
- Follow existing test patterns from `tests/test_story.py` and `tests/test_build.py`

## Visual Design

No visual assets provided.

## Existing Code to Leverage

**IndexView Pattern (`src/storyville/views/index_view.py`)**

- Dataclass-based view with `__call__(self) -> Node` signature
- Uses tdom t-string templates: `html(t"""...""")`
- Shows established pattern for view classes in this codebase
- StoryView should follow this exact structure but return Element instead of Node

**Layout Component (`src/storyville/components/layout/__init__.py`)**

- Demonstrates complex tdom template with embedded components
- Shows how to interpolate values: `{self.title}`, `{self.children}`
- Uses `<{Component} prop={value} />` syntax for embedding components
- Reference for tdom template syntax and component composition

**Story Test Patterns (`tests/test_story.py`)**

- Shows use of dataclasses for test components
- Pattern for testing component instantiation with props
- Demonstrates property testing and post_update lifecycle
- Use similar patterns for StoryView testing structure

**Aria Testing Pattern (`tests/test_build.py`)**

- Imports: `from aria_testing import get_by_tag_name, get_text_content`
- Note: test_build.py uses `parse_html(html_string)` for HTML strings, but StoryView returns Element directly
- For StoryView tests: pass the Element returned by `StoryView(story)()` directly to aria-testing functions
- Calls `get_by_tag_name(element, "p")` to find elements
- Calls `get_text_content(p)` to extract text for assertions

**Story Instance Property (`src/storyville/story/models.py`)**

- Current implementation returns `object | None`
- Instantiates component: `self.component(**self.props)`
- Need to modify return type and add type guard
- Logic for None handling when no component exists

## Out of Scope

- Starlette integration and HTTP request/response handling
- Full hierarchy navigation beyond single parent link
- Advanced CSS styling or layout frameworks
- Reusable component extraction from default layout
- Error pages or fallback rendering for failed stories
- Hot reload or live preview functionality
- CLI integration or command-line rendering
- Integration with the web-based component browser
- Performance optimization or caching
- Support for multiple template formats beyond tdom
