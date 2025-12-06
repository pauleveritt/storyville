# Spec Initialization

**Created:** 2025-11-18
**Status:** Requirements gathering in progress

## Initial Description

Add assertion capabilities to Storyville stories that run in the **StoryView UI** during development, displaying **pass/fail badges** in the rendered HTML page.

### Key Design Decision

Assertions should execute in the StoryView component (the browser-based story renderer), not just in pytest. This means:

- Assertions run during hot-reload development in the browser
- Visual feedback (badges) shows pass/fail status directly in the rendered page
- Developers see assertion results immediately as they code, without running pytest

This is a significant architectural decision that affects:
- Where assertions execute (browser context vs test context)
- When they execute (every render vs on-demand)
- How errors are displayed (visual badges vs test output)
- Performance considerations (assertions running on every hot-reload)
- Safety/sandboxing (assertions running in production-like UI context)

### Previously Discussed

Earlier conversation mentioned:
- Singular/plural field naming for assertions (`assertion` vs `assertions`)
- Integration with pytest for automated testing

## Context

This spec is being created for Storyville, a component-driven development platform for Python 3.14+.

**Product Context:**
- Framework-independent component development system
- Uses tdom for templating, Starlette for web framework
- Supports hot-reload development server with subinterpreter pool
- Story-based development: Sites → Sections → Subjects → Stories

**Current State:**
- Hot reload development server: Complete
- Component organization system: Complete
- Next priorities: Story-to-test integration, component browser, CLI workflow
