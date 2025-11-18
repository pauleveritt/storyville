# Specification: Large-Scale Example with Build Performance Instrumentation

## Goal
Create a large-scale example (examples.huge) with 300 stories and build performance instrumentation to enable performance testing and provide visibility into build process characteristics.

## User Stories
- As a developer, I want to test Storytime performance at scale so that I can identify bottlenecks before production use
- As a maintainer, I want to track build phase timing so that I can detect performance regressions

## Specific Requirements

**Large-Scale Example Structure (examples.huge)**
- Create directory structure under examples/huge/ following existing examples pattern
- Generate 10 sections with realistic design system names (Forms, Navigation, Feedback, Layout, Data Display, Overlays, Media, Typography, Inputs, Controls)
- Each section contains 10 components with design system names (Button, Card, Alert, Modal, Dropdown, Tooltip, Badge, Avatar, Checkbox, Input, etc.)
- Each component has 3 story variations using simple prop changes (default, disabled, loading states)
- Total output: 300 stories (10 sections × 10 components × 3 variations)
- Follow existing pattern: Site (stories.py with this_site), Section (stories.py with this_section), Subject (stories.py with this_subject)

**Simple Component Implementation**
- Components are basic dataclasses with simple props (text, variant, state, etc.)
- Each component renders using tdom t-strings returning basic HTML (div/button/span with text and classes)
- Follow Button component pattern from examples.complete: dataclass with __call__ returning html(t"...")
- Keep component logic minimal to focus on scale testing, not functionality

**Build Phase Instrumentation**
- Add timing measurement for 3 distinct build phases in build.py
- Phase 1 (Reading): measure time in make_site() call to load content from filesystem
- Phase 2 (Rendering): measure time for all view rendering (_write_html calls for Site/Section/Subject/Story)
- Phase 3 (Writing): measure time for file I/O operations (path.write_text and copytree)
- Use time.perf_counter() for high-resolution timing measurements
- Instrumentation integrated into build_site() function without breaking existing behavior

**Python Logging Integration**
- Import and configure Python's standard logging module in build.py
- Create logger instance: logger = logging.getLogger(__name__)
- Log phase timing metrics at INFO level after each phase completes
- Format: "Phase [name]: completed in {duration:.2f}s"
- Log total build time at INFO level: "Build completed in {total:.2f}s"
- Logging should integrate with existing CLI logging configuration from __main__.py

**Performance Testing with pytest-benchmark**
- Add pytest-benchmark to dev dependencies in pyproject.toml
- Create test_huge_example() in tests/test_examples.py for smoke testing
- Smoke test verifies: build completes successfully, expected directory count matches (~300 story dirs), no errors during build
- Create test_huge_build_performance() using benchmark fixture from pytest-benchmark
- Performance test measures total build time using benchmark(build_site, "examples.huge", tmp_path)
- Keep tests fast by running smoke test once per session, performance test tracks baseline without exhaustive validation

**Integration with Existing Build System**
- Instrumentation code added to existing build_site() function in src/storytime/build.py
- No changes to build_site() function signature or return type
- No changes to existing examples or their tests
- Logging output should appear when running storytime build or storytime serve commands

## Existing Code to Leverage

**examples.complete structure**
- Use Site/Section/Subject/Story hierarchy pattern from examples/complete/
- Follow this_site(), this_section(), this_subject() function naming from examples.complete
- Story definitions use Story(props={}, title=None, description=None) pattern from complete example
- Target inheritance pattern where Subject.target is inherited by all Stories unless overridden

**Button component implementation**
- Replicate dataclass pattern with text and variant props from examples/complete/components/button/button.py
- Use __call__ method returning html(t"...") with tdom t-strings
- Keep component implementations minimal like Button example (simple div/button/span rendering)

**build.py structure**
- Extend build_site() function from src/storytime/build.py without changing signature
- Use existing _write_html() helper for file writing operations
- Follow existing pattern of walking site.items tree for sections/subjects/stories

**test_examples.py patterns**
- Add test functions to existing tests/test_examples.py file
- Use make_site() pattern from existing example tests for loading examples.huge
- Follow session-scoped fixture pattern from test_build.py for one-time build in smoke test
- Use structural pattern matching (match/case) for traversing tree as seen in test_complete_example_structure()

**Logging configuration from __main__.py**
- Use logging.basicConfig() pattern from src/storytime/__main__.py serve command
- Logger instance uses logging.getLogger(__name__) pattern seen in existing storytime modules
- INFO level logging with format string pattern from __main__.py

## Out of Scope
- Memory usage tracking or profiling
- Performance visualization, graphs, or dashboards
- Testing different scales (100 vs 1000 stories variants)
- Optimizing the build process itself based on instrumentation data
- Fully functional interactive components (only simple showcase components)
- Elaborate story scenarios or complex prop variations
- Toggle flags or CLI options for enabling/disabling instrumentation
- Exhaustive testing of all 300 individual stories
- Custom template usage in examples.huge (use default StoryView layout)
- Static asset copying performance measurement beyond what's already in Phase 3
