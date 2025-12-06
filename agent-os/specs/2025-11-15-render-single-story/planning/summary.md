# Spec Summary: Render a Single Story

## Overview

This spec implements the fundamental rendering mechanism for individual Story instances, providing both custom template
support and a sensible default layout. This is foundational work for the web-based component browser.

## Key Deliverables

### 1. View Protocol (`src/storyville/models.py`)

- NEW file
- Defines Protocol with `__call__(self) -> Element` signature
- Enables structural typing for view classes

### 2. Story Class Updates (`src/storyville/story/models.py`)

- MODIFIED file
- Update `instance` property to return `Element` with type guard

### 3. StoryView (`src/storyville/story/views.py`)

- NEW file
- Dataclass implementing View Protocol
- Two rendering modes:
    - Custom template mode (when Story.template exists)
    - Default layout mode (when Story.template is None)

### 4. Comprehensive Tests (`tests/story/test_story_view.py`)

- NEW file
- Test both rendering modes
- Verify type safety
- Use aria-testing for semantic validation

## Critical Requirements

**MUST HAVE:**

- View Protocol with exact signature
- StoryView as dataclass with `story: Story` field
- Two distinct rendering modes with correct conditional logic
- Type guard in Story.instance property
- Default layout showing title, props, instance, and parent link
- No error handling - let exceptions propagate
- No Starlette integration

**MUST NOT HAVE:**

- Reusable component extraction
- Advanced layout features
- Full hierarchy navigation
- Custom error handling

## Success Criteria

- All quality checks pass: `just test`, `just typecheck`, `just fmt`
- StoryView renders stories correctly in both modes
- Type safety verified through static analysis and runtime guards
- Tests provide comprehensive coverage using aria-testing

## Roadmap Impact

Directly enables:

- Roadmap Item #1: Component Rendering System
- Roadmap Item #2: Story Definition API
- Roadmap Item #3: Web-Based Component Browser (foundation)

## Next Steps

After this spec is implemented, future specs can:

1. Integrate StoryView with Starlette routes
2. Extract reusable layout components
3. Add styling and theming
4. Enhance navigation capabilities
