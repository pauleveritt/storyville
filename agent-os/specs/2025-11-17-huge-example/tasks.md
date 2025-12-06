# Task Breakdown: Large-Scale Example with Build Performance Instrumentation

## Overview
Total Tasks: 4 major task groups with 36 sub-tasks
Target: Create examples.huge with 300 stories and comprehensive build performance instrumentation

## Task List

### Task Group 1: Example Package Structure and Site Hierarchy
**Dependencies:** None

- [x] 1.0 Complete examples.huge package structure
  - [x] 1.1 Write 2-4 focused tests for Site structure
    - Test site loads successfully with title
    - Test site has 10 sections
    - Verify section names match expected design system categories
  - [x] 1.2 Create examples/huge/ directory structure
    - Follow examples/complete/ directory pattern
    - Create root __init__.py file
  - [x] 1.3 Create examples/huge/stories.py with this_site()
    - Return Site(title="Huge Scale Example")
    - Follow pattern from examples/complete/stories.py
  - [x] 1.4 Create 10 section directories with realistic names
    - forms/
    - navigation/
    - feedback/
    - layout/
    - data_display/
    - overlays/
    - media/
    - typography/
    - inputs/
    - controls/
  - [x] 1.5 Create stories.py with this_section() in each section directory
    - Section(title="Forms", description="Form components")
    - Section(title="Navigation", description="Navigation components")
    - Section(title="Feedback", description="Feedback components")
    - Section(title="Layout", description="Layout components")
    - Section(title="Data Display", description="Data display components")
    - Section(title="Overlays", description="Overlay components")
    - Section(title="Media", description="Media components")
    - Section(title="Typography", description="Typography components")
    - Section(title="Inputs", description="Input components")
    - Section(title="Controls", description="Control components")
  - [x] 1.6 Ensure Site structure tests pass
    - Run ONLY the 2-4 tests written in 1.1
    - Verify sections load correctly
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-4 tests written in 1.1 pass
- Site loads successfully with 10 sections
- Section names are realistic design system categories
- Directory structure follows existing examples pattern

### Task Group 2: Component Implementation and Subject Layer
**Dependencies:** Task Group 1

- [x] 2.0 Complete component and subject layer
  - [x] 2.1 Write 2-4 focused tests for component rendering
    - Test component instances render correctly
    - Test component props are applied
    - Verify basic HTML structure
  - [x] 2.2 Create 10 simple components per section (100 total components)
    - **Forms section:** FormButton, FormInput, FormTextarea, FormSelect, FormCheckbox, FormRadio, FormSwitch, FormSlider, FormDatePicker, FormFileUpload
    - **Navigation section:** NavBar, NavMenu, NavBreadcrumb, NavPagination, NavTabs, NavSidebar, NavSteps, NavLink, NavDropdown, NavFooter
    - **Feedback section:** FeedbackAlert, FeedbackToast, FeedbackModal, FeedbackBanner, FeedbackNotification, FeedbackProgress, FeedbackSpinner, FeedbackSkeleton, FeedbackBadge, FeedbackTooltip
    - **Layout section:** LayoutContainer, LayoutGrid, LayoutStack, LayoutSpacer, LayoutDivider, LayoutCard, LayoutPanel, LayoutSection, LayoutHeader, LayoutFooter
    - **Data Display section:** DataTable, DataList, DataCard, DataTag, DataAvatar, DataTimeline, DataTree, DataChart, DataStat, DataCode
    - **Overlays section:** OverlayModal, OverlayDrawer, OverlayPopover, OverlayTooltip, OverlayDialog, OverlayMenu, OverlayDropdown, OverlaySheet, OverlaySidebar, OverlayBackdrop
    - **Media section:** MediaImage, MediaVideo, MediaAudio, MediaIcon, MediaGallery, MediaCarousel, MediaThumbnail, MediaPlayer, MediaEmbed, MediaUploader
    - **Typography section:** TypoHeading, TypoText, TypoLabel, TypoCode, TypoQuote, TypoList, TypoLink, TypoParagraph, TypoEmphasis, TypoMark
    - **Inputs section:** InputText, InputNumber, InputEmail, InputPassword, InputSearch, InputURL, InputTel, InputDate, InputTime, InputColor
    - **Controls section:** ControlButton, ControlIconButton, ControlToggle, ControlCheckbox, ControlRadio, ControlSwitch, ControlSlider, ControlRating, ControlSegmented, ControlChip
  - [x] 2.3 Implement components as simple dataclasses
    - Follow Button pattern from examples/complete/components/button/button.py
    - Props: text (str), variant (str), state (str)
    - __call__() method returning html(t"...")
    - Render as basic HTML: div/button/span with text and class attribute
  - [x] 2.4 Create component directories and .py files
    - Each component in its own .py file within section directory
    - Example: examples/huge/forms/form_button/form_button.py
    - Keep implementations minimal (8-10 lines per component)
  - [x] 2.5 Create stories.py with this_subject() for each component
    - Subject(title="[Component Name]", description="...", target=[Component])
    - Example: Subject(title="Form Button", description="Button for forms", target=FormButton)
    - Follow pattern from examples/complete/components/button/stories.py
  - [x] 2.6 Add 3 story variations per component (300 stories total)
    - Story 1: Default state (props=dict(text="Default", variant="primary", state="default"))
    - Story 2: Disabled state (props=dict(text="Disabled", variant="secondary", state="disabled"))
    - Story 3: Loading state (props=dict(text="Loading", variant="primary", state="loading"))
    - Follow Story pattern from examples.complete
  - [x] 2.7 Ensure component tests pass
    - Run ONLY the 2-4 tests written in 2.1
    - Verify critical component behaviors work
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-4 tests written in 2.1 pass
- 100 components created across 10 sections
- Each component has 3 story variations
- Total of 300 stories successfully created
- Components follow dataclass pattern with __call__() method

### Task Group 3: Build Performance Instrumentation
**Dependencies:** Task Groups 1-2

- [x] 3.0 Complete build instrumentation
  - [x] 3.1 Write 2-4 focused tests for instrumentation
    - Test logging output contains phase timings
    - Test all 3 phases are measured
    - Verify logging format matches specification
  - [x] 3.2 Add logging imports to build.py
    - Import logging module
    - Create logger: logger = logging.getLogger(__name__)
  - [x] 3.3 Add timing imports to build.py
    - Import time.perf_counter for high-resolution timing
  - [x] 3.4 Implement Phase 1 (Reading) instrumentation
    - Add start_reading = time.perf_counter() before make_site() call
    - Add end_reading = time.perf_counter() after make_site() call
    - Calculate reading_duration = end_reading - start_reading
    - Log: logger.info(f"Phase Reading: completed in {reading_duration:.2f}s")
  - [x] 3.5 Implement Phase 2 (Rendering) instrumentation
    - Add start_rendering = time.perf_counter() before view rendering loop
    - Add end_rendering = time.perf_counter() after all _write_html calls
    - Calculate rendering_duration = end_rendering - start_rendering
    - Log: logger.info(f"Phase Rendering: completed in {rendering_duration:.2f}s")
    - Measure time for SiteView, AboutView, DebugView, and all Section/Subject/Story views
  - [x] 3.6 Implement Phase 3 (Writing) instrumentation
    - Add start_writing = time.perf_counter() before path.write_text operations
    - Track time for all file I/O including copytree for static assets
    - Add end_writing = time.perf_counter() after all writes complete
    - Calculate writing_duration = end_writing - start_writing
    - Log: logger.info(f"Phase Writing: completed in {writing_duration:.2f}s")
  - [x] 3.7 Add total build time logging
    - Calculate total_duration = reading_duration + rendering_duration + writing_duration
    - Log: logger.info(f"Build completed in {total_duration:.2f}s")
  - [x] 3.8 Integrate with existing logging configuration
    - Verify logging works with logging.basicConfig() from __main__.py
    - Test logging output appears in storyville build and storyville serve commands
    - Use INFO level for all timing logs
  - [x] 3.9 Ensure instrumentation tests pass
    - Run ONLY the 2-4 tests written in 3.1
    - Verify logging output is correct
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-4 tests written in 3.1 pass
- All 3 build phases have timing instrumentation
- Logging output follows specified format
- No changes to build_site() function signature
- Logging appears in CLI commands (build/serve)

### Task Group 4: Performance Testing and Integration
**Dependencies:** Task Groups 1-3

- [x] 4.0 Complete performance testing and integration
  - [x] 4.1 Add pytest-benchmark to pyproject.toml
    - Add to [dependency-groups] dev section
    - Version: pytest-benchmark>=4.0.0
  - [x] 4.2 Install pytest-benchmark
    - Run: uv sync
  - [x] 4.3 Write smoke test for examples.huge
    - Create test_huge_example() in tests/test_examples.py
    - Use make_site("examples.huge") to load the example
    - Verify site has 10 sections
    - Verify first section has 10 subjects
    - Verify first subject has 3 stories
    - Use structural pattern matching (match/case) for tree traversal
  - [x] 4.4 Write build smoke test for examples.huge
    - Create test_huge_build_smoke() in tests/test_examples.py
    - Build site to tmp_path using build_site("examples.huge", tmp_path)
    - Verify build completes without errors
    - Count output directories: expect ~311 total (1 site + 10 sections + 100 subjects + 300 stories)
    - Verify index.html exists in key locations
  - [x] 4.5 Write performance benchmark test
    - Create test_huge_build_performance() in tests/test_examples.py
    - Use pytest-benchmark's benchmark fixture
    - Measure: benchmark(build_site, "examples.huge", tmp_path)
    - Track total build time for performance regression detection
    - Keep test focused on timing, not validation
  - [x] 4.6 Run all examples.huge tests
    - Run test_huge_example() to verify structure
    - Run test_huge_build_smoke() to verify build works
    - Run test_huge_build_performance() to establish baseline
    - Verify all tests pass
  - [x] 4.7 Verify integration with existing examples
    - Run existing examples tests (test_complete_example_structure, etc.)
    - Ensure no regressions in other examples
    - Verify examples.huge doesn't break existing functionality
  - [x] 4.8 Test CLI integration
    - Run: storyville build examples.huge /tmp/test-huge
    - Verify logging output shows phase timings
    - Verify build completes successfully
    - Check output directory structure
  - [x] 4.9 Run full test suite
    - Execute: just test
    - Verify all tests pass including new examples.huge tests
    - Confirm no regressions in existing tests
  - [x] 4.10 Run quality checks
    - Execute: just typecheck (verify type hints are correct)
    - Execute: just fmt (verify formatting is correct)
    - Fix any issues identified by quality checks

**Acceptance Criteria:**
- pytest-benchmark added to dependencies
- Smoke test verifies examples.huge loads and builds correctly
- Performance benchmark establishes baseline timing
- CLI commands show instrumentation logging
- All quality checks pass (test, typecheck, fmt)
- No regressions in existing examples or tests

## Execution Order

Recommended implementation sequence:
1. **Task Group 1**: Example Package Structure and Site Hierarchy
   - Establish the foundation with Site and 10 Sections
   - Creates the directory structure for the large-scale example
   - Validates the high-level hierarchy works

2. **Task Group 2**: Component Implementation and Subject Layer
   - Implement 100 components across 10 sections
   - Create 300 stories (3 variations per component)
   - Largest task group - creates the bulk of the content

3. **Task Group 3**: Build Performance Instrumentation
   - Add timing measurement for 3 build phases
   - Integrate Python logging module
   - Does not require examples.huge to be complete, but easier to test with large dataset

4. **Task Group 4**: Performance Testing and Integration
   - Add pytest-benchmark for performance tracking
   - Create smoke tests and performance benchmarks
   - Verify integration and run quality checks

## Notes

- **Test Writing Strategy**: Each task group writes 2-4 focused tests at the beginning, then runs ONLY those tests at the end. This prevents the test suite from becoming a bottleneck during development.

- **Component Organization**: The 100 components are organized by design system category (Forms, Navigation, Feedback, etc.) to create a realistic large-scale example that mirrors real-world usage.

- **Story Variations**: Each component has 3 simple story variations (default, disabled, loading) to demonstrate different states without complex logic.

- **Instrumentation Integration**: The build instrumentation is integrated directly into the existing build_site() function without changing its signature, ensuring backward compatibility.

- **Performance Testing**: pytest-benchmark is used to establish a baseline for build performance, enabling detection of performance regressions in future changes.

- **Quality Standards**: All code must pass type checking (just typecheck) and formatting (just fmt) before completion, following the project's CLAUDE.md standards.
