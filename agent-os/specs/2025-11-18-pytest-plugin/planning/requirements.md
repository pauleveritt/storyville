# Spec Requirements: pytest Plugin for Story Assertions

## Initial Description
"pytest plugin. Write a plugin that does test discovery on stories with assertions.

I also want some control in a config settings. Would be great if you didn't have to write any tests manually. Make the DX great: good names for tests, good reporting on failures. Decide if making a tree is necessary."

## Requirements Discussion

### First Round Questions

**Q1: Test Discovery Mechanism** - I'm assuming the plugin should scan for all story files in common directories (like `examples/`, `stories/`, `tests/`). Should it auto-discover stories everywhere, or only in locations you explicitly point it to via config?
**Answer:** Only locations that you point at via config option (not scan everywhere)

**Q2: Config Settings** - For configuration, I'm thinking we could use `[tool.storyville.pytest]` in pyproject.toml with settings like `story_paths`, `enabled`, `run_assertions_on_collect`. Does that match your expectations?
**Answer:** Good (approved the proposed `[tool.storyville.pytest]` settings)

**Q3: Automatic Test Generation** - When you say "wouldn't have to write any tests manually", I assume you want the plugin to use pytest's collection hooks to automatically generate test items for each story that has assertions. Is that correct?
**Answer:** Yes (use pytest collection hooks)

**Q4: Test Naming Conventions** - For good DX with test names, I'm thinking something like: `test_story[site.section.subject.story_name::assertion_name]` so it's clear which story and which specific assertion failed. Does this naming pattern work for you?
**Answer:** Yes (use the proposed pattern: `test_story[site.section.subject.story_name::assertion_name]`)

**Q5: Failure Reporting Format** - For good failure reporting, should we include: (1) The story's rendered HTML, (2) The assertion that failed, (3) The error message/traceback, (4) Story metadata (props, etc.)?
**Answer:** Yes to all listed items, PLUS include diffs (visual diffs)

**Q6: Tree Structure Decision** - Regarding "making a tree", are you asking whether test results should be organized hierarchically (site → section → subject → story) or flattened? My assumption is a flat structure would be simpler and work better with pytest's output.
**Answer:** Flatten (not hierarchical)

**Q7: Integration with Fixtures** - Should the plugin allow manual test writing as well (using pytest fixtures to access stories), or is it ONLY for automatic test generation from assertions?
**Answer:** Yes to fixtures for manual testing, AND write some example tests that demonstrate this manual testing capability

**Q8: Performance Considerations** - Should the plugin support running story assertions in parallel (pytest-xdist), or should each story be rendered independently for isolation?
**Answer:** Yes to parallel capability and flag

**Q9: Assertion Result Handling** - Since stories now cache `assertion_results` after rendering, should the plugin: (a) re-run assertions fresh for each test, (b) use cached results if available, or (c) always render fresh for testing?
**Answer:** Yes (need clarification - likely means fresh rendering)

**Q10: Out of Scope** - Should the following be excluded from this plugin: (1) visual regression testing (screenshot comparison), (2) accessibility testing beyond what's in assertions, (3) mutation testing, (4) coverage reporting?
**Answer:** Yes to all of those (exclude all 4 items: visual regression, accessibility beyond assertions, mutation testing, coverage reporting)

### Existing Code to Reference

No similar existing features identified for reference.

### Follow-up Questions

**Follow-up 1:** For Question 9 about assertion result handling - you answered "Yes" but I need clarification: Should the plugin (a) re-run assertions fresh for each test, (b) use cached results if available, or (c) always render the story fresh for testing to ensure test isolation?
**Answer:** Option C - Always render the story completely fresh during testing to ensure proper test isolation

**Follow-up 2:** For the config `story_paths` setting - what should the default paths be? Just `["examples/"]`? Or should it include other directories by default?
**Answer:** `["examples/"]` - Just examples directory as default

**Follow-up 3:** For parallel execution - should this integrate with pytest-xdist (the standard pytest parallel plugin), or do you want a custom parallel implementation?
**Answer:** Integrate with pytest-xdist (users run `pytest -n auto`)

**Follow-up 4:** For visual diffs in failure reporting - what format would you like? HTML diff? Text diff? Side-by-side comparison? Should it show the diff of the rendered HTML?
**Answer:** Option B - Unified text diff of rendered HTML

**Follow-up 5:** For the manual test examples you requested - where should these example tests live? In the main `tests/` directory, or in a separate location like `examples/pytest_examples/`?
**Answer:** `tests/` - Example tests should live in the main tests directory alongside other tests

**Follow-up 6:** Should this be distributed as a separate pytest plugin package (like `pytest-storyville`), or built directly into the storyville core package?
**Answer:** Built directly into storyville core as an optional pytest plugin (not a separate package)

**Follow-up 7:** Are there any specific pytest version requirements we should target? (I see pytest 9.0.0+ is currently used)
**Answer:** Current (maintain pytest 9.0.0+ as minimum)

## Visual Assets

### Files Provided:
No visual assets provided.

### Visual Insights:
No visual assets to analyze.

## Requirements Summary

### Functional Requirements
- **Automatic test discovery**: Plugin discovers stories with assertions from configured paths only
- **Configuration-based discovery**: Use `[tool.storyville.pytest]` in pyproject.toml with `story_paths` setting
- **Default story paths**: `["examples/"]` as the default search location
- **Test generation**: One pytest test item per assertion in each discovered story
- **Test naming**: `test_story[site.section.subject.story_name::assertion_name]` format
- **Fresh rendering**: Always render stories completely fresh during testing for proper isolation
- **Flat structure**: Test results organized flatly, not hierarchically
- **Rich failure reporting**: Include rendered HTML, assertion details, error traceback, story metadata, and unified text diffs
- **Parallel execution**: Integration with pytest-xdist (users run `pytest -n auto`)
- **Dual testing modes**: Support both automatic test generation AND manual test writing via fixtures
- **Example tests**: Provide example tests in `tests/` directory demonstrating manual fixture usage
- **Core integration**: Built directly into storyville package as optional pytest plugin

### Reusability Opportunities
- Existing Story model with assertions and assertion_results fields (`/src/storyville/story/models.py`)
- Current pytest infrastructure and test directory structure (`/tests/`)
- Existing CLI flag `--with-assertions` pattern for enabling/disabling features
- Type definitions: `AssertionCallable`, `AssertionResult` already defined

### Scope Boundaries

**In Scope:**
- Pytest plugin using collection hooks for automatic test generation
- Configuration system via `[tool.storyville.pytest]` in pyproject.toml
- Config-based story path discovery (default: `["examples/"]`)
- Test naming conventions: `test_story[site.section.subject.story_name::assertion_name]`
- Fresh story rendering per test for isolation
- Flat test structure (not hierarchical)
- Rich failure reporting with unified text diffs of rendered HTML
- pytest-xdist integration for parallel execution
- Fixtures for manual test writing
- Example tests demonstrating manual testing approach
- Integration as optional plugin within storyville core package

**Out of Scope:**
- Visual regression testing (screenshot comparison)
- Accessibility testing beyond what's defined in story assertions
- Mutation testing
- Coverage reporting specific to stories
- Separate package distribution (will be part of core)
- Hierarchical test organization
- Auto-discovery of all Python files (only configured paths)

### Technical Considerations
- **pytest integration**: Use pytest 9.0.0+ collection hooks (`pytest_collect_file`, `pytest_generate_tests`, or custom Item/Collector classes)
- **Python compatibility**: Must work with Python 3.14+ type hints and modern syntax (structural pattern matching, PEP 695 generics, etc.)
- **Story rendering**: Leverage existing Story model but ensure fresh rendering for each test (don't use cached `assertion_results`)
- **Configuration**: Follow existing pyproject.toml patterns with `[tool.storyville.pytest]` section
- **Parallel safety**: Ensure compatibility with pytest-xdist for parallel test execution
- **Failure output**: Generate unified text diffs using Python's difflib for rendered HTML comparison
- **Plugin registration**: Use pytest entry points to register as optional plugin within core package
- **Test isolation**: Each test should independently render its story to avoid state sharing
- **Fixture design**: Provide fixtures that allow manual access to stories for custom test writing

### Key Design Decisions

1. **Config-based discovery**: Only scan paths specified in `[tool.storyville.pytest]` config, defaulting to `["examples/"]`
2. **Automatic test generation**: Use pytest collection hooks to generate test items automatically
3. **Flat structure**: Tests organized flatly for better pytest output compatibility
4. **Fresh rendering**: Always render stories fresh during tests (ignore cached results)
5. **pytest-xdist integration**: Leverage standard pytest parallel plugin rather than custom implementation
6. **Unified text diff**: Use simple text diff format for failure reporting (not HTML/visual diffs)
7. **Core integration**: Built into storyville package as optional plugin (not separate `pytest-storyville` package)
8. **Dual modes**: Support both automatic generation and manual fixture-based testing
9. **Example location**: Example tests in main `tests/` directory alongside other tests
10. **Version requirements**: Maintain pytest 9.0.0+ as minimum supported version
