# Task Breakdown: Better Examples for Storytime

## Overview
Total Task Groups: 6
Total Tasks: ~30-40 individual tasks

This breakdown implements comprehensive examples demonstrating all Story variation patterns (6 variations) across 5 example categories (minimal, complete, inheritance, templates, no_sections) with full test coverage using aria-testing.

## Task List

### Phase 1: Update Existing Examples

#### Task Group 1: Update Minimal Example
**Dependencies:** None

- [x] 1.0 Update minimal example with documentation
  - [x] 1.1 Fix function name in `examples/minimal/stories.py`
    - Change function to use `this_site()` (currently correct)
    - Verify it returns `Site(title="Minimal Site")`
  - [x] 1.2 Create `examples/minimal/README.md`
    - Overview: "Demonstrates the most basic Storytime usage"
    - Structure: Describe one Section, one Subject, one Story with props only
    - Key Features: Single component (Heading), props inheritance from Subject target
    - Keep under 20 lines
  - [x] 1.3 Verify existing structure is correct
    - Verify `components/heading/stories.py` defines Subject with target=Heading
    - Verify `components/heading/heading.py` has simple Heading component
    - No changes needed to component or Subject

**Acceptance Criteria:**
- Function name is correct in stories.py
- README.md exists and documents minimal example features
- Existing structure verified as matching spec requirements

#### Task Group 2: Update No Sections Example
**Dependencies:** None

- [x] 2.0 Update no_sections example with documentation
  - [x] 2.1 Verify no_sections structure
    - Confirm Subject is directly under Site (no Section in tree)
    - Verify `examples/no_sections/components/stories.py` exists
    - Check that hierarchy is Site → Subject (no Section layer)
  - [x] 2.2 Create `examples/no_sections/README.md`
    - Overview: "Demonstrates that Sections are optional in the hierarchy"
    - Structure: Site directly contains Subject without Section layer
    - Key Features: Flat structure, direct Site-to-Subject relationship
    - Keep under 20 lines

**Acceptance Criteria:**
- Structure verified as Site → Subject (no Section)
- README.md exists and documents no_sections pattern
- Example demonstrates optional nature of Sections

### Phase 2: Create New Examples

#### Task Group 3: Complete Example (All Optional Fields)
**Dependencies:** Task Groups 1-2

- [x] 3.0 Create complete example demonstrating all optional fields
  - [x] 3.1 Write 2-5 focused tests in `tests/test_examples.py`
    - Test `test_complete_example_structure()` validates Site/Section/Subject hierarchy
    - Test `test_complete_example_all_fields()` verifies title/description on all models
    - Test `test_complete_example_story_variations()` checks 3 Story patterns
    - Limit to 2-5 tests covering critical complete example behaviors
  - [x] 3.2 Create `examples/complete/` directory structure
    - Create `examples/complete/stories.py` with Site(title="Complete Example")
    - Create `examples/complete/components/` directory
    - Create `examples/complete/components/stories.py` with Section(title="...", description="...")
    - Create `examples/complete/components/button/` directory
  - [x] 3.3 Create Button component at `examples/complete/components/button/button.py`
    - Dataclass with `text: str` and `variant: str` fields (2 props max)
    - Implement `__call__(self) -> Node` returning `html(t"<button class={self.variant}>{self.text}</button>")`
    - Follow Heading component pattern from minimal example
  - [x] 3.4 Create `examples/complete/components/button/stories.py`
    - Define Subject(title="Button Component", description="...", target=Button)
    - Define 3 Stories:
      - Story 1: props only (text="Click", variant="primary") - minimal
      - Story 2: Story(title="Custom Title", description="...", props={"text": "...", "variant": "..."})
      - Story 3: Different props for same component (text="Cancel", variant="secondary")
  - [x] 3.5 Create `examples/complete/README.md`
    - Overview: "Shows all optional Site/Section/Subject/Story fields populated"
    - Structure: Full hierarchy with all optional fields
    - Key Features: Site title, Section title/desc, Subject title/desc/target, 3 Story variations
    - Keep under 20 lines
  - [x] 3.6 Run complete example tests only
    - Run ONLY the 2-5 tests written in 3.1
    - Verify Site loads with `make_site("examples.complete")`
    - Verify tree structure is correct
    - Do NOT run entire test suite

**Acceptance Criteria:**
- The 2-5 tests written in 3.1 pass
- Complete example demonstrates all optional fields
- Button component is simple (2 props max)
- 3 Story variations demonstrate different patterns
- README documents what complete example shows

#### Task Group 4: Inheritance Example (Field Inheritance Patterns)
**Dependencies:** Task Groups 1-3

- [ ] 4.0 Create inheritance example demonstrating field inheritance
  - [ ] 4.1 Write 2-5 focused tests in `tests/test_examples.py`
    - Test `test_inheritance_example_target_inheritance()` verifies Story inherits target from Subject
    - Test `test_inheritance_example_title_generation()` checks auto-generated Story titles
    - Test `test_inheritance_example_target_override()` validates Story can override target
    - Limit to 2-5 tests covering critical inheritance behaviors
  - [ ] 4.2 Create `examples/inheritance/` directory structure
    - Create `examples/inheritance/stories.py` with Site(title="Inheritance Example")
    - Create `examples/inheritance/components/` directory
    - Create `examples/inheritance/components/stories.py` with Section
    - Create `examples/inheritance/components/card/` directory
  - [ ] 4.3 Create Card component at `examples/inheritance/components/card/card.py`
    - Dataclass with `title: str` and `text: str` fields
    - Implement `__call__(self) -> Node` returning `html(t"<div><h2>{self.title}</h2><p>{self.text}</p></div>")`
  - [ ] 4.4 Create alternate Badge component at `examples/inheritance/components/card/badge.py`
    - Dataclass with `count: int` field
    - Implement `__call__(self) -> Node` returning `html(t"<span>{self.count}</span>")`
    - Used to demonstrate target override
  - [ ] 4.5 Create `examples/inheritance/components/card/stories.py`
    - Define Subject(target=Card) with NO title (will use package_path)
    - Define Stories demonstrating inheritance:
      - Story 1: No title (inherits auto-generated from Subject), props for Card
      - Story 2: Explicit title="Custom Card Title", props for Card
      - Story 3: target=Badge (overrides Subject's target), props for Badge
      - Story 4: No title (inherits), different Card props
  - [ ] 4.6 Create `examples/inheritance/README.md`
    - Overview: "Demonstrates field inheritance patterns across the hierarchy"
    - Structure: Subject with target, Stories with various inheritance patterns
    - Key Features: Target inheritance, title generation, target override
    - Explain inheritance rules
    - Keep under 20 lines
  - [ ] 4.7 Run inheritance example tests only
    - Run ONLY the 2-5 tests written in 4.1
    - Use structural pattern matching to verify target inheritance
    - Verify title auto-generation logic
    - Do NOT run entire test suite

**Acceptance Criteria:**
- The 2-5 tests written in 4.1 pass
- Stories demonstrate target inheritance from Subject
- Stories demonstrate title auto-generation
- One Story demonstrates target override
- README explains inheritance rules
- Tests use structural pattern matching for tree traversal

#### Task Group 5: Templates Example (Custom Template Usage)
**Dependencies:** Task Groups 1-4

- [ ] 5.0 Create templates example demonstrating custom templates
  - [ ] 5.1 Write 2-5 focused tests in `tests/test_examples.py`
    - Test `test_templates_example_default_template()` verifies Story without template uses default layout
    - Test `test_templates_example_custom_template()` validates Story with custom template
    - Test `test_templates_example_template_override()` checks template completely overrides rendering
    - Limit to 2-5 tests covering critical template behaviors
  - [ ] 5.2 Create `examples/templates/` directory structure
    - Create `examples/templates/stories.py` with Site
    - Create `examples/templates/components/` directory
    - Create `examples/templates/components/stories.py` with Section
    - Create `examples/templates/components/alert/` directory
  - [ ] 5.3 Create Alert component at `examples/templates/components/alert/alert.py`
    - Dataclass with `message: str` field
    - Implement `__call__(self) -> Node` returning `html(t"<div role='alert'>{self.message}</div>")`
  - [ ] 5.4 Create custom template function
    - Define `custom_alert_template()` function in stories.py
    - Returns `html(t"<div class='custom'><h1>Custom Template</h1><p>Full control</p></div>")`
    - Demonstrates complete rendering override using tdom t-string
  - [ ] 5.5 Create `examples/templates/components/alert/stories.py`
    - Define Subject(target=Alert)
    - Define 2 Stories:
      - Story 1: No template (uses default StoryView layout), props for Alert
      - Story 2: template=custom_alert_template (overrides all rendering)
  - [ ] 5.6 Create `examples/templates/README.md`
    - Overview: "Demonstrates custom template usage for Stories"
    - Structure: Subject with 2 Stories, one with template, one without
    - Key Features: Default StoryView layout vs custom template override
    - Explain when to use custom templates
    - Keep under 20 lines
  - [ ] 5.7 Run templates example tests only
    - Run ONLY the 2-5 tests written in 5.1
    - Verify StoryView rendering for Story without template
    - Verify custom template rendering for Story with template
    - Use aria-testing to validate both rendering modes
    - Do NOT run entire test suite

**Acceptance Criteria:**
- The 2-5 tests written in 5.1 pass
- Default template Story uses StoryView layout
- Custom template Story uses custom rendering
- Template function demonstrates full control using tdom t-string
- README explains template override behavior
- Tests verify both rendering modes with aria-testing

### Phase 3: Comprehensive Test Coverage

#### Task Group 6: Test Review & Integration Testing
**Dependencies:** Task Groups 1-5

- [ ] 6.0 Review and complete comprehensive test coverage
  - [ ] 6.1 Review existing tests from Task Groups 3-5
    - Review the 2-5 tests written for complete example (Task 3.1)
    - Review the 2-5 tests written for inheritance example (Task 4.1)
    - Review the 2-5 tests written for templates example (Task 5.1)
    - Total existing tests: approximately 6-15 tests
  - [ ] 6.2 Write comprehensive integration tests for all examples
    - Add `test_minimal_example()` - load Site, traverse tree, test all views
    - Add `test_no_sections_example()` - verify Site → Subject structure, test views
    - Add integration tests for complete/inheritance/templates if not covered in 3.1/4.1/5.1
    - Maximum 10 additional tests to cover critical gaps
  - [ ] 6.3 Implement tree traversal with structural pattern matching
    - Each test loads Site using `make_site("examples.[name]")`
    - Use `match`/`case` to verify node types during traversal
    - Traverse: `site.items` → Sections, `section.items` → Subjects, `subject.items` → Stories
    - Validate parent references and package_path values
  - [ ] 6.4 Add component rendering tests with aria-testing
    - For each Story in each example, render `story.instance`
    - Use `get_by_tag_name()` to find component elements
    - Use `get_text_content()` to verify prop values rendered
    - Verify standard ARIA attributes (roles, labels, states only)
    - Focus on verifying components rendered with expected props
  - [ ] 6.5 Add view rendering tests with aria-testing
    - For each Section: create `SectionView(section=section)()` and verify with aria-testing
    - For each Subject: create `SubjectView(subject=subject)()` and verify with aria-testing
    - For each Story: create `StoryView(story=story)()` and verify with aria-testing
    - Use `isinstance(result, Element)` type guard for all views
    - Verify h1 titles, description paragraphs, navigation links
    - Check titles, descriptions, and props display correctly
  - [ ] 6.6 Add field inheritance validation tests
    - Verify `story.target is None` means Story inherits from Subject
    - Verify `story.title is None` means auto-generated from Subject
    - Check explicit Story titles and targets override inheritance
    - Validate parent references throughout tree
  - [ ] 6.7 Run all example tests
    - Run complete test suite: `just test`
    - Expected total: approximately 16-25 tests for all examples
    - Verify all tree traversal, rendering, and inheritance tests pass
    - All tests should be in `tests/test_examples.py`

**Acceptance Criteria:**
- All example tests pass (approximately 16-25 tests total)
- Tree traversal uses structural pattern matching
- Component rendering verified with aria-testing
- All three view types (Section/Subject/Story) tested with aria-testing
- Field inheritance patterns validated
- All 5 examples have comprehensive test coverage
- Tests verify both component output and view rendering

### Phase 4: Quality Assurance

#### Task Group 7: Quality Checks and Documentation Review
**Dependencies:** Task Groups 1-6

- [ ] 7.0 Run quality checks and verify all requirements met
  - [ ] 7.1 Run all quality checks
    - Run `just test` - verify all tests pass
    - Run `just typecheck` - verify type checking passes
    - Run `just fmt` - verify code formatting is correct
    - All checks must pass
  - [ ] 7.2 Verify all 5 examples exist with correct structure
    - Confirm `examples/minimal/` has README.md and correct structure
    - Confirm `examples/no_sections/` has README.md and correct structure
    - Confirm `examples/complete/` has all files and README.md
    - Confirm `examples/inheritance/` has all files and README.md
    - Confirm `examples/templates/` has all files and README.md
  - [ ] 7.3 Verify all Story variations are demonstrated
    - Story with props only (inheriting target) - in minimal, complete
    - Story with own target (override) - in inheritance
    - Story with custom template - in templates
    - Story with title and description - in complete
    - Story with minimal config - in minimal, inheritance
    - Stories with different prop combinations - in complete, inheritance
  - [ ] 7.4 Review all README.md files for quality
    - Each README has Overview, Structure, Key Features sections
    - Each README is under 20 lines
    - Each README clearly explains what features example demonstrates
    - Markdown formatting is correct
  - [ ] 7.5 Verify all components are simple
    - All components use dataclass pattern
    - All components have 2-3 props maximum
    - All components implement `__call__() -> Node`
    - All components use `html(t"...")` tdom t-strings
    - No complex nested children, forms, or layouts
  - [ ] 7.6 Verify test coverage completeness
    - All examples have tree traversal tests
    - All examples have component rendering tests with aria-testing
    - All examples have view rendering tests (SectionView/SubjectView/StoryView)
    - Inheritance patterns validated with tests
    - Template modes validated with tests
    - Tests use structural pattern matching for tree traversal

**Acceptance Criteria:**
- All quality checks pass (`just test`, `just typecheck`, `just fmt`)
- All 5 examples exist with correct structure
- All 6 Story variations demonstrated across examples
- All README.md files are high quality and under 20 lines
- All components are simple (2-3 props, dataclass pattern)
- All examples have comprehensive test coverage
- Tests verify tree structure, components, and views

## Execution Order

Recommended implementation sequence:

1. **Phase 1: Update Existing Examples** (Task Groups 1-2)
   - Update minimal and no_sections examples with documentation
   - Low risk, establishes documentation pattern
   - Can be done in parallel

2. **Phase 2: Create New Examples** (Task Groups 3-5)
   - Create complete, inheritance, and templates examples
   - Each group builds on understanding from previous groups
   - Execute in sequence: complete → inheritance → templates
   - Each group writes focused tests (2-5 per example)

3. **Phase 3: Comprehensive Test Coverage** (Task Group 6)
   - Review all existing tests from previous groups
   - Add integration tests to fill coverage gaps
   - Implement tree traversal, component rendering, and view rendering tests
   - Maximum 10 additional tests beyond what was written in Phase 2

4. **Phase 4: Quality Assurance** (Task Group 7)
   - Run all quality checks
   - Verify all requirements met
   - Review documentation quality
   - Final validation of completeness

## Testing Strategy

### Test Writing Constraints
- Task Groups 3-5 each write 2-5 focused tests maximum
- Task Group 6 adds maximum 10 additional tests for integration/gaps
- Total expected tests: 16-25 tests across all examples
- Each test group runs ONLY their newly written tests, not entire suite
- Final Task Group 7 runs complete test suite

### Test Coverage Focus
- **Tree structure**: Use structural pattern matching to traverse and validate
- **Component rendering**: Use aria-testing for component output verification
- **View rendering**: Test SectionView, SubjectView, StoryView with aria-testing
- **Field inheritance**: Validate target/title inheritance patterns
- **Template modes**: Verify default vs custom template rendering

### aria-testing Patterns
- Use `get_by_tag_name(element, "h1")` for finding elements
- Use `get_text_content(element)` for extracting text
- Use `query_all_by_tag_name(element, "p")` for multiple elements
- Use `isinstance(result, Element)` type guard for view results
- Focus on standard ARIA attributes only (roles, labels, states)

## Python 3.14+ Standards

All code must follow modern Python standards:
- Use structural pattern matching (`match`/`case`) for tree traversal
- Use modern type hints: `X | Y` syntax, built-in generics
- Use `type` statement for type aliases if needed
- Use dataclass pattern for all components
- Follow tdom t-string pattern for HTML generation

## Notes

- **Example complexity**: Keep components simple (2-3 props max)
- **Testing focus**: Test critical workflows, not exhaustive coverage
- **Documentation**: README files should be concise and focused
- **Code reuse**: Follow existing patterns from minimal example (Heading component)
- **Tree traversal**: Use structural pattern matching as demonstrated in `make_site()`
- **View protocol**: All views implement `__call__() -> Node` protocol
- **Quality gates**: All checks must pass before feature is complete
